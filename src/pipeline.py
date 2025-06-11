from datetime import datetime
import hashlib
import logging
import re
import yaml
from typing import Dict, Any, List, Optional
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from pathlib import Path

from .models import (
    DocumentationGuide,
    DocumentationGuideEntry,
    PipelineState,
    DocumentationContext,
    DocumentationResult,
    CodeFile,
    DocumentationRequest,
)
from .config import ConfigManager
from .document_processor import DocumentProcessor
from .code_analyzer import CodeAnalyzer


class DocumentationPipeline:
    """Main LangGraph pipeline for generating documentation."""

    def __init__(self, config_path: str = "config.yaml"):
        self.config_manager = ConfigManager(config_path)
        self.config = self.config_manager.load_config()
        self.doc_processor = DocumentProcessor(self.config)
        self.code_analyzer = CodeAnalyzer(self.config)
        self.llm = self._initialize_llm()
        self._setup_logging()

    def _setup_logging(self):
        """Setup logging for the pipeline."""
        log_level = logging.INFO
        if hasattr(self.config, 'logging') and self.config.logging.get('debug', False):
            log_level = logging.DEBUG

        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('documentation_pipeline.log')
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("Documentation pipeline initialized")

    def _initialize_llm(self):
        """Initialize the language model based on configuration."""
        model_config = self.config_manager.get_model_config()
        provider = model_config.get("provider", "openai")

        if provider == "openai":
            # Use environment variable or passed key
            import os

            api_key = model_config.get("api_key") or os.getenv("OPENAI_API_KEY")
            return ChatOpenAI(
                model=model_config.get("name", "gpt-4o"),
                temperature=model_config.get("temperature", 0.2),
                api_key=api_key,
            )
        elif provider == "anthropic":
            import os

            api_key = model_config.get("api_key") or os.getenv("ANTHROPIC_API_KEY")
            return ChatAnthropic(
                model=model_config.get("name", "claude-3.5-sonnet-latest"),
                temperature=model_config.get("temperature", 0.2),
                api_key=api_key,
                timeout=model_config.get("timeout", 60.0),
            )
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def _load_existing_documentation_results(self, state: PipelineState) -> List[DocumentationResult]:
        """Load existing documentation files and create DocumentationResult objects with error handling."""
        self.logger.info("Loading existing documentation files...")
        print("Loading existing documentation files...")

        output_path = state.request.output_path
        if not output_path.exists():
            self.logger.warning(f"No existing documentation found at {output_path}")
            print(f"No existing documentation found at {output_path}")
            return []

        results = []
        failed_loads = 0

        # Find all documentation files
        for doc_file in output_path.rglob("*_documentation.md"):
            try:
                # Extract metadata to get original file path
                metadata = self._extract_metadata_from_doc(doc_file)
                if not metadata:
                    self.logger.warning(f"No metadata found in {doc_file}, skipping")
                    print(f"Warning: No metadata found in {doc_file}, skipping")
                    failed_loads += 1
                    continue

                relative_path = metadata.get("relative_path")
                if not relative_path:
                    self.logger.warning(f"No relative_path in metadata for {doc_file}, skipping")
                    print(f"Warning: No relative_path in metadata for {doc_file}, skipping")
                    failed_loads += 1
                    continue

                # Construct original file path
                original_file_path = state.request.repo_path / relative_path

                # Read the documentation content
                with open(doc_file, "r", encoding="utf-8") as f:
                    doc_content = f.read()

                # Extract just the LLM-generated content (remove headers and metadata)
                import re

                # Find content between the title and either "## Original Code" or the metadata
                content_start = doc_content.find("# Documentation for")
                if content_start == -1:
                    content_start = 0

                clean_content = doc_content[content_start:]

                # Remove original code section and metadata
                original_code_pattern = r"\n## Original Code\n.*"
                clean_content = re.sub(
                    original_code_pattern, "", clean_content, flags=re.DOTALL
                )

                metadata_pattern = r"\n---\n<!-- GENERATION METADATA -->.*"
                clean_content = re.sub(
                    metadata_pattern, "", clean_content, flags=re.DOTALL
                )

                # Create DocumentationResult
                result = DocumentationResult(
                    file_path=original_file_path,
                    documentation=clean_content.strip(),
                    success=True,
                    error_message=None,
                )
                results.append(result)
                self.logger.debug(f"Successfully loaded documentation from {doc_file}")

            except Exception as e:
                error_msg = f"Could not load documentation from {doc_file}: {e}"
                self.logger.error(error_msg, exc_info=True)
                print(f"Warning: {error_msg}")
                failed_loads += 1
                continue

        self.logger.info(f"Loaded {len(results)} existing documentation files, {failed_loads} failed to load")
        print(f"Loaded {len(results)} existing documentation files")

        if failed_loads > 0:
            print(f"Warning: {failed_loads} documentation files failed to load")

        return results

    def load_existing_documentation(self, state: PipelineState) -> Dict[str, Any]:
        """Load existing documentation files instead of generating new ones with error handling."""
        self.logger.info("Loading existing documentation for design docs generation...")
        print("Loading existing documentation for design docs generation...")

        try:
            # Load existing documentation results
            existing_results = self._load_existing_documentation_results(state)

            if not existing_results:
                error_msg = (f"No existing documentation found at {state.request.output_path}. "
                            "Please generate individual file documentation first, or run without --design-docs-only flag.")
                self.logger.error(error_msg)
                raise ValueError(error_msg)

            # Also load existing docs context if available
            docs_path = state.request.docs_path
            docs = self.doc_processor.load_existing_docs(docs_path)

            self.logger.info(f"Successfully loaded {len(existing_results)} existing documentation files")

            return {
                "existing_docs": docs,
                "results": existing_results,
                "code_files": [],  # Empty since we're not processing source files
                "current_file_index": len(existing_results),  # Set to end
                "completed": False,
            }

        except Exception as e:
            self.logger.error(f"Failed to load existing documentation: {e}", exc_info=True)
            raise

    def should_load_existing_docs(self, state: PipelineState) -> str:
        """Determine whether to load existing docs or generate new ones."""
        if state.request.design_docs_only:
            return "load_existing"
        return "continue"

    def create_pipeline(self):
        """Create the LangGraph pipeline."""
        workflow = StateGraph(PipelineState)

        # Add nodes
        workflow.add_node("load_existing_docs", self.load_existing_docs)
        workflow.add_node("load_existing_documentation", self.load_existing_documentation)
        workflow.add_node("load_documentation_guide", self.load_documentation_guide)
        workflow.add_node("summarize_docs", self.summarize_docs)
        workflow.add_node("scan_repository", self.scan_repository)
        workflow.add_node("generate_documentation", self.generate_documentation)
        workflow.add_node("generate_design_docs", self.generate_design_documentation)
        workflow.add_node("initialize_design_documents", self.initialize_design_documents)
        workflow.add_node("generate_design_section", self.generate_design_section)
        workflow.add_node("assemble_design_document", self.assemble_design_document)
        workflow.add_node("save_results", self.save_results)

        # Add edges
        workflow.set_entry_point("load_existing_docs")

        # First decision: design-docs-only or normal flow
        workflow.add_conditional_edges(
            "load_existing_docs",
            self.should_load_existing_docs,
            {
                "load_existing": "load_existing_documentation",
                "continue": "check_summarization",
            },
        )

        # Add a separate node for summarization check
        workflow.add_node("check_summarization", self.check_summarization_step)
        workflow.add_conditional_edges(
            "check_summarization",
            self.should_summarize,
            {"summarize": "summarize_docs", "continue": "check_file_generation"},
        )

        # Check if we should generate file documentation
        workflow.add_node("check_file_generation", self.check_file_generation_step)
        workflow.add_conditional_edges(
            "check_file_generation",
            self.should_generate_files,
            {"generate": "scan_repository", "skip": "generate_design_docs"},
        )

        workflow.add_edge("summarize_docs", "check_file_generation")
        workflow.add_edge("scan_repository", "generate_documentation")
        workflow.add_conditional_edges(
            "generate_documentation",
            self.has_more_files,
            {"continue": "generate_documentation", "finish": "generate_design_docs"},
        )

        # Design-docs-only path
        workflow.add_edge("load_existing_documentation", "load_documentation_guide")
        workflow.add_edge("load_documentation_guide", "generate_design_docs")

        # Design docs workflow
        workflow.add_conditional_edges(
            "generate_design_docs",
            self.should_generate_design_docs,
            {"generate": "initialize_design_documents", "skip": "save_results"},
        )

        workflow.add_edge("initialize_design_documents", "generate_design_section")
        workflow.add_conditional_edges(
            "generate_design_section",
            self.has_more_sections,
            {
                "continue": "generate_design_section",
                "assemble": "assemble_design_document",
                "next_document": "initialize_design_documents",
                "finish": "save_results",
            },
        )

        workflow.add_conditional_edges(
            "assemble_design_document",
            self.has_more_documents,
            {"continue": "initialize_design_documents", "finish": "save_results"},
        )

        workflow.add_edge("save_results", END)

        return workflow.compile()
    
    def check_file_generation_step(self, state: PipelineState) -> Dict[str, Any]:
        """Pass-through step for file generation check."""
        return {}

    def should_generate_files(self, state: PipelineState) -> str:
        """Determine if file documentation should be generated."""
        if state.request.generate_file_documentation:
            return "generate"
        return "skip"

    def should_generate_design_docs(self, state: PipelineState) -> str:
        """Determine if design documentation should be generated."""
        if state.request.generate_design_docs:
            return "generate"
        return "skip"
    
    def load_documentation_guide(self, state: PipelineState) -> Dict[str, Any]:
        """Load existing documentation guide if available."""
        if not state.request.generate_documentation_guide:
            # Check if we should load existing guide for design docs generation
            if state.request.generate_design_docs:
                guide_path = state.request.output_path / "documentation_guide.md"
                if guide_path.exists():
                    try:
                        with open(guide_path, "r", encoding="utf-8") as f:
                            guide_content = f.read()
                        print(f"✓ Loaded existing documentation guide for design docs context")

                        # Add guide content to existing docs context
                        current_content = state.existing_docs.content
                        enhanced_content = f"{current_content}\n\n## Documentation Guide\n{guide_content}"

                        enhanced_docs = DocumentationContext(
                            content=enhanced_content,
                            token_count=self.doc_processor.count_tokens(enhanced_content),
                            summarized=state.existing_docs.summarized,
                            original_docs=state.existing_docs.original_docs + [guide_content],
                        )

                        return {"existing_docs": enhanced_docs}

                    except Exception as e:
                        print(f"Warning: Could not load documentation guide from {guide_path}: {e}")
            return {}

        # Original logic for when guide generation is requested
        guide_path = state.request.output_path / "documentation_guide.md"

        if guide_path.exists():
            try:
                with open(guide_path, "r", encoding="utf-8") as f:
                    guide_content = f.read()
                print(f"✓ Loaded existing documentation guide from {guide_path}")

                # Add guide content to existing docs context
                current_content = state.existing_docs.content
                enhanced_content = f"{current_content}\n\n## Documentation Guide\n{guide_content}"

                enhanced_docs = DocumentationContext(
                    content=enhanced_content,
                    token_count=self.doc_processor.count_tokens(enhanced_content),
                    summarized=state.existing_docs.summarized,
                    original_docs=state.existing_docs.original_docs + [guide_content],
                )

                return {"existing_docs": enhanced_docs}

            except Exception as e:
                print(f"Warning: Could not load documentation guide from {guide_path}: {e}")

        return {}
    
    def has_more_sections(self, state: PipelineState) -> str:
        """Check if there are more sections to process in the current document."""
        design_state = state.design_documentation_state
        if not design_state:
            return "finish"

        current_doc = design_state.documents[design_state.current_document_index]

        # Check if current section is complete
        if design_state.current_section_index < len(current_doc.sections):
            return "continue"

        # Current document sections are complete, check if we need to assemble
        if not current_doc.assembled_content:
            return "assemble"

        # Document is complete, check if there are more documents
        if design_state.current_document_index + 1 < len(design_state.documents):
            return "next_document"

        return "finish"

    def has_more_documents(self, state: PipelineState) -> str:
        """Check if there are more documents to process."""
        design_state = state.design_documentation_state
        if not design_state:
            return "finish"

        if design_state.current_document_index + 1 < len(design_state.documents):
            return "continue"

        return "finish"

    def check_summarization_step(self, state: PipelineState) -> Dict[str, Any]:
        """Pass-through step for summarization check."""
        return {}

    def load_existing_docs(self, state: PipelineState) -> Dict[str, Any]:
        """Load and process existing documentation."""
        print("Loading existing documentation...")

        # Handle optional docs_path
        docs_path = state.request.docs_path
        docs = self.doc_processor.load_existing_docs(docs_path)

        return {"existing_docs": docs}

    def should_summarize(self, state: PipelineState) -> str:
        """Determine if documentation needs summarization."""
        if self.doc_processor.needs_summarization(state.existing_docs):
            return "summarize"
        return "continue"

    def summarize_docs(self, state: PipelineState) -> Dict[str, Any]:
        """Summarize existing documentation if it's too large with error handling."""
        self.logger.info("Starting documentation summarization...")
        print("Summarizing existing documentation...")

        docs = state.existing_docs
        chunks = self.doc_processor.create_chunks(docs.content)

        self.logger.info(f"Created {len(chunks)} chunks for summarization")

        summarization_prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content="""You are a technical documentation summarizer. 
Summarize the following documentation chunk while preserving:
1. Key technical concepts and terminology
2. Important architectural decisions
3. Critical implementation details
4. Dependencies and relationships

Keep the summary concise but comprehensive."""
                ),
                HumanMessage(content="Summarize this documentation:\n\n{chunk}"),
            ]
        )

        summaries = []
        failed_chunks = 0

        for i, chunk in enumerate(chunks):
            try:
                self.logger.debug(f"Summarizing chunk {i+1}/{len(chunks)}")
                messages = summarization_prompt.format_messages(chunk=chunk)
                response = self.llm.invoke(messages)

                # Handle different response types
                if hasattr(response, "content"):
                    content = response.content
                else:
                    content = str(response)
                summaries.append(content)

            except Exception as e:
                error_msg = f"Error summarizing chunk {i+1}: {e}"
                self.logger.error(error_msg, exc_info=True)
                print(f"Error summarizing chunk: {e}")
                summaries.append(chunk[:500] + "...")  # Fallback truncation
                failed_chunks += 1

        if failed_chunks > 0:
            self.logger.warning(f"{failed_chunks}/{len(chunks)} chunks failed summarization, using fallback truncation")

        summarized_content = "\n\n".join(summaries)
        summarized_docs = DocumentationContext(
            content=summarized_content,
            token_count=self.doc_processor.count_tokens(summarized_content),
            summarized=True,
            original_docs=docs.original_docs,
        )

        self.logger.info(f"Summarization complete. Original: {docs.token_count} tokens, Summarized: {summarized_docs.token_count} tokens")
        return {"existing_docs": summarized_docs}

    def scan_repository(self, state: PipelineState) -> Dict[str, Any]:
        """Scan the repository for code files."""
        print(f"Scanning repository: {state.request.repo_path}")

        code_files = self.code_analyzer.scan_repository(state.request.repo_path)

        # Apply max_files limit if configured
        max_files = state.request.config.processing.get("max_files")
        if max_files and max_files > 0:
            code_files = code_files[:max_files]
            print(f"Limited to {max_files} files (configured maximum)")

        print(f"Found {len(code_files)} code files to document")

        return {"code_files": code_files, "current_file_index": 0}

    def save_single_result(self, state: PipelineState, result: DocumentationResult) -> None:
        """Save documentation for a single file immediately with error handling."""
        if not result.success:
            self.logger.debug(f"Skipping save for failed result: {result.file_path}")
            return

        # Skip saving if this was a skipped file
        if result.documentation == "[SKIPPED - No changes detected]":
            self.logger.debug(f"Skipping save for unchanged file: {result.file_path}")
            return

        try:
            output_path = state.request.output_path
            output_path.mkdir(parents=True, exist_ok=True)

            # Create output filename
            relative_path = result.file_path.relative_to(state.request.repo_path)
            doc_filename = f"{relative_path.stem}_documentation.md"
            doc_path = output_path / relative_path.parent / doc_filename

            # Create directory if needed
            doc_path.parent.mkdir(parents=True, exist_ok=True)

            # Calculate file hash and generation timestamp
            file_hash = self._calculate_file_hash(result.file_path)
            generation_date = datetime.now().isoformat()

            # Write documentation with header notice and footer metadata
            with open(doc_path, "w", encoding="utf-8") as f:
                # Header notice
                f.write("<!-- AUTO-GENERATED DOCUMENTATION -->\n")
                f.write(
                    "<!-- This file was automatically generated and should not be manually edited -->\n"
                )
                f.write(
                    "<!-- To update this documentation, regenerate it using the documentation pipeline -->\n\n"
                )

                # Original title and LLM-generated content
                f.write(f"# Documentation for {relative_path}\n\n")
                f.write(result.documentation)

                # Include original code if configured
                if self.config.output.get("include_code", True):
                    f.write(f"\n\n## Original Code\n\n")
                    f.write(
                        f"```{result.file_path.suffix[1:] if result.file_path.suffix else 'text'}\n"
                    )
                    with open(
                        result.file_path, "r", encoding="utf-8", errors="ignore"
                    ) as code_file:
                        f.write(code_file.read())
                    f.write("\n```")

                # Footer with machine-readable metadata
                f.write("\n\n---\n")
                f.write("<!-- GENERATION METADATA -->\n")
                f.write("```yaml\n")
                f.write("# Documentation Generation Metadata\n")
                f.write(f"file_hash: {file_hash}\n")
                f.write(f"relative_path: {relative_path}\n")
                f.write(f"generation_date: {generation_date}\n")
                f.write("```\n")
                f.write("<!-- END GENERATION METADATA -->\n")

            self.logger.debug(f"Successfully saved documentation to: {doc_path}")
            print(f"  ✓ Saved documentation: {doc_path}")

        except Exception as e:
            error_msg = f"Failed to save documentation for {result.file_path}: {e}"
            self.logger.error(error_msg, exc_info=True)
            raise Exception(error_msg) from e

    def has_more_files(self, state: PipelineState) -> str:
        """Check if there are more files to process."""
        if state.current_file_index >= len(state.code_files):
            return "finish"
        return "continue"

    def _extract_metadata_from_doc(self, doc_path: Path) -> Optional[Dict[str, str]]:
        """Extract generation metadata from an existing documentation file with error handling."""
        if not doc_path.exists():
            self.logger.warning(f"Documentation file does not exist: {doc_path}")
            return None

        try:
            with open(doc_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Look for YAML metadata block
            yaml_pattern = r"<!-- GENERATION METADATA -->\s*```yaml\s*\n(.*?)\n```\s*<!-- END GENERATION METADATA -->"
            yaml_match = re.search(yaml_pattern, content, re.DOTALL)

            if yaml_match:
                yaml_content = yaml_match.group(1)
                # Parse the YAML content
                metadata = {}
                for line in yaml_content.split("\n"):
                    line = line.strip()
                    if line and not line.startswith("#"):
                        if ":" in line:
                            key, value = line.split(":", 1)
                            metadata[key.strip()] = value.strip()
                self.logger.debug(f"Successfully extracted YAML metadata from {doc_path}")
                return metadata

            # Fallback: Look for HTML comment metadata
            html_pattern = r"<!-- GENERATION_METADATA\s*\n(.*?)\n-->"
            html_match = re.search(html_pattern, content, re.DOTALL)

            if html_match:
                metadata_content = html_match.group(1)
                metadata = {}
                for line in metadata_content.split("\n"):
                    line = line.strip()
                    if line and ":" in line:
                        key, value = line.split(":", 1)
                        metadata[key.strip()] = value.strip()
                self.logger.debug(f"Successfully extracted HTML metadata from {doc_path}")
                return metadata

            self.logger.warning(f"No metadata found in documentation file: {doc_path}")
            return None

        except Exception as e:
            error_msg = f"Could not read metadata from {doc_path}: {e}"
            self.logger.error(error_msg, exc_info=True)
            print(f"Warning: {error_msg}")
            return None

    def _should_generate_documentation(
        self, state: PipelineState, code_file: CodeFile
    ) -> bool:
        """Check if documentation should be generated for a file based on changes."""
        # Calculate expected output path
        output_path = state.request.output_path
        relative_path = code_file.path.relative_to(state.request.repo_path)
        doc_filename = f"{relative_path.stem}_documentation.md"
        doc_path = output_path / relative_path.parent / doc_filename

        # If no existing documentation, generate it
        if not doc_path.exists():
            print(f"  → No existing documentation found, will generate")
            return True

        # Extract metadata from existing documentation
        existing_metadata = self._extract_metadata_from_doc(doc_path)
        if not existing_metadata:
            print(f"  → No metadata found in existing documentation, will regenerate")
            return True

        # Calculate current file hash
        current_hash = self._calculate_file_hash(code_file.path)
        current_relative_path = str(relative_path)

        # Compare with existing metadata
        existing_hash = existing_metadata.get("file_hash")
        existing_path = existing_metadata.get("relative_path")

        if existing_hash == current_hash and existing_path == current_relative_path:
            print(f"  → File unchanged (hash: {current_hash[:8]}...), skipping")
            return False
        else:
            if existing_hash != current_hash:
                print(
                    f"  → File changed (hash: {existing_hash[:8] if existing_hash else 'unknown'}... → {current_hash[:8]}...), will regenerate"
                )
            if existing_path != current_relative_path:
                print(
                    f"  → Path changed ({existing_path} → {current_relative_path}), will regenerate"
                )
            return True

    def generate_documentation(self, state: PipelineState) -> Dict[str, Any]:
        """Generate documentation for the current code file with enhanced error handling."""
        if state.current_file_index >= len(state.code_files):
            return {"completed": True}

        current_file = state.code_files[state.current_file_index]
        total_files = len(state.code_files)
        current_index = state.current_file_index + 1

        self.logger.info(f"Processing file {current_index}/{total_files}: {current_file.relative_path}")
        print(f"Processing file: {current_file.relative_path} ({current_index}/{total_files})")

        # Check if we should generate documentation for this file
        if not self._should_generate_documentation(state, current_file):
            self.logger.info(f"Skipping unchanged file: {current_file.relative_path}")
            # Create a "skipped" result to track that we processed this file
            result = DocumentationResult(
                file_path=current_file.path,
                documentation="[SKIPPED - No changes detected]",
                success=True,
                error_message=None,
            )

            # Update results and move to next file
            new_results = state.results + [result]
            new_index = state.current_file_index + 1
            return {"results": new_results, "current_file_index": new_index}

        self.logger.info(f"Generating documentation for: {current_file.relative_path}")
        print(f"  → Generating documentation...")

        try:
            # Prepare context
            context = self.doc_processor.prepare_context(state.existing_docs)

            # Create documentation prompt
            doc_prompt = ChatPromptTemplate.from_messages(
                [
                    SystemMessage(
                        content=f"""You are a technical documentation generator. Create comprehensive documentation for the provided code file.

Use this existing project documentation as context:
{context}

Generate documentation that includes:
1. **Purpose**: What this file does and why it exists
2. **Functionality**: Detailed explanation of the main functions/classes
3. **Key Components**: Important classes, functions, variables, or modules
4. **Dependencies**: What this file depends on and what depends on it
5. **Usage Examples**: How this code would typically be used

Format the output as clean Markdown. Be thorough but concise.
File extension: {current_file.extension}
Relative path: {current_file.relative_path}"""
                    ),
                    HumanMessage(
                        content=f"Document this code file:\n\n```{current_file.extension[1:] if current_file.extension else 'text'}\n{current_file.content}\n```"
                    ),
                ]
            )

            messages = doc_prompt.format_messages()
            response = self.llm.invoke(messages)

            # Handle different response types
            if hasattr(response, "content"):
                documentation = response.content
            else:
                documentation = str(response)

            result = DocumentationResult(
                file_path=current_file.path, documentation=documentation, success=True
            )

            # Save immediately if incremental saving is enabled
            save_incrementally = state.request.config.processing.get(
                "save_incrementally", True
            )
            if save_incrementally:
                try:
                    self.save_single_result(state, result)
                    self.logger.info(f"Successfully saved documentation for: {current_file.relative_path}")
                except Exception as save_error:
                    self.logger.error(f"Failed to save documentation for {current_file.relative_path}: {save_error}")
                    result.success = False
                    result.error_message = f"Save failed: {str(save_error)}"

        except Exception as e:
            error_msg = f"Failed to generate documentation for {current_file.relative_path}: {str(e)}"
            self.logger.error(error_msg, exc_info=True)

            result = DocumentationResult(
                file_path=current_file.path,
                documentation="",
                success=False,
                error_message=str(e),
            )
            print(f"  → Error generating documentation: {e}")

        # Update results and move to next file
        new_results = state.results + [result]
        new_index = state.current_file_index + 1

        # Log progress
        successful_so_far = len([r for r in new_results if r.success])
        failed_so_far = len([r for r in new_results if not r.success])
        self.logger.info(f"Progress: {current_index}/{total_files} processed, {successful_so_far} successful, {failed_so_far} failed")

        return {"results": new_results, "current_file_index": new_index}

    def _generate_documentation_guide(self, state: PipelineState) -> DocumentationGuide:
        """Generate a documentation guide from the created documentation files."""
        print("Generating documentation guide...")

        guide_entries = []
        output_path = state.request.output_path

        # Process each successful documentation result
        successful_results = [
            r
            for r in state.results
            if r.success and r.documentation != "[SKIPPED - No changes detected]"
        ]

        for result in successful_results:
            # Calculate paths
            relative_source_path = result.file_path.relative_to(state.request.repo_path)
            doc_filename = f"{relative_source_path.stem}_documentation.md"
            doc_relative_path = relative_source_path.parent / doc_filename

            # Read the generated documentation to create a summary
            doc_full_path = output_path / doc_relative_path

            if doc_full_path.exists():
                try:
                    with open(doc_full_path, "r", encoding="utf-8") as f:
                        doc_content = f.read()

                    # Extract just the LLM-generated content (skip header comments and metadata)
                    # Find content between the title and either "## Original Code" or the metadata
                    import re

                    # Remove header comments
                    content_start = doc_content.find("# Documentation for")
                    if content_start == -1:
                        content_start = 0

                    clean_content = doc_content[content_start:]

                    # Remove original code section and metadata
                    original_code_pattern = r"\n## Original Code\n.*"
                    clean_content = re.sub(
                        original_code_pattern, "", clean_content, flags=re.DOTALL
                    )

                    metadata_pattern = r"\n---\n<!-- GENERATION METADATA -->.*"
                    clean_content = re.sub(
                        metadata_pattern, "", clean_content, flags=re.DOTALL
                    )

                    # Generate summary using LLM
                    summary = self._generate_doc_summary(
                        clean_content, str(relative_source_path)
                    )

                    guide_entry = DocumentationGuideEntry(
                        doc_file_path=str(doc_relative_path),
                        summary=summary,
                        original_file_path=str(relative_source_path),
                    )
                    guide_entries.append(guide_entry)

                except Exception as e:
                    print(
                        f"Warning: Could not process documentation file {doc_full_path}: {e}"
                    )
                    # Create a basic entry even if we can't read the file
                    guide_entry = DocumentationGuideEntry(
                        doc_file_path=str(doc_relative_path),
                        summary=f"Documentation for {relative_source_path} (summary unavailable)",
                        original_file_path=str(relative_source_path),
                    )
                    guide_entries.append(guide_entry)

        # Create the documentation guide
        guide = DocumentationGuide(
            entries=guide_entries,
            total_files=len(guide_entries),
            generation_date=datetime.now().isoformat(),
        )

        print(f"Generated documentation guide with {len(guide_entries)} entries")
        return guide

    def _generate_doc_summary(self, doc_content: str, file_path: str) -> str:
        """Generate a concise summary of documentation content using LLM."""

        summary_prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content="""You are a technical documentation summarizer. Create a concise 2-4 sentence summary of the provided documentation that captures:
1. The primary purpose/function of the code
2. Key components or functionality

Keep the summary brief but informative enough for an AI to determine if this documentation is relevant for a specific task.
Focus on WHAT the code does, not HOW it's documented."""
                ),
                HumanMessage(
                    content=f"Summarize this documentation for file '{file_path}':\n\n{doc_content}..."
                ),
            ]
        )

        try:
            messages = summary_prompt.format_messages()
            response = self.llm.invoke(messages)

            if hasattr(response, "content"):
                summary = response.content.strip()
            else:
                summary = str(response).strip()

            return summary

        except Exception as e:
            print(f"Warning: Could not generate summary for {file_path}: {e}")
            # Fallback to a basic summary
            return f"Documentation for {file_path}"

    def _save_documentation_guide(
        self, state: PipelineState, guide: DocumentationGuide
    ) -> None:
        """Save the documentation guide to a file."""

        output_path = state.request.output_path
        guide_path = output_path / "documentation_guide.md"

        # Create the guide content
        guide_content = f"""# Documentation Guide

<!-- AUTO-GENERATED DOCUMENTATION GUIDE -->
<!-- This file was automatically generated and should not be manually edited -->

This guide provides an overview of all generated documentation files in this repository.
Use this guide to quickly locate relevant documentation when working on specific features or components.

**Generated on:** {guide.generation_date}  
**Total documented files:** {guide.total_files}

## Documentation Files

"""

        # Add each entry
        for entry in guide.entries:
            guide_content += f"### {entry.original_file_path}\n\n"
            guide_content += f"**Documentation:** `{entry.doc_file_path}`\n\n"
            guide_content += f"**Summary:** {entry.summary}\n\n"
            guide_content += "---\n\n"

        # Save the guide
        with open(guide_path, "w", encoding="utf-8") as f:
            f.write(guide_content)

        print(f"✓ Documentation guide saved: {guide_path}")

    def generate_design_documentation(self, state: PipelineState) -> Dict[str, Any]:
        """Generate design documentation from the individual file documentation."""
        if not state.request.generate_design_docs:
            return {"completed": True}

        print("Starting design documentation generation...")

        # Generate documentation guide if requested
        if state.request.generate_documentation_guide:
            guide = self._generate_documentation_guide(state)
            self._save_documentation_guide(state, guide)

            # Add guide to existing docs context for design document generation
            if guide and guide.entries:
                guide_content = self._format_guide_for_context(guide)
                current_content = state.existing_docs.content
                enhanced_content = f"{current_content}\n\n## Documentation Guide\n{guide_content}"

                enhanced_docs = DocumentationContext(
                    content=enhanced_content,
                    token_count=self.doc_processor.count_tokens(enhanced_content),
                    summarized=state.existing_docs.summarized,
                    original_docs=state.existing_docs.original_docs + [guide_content],
                )

                # Update state with enhanced docs
                state.existing_docs = enhanced_docs

            return {"documentation_guide": guide, "completed": True}
        else:
            # Try to load existing documentation guide from well-known location
            guide_path = state.request.output_path / "documentation_guide.md"
            if guide_path.exists():
                try:
                    with open(guide_path, "r", encoding="utf-8") as f:
                        guide_content = f.read()
                    print(f"✓ Loaded existing documentation guide from {guide_path}")

                    # Add to existing docs context
                    current_content = state.existing_docs.content
                    enhanced_content = f"{current_content}\n\n## Documentation Guide\n{guide_content}"

                    enhanced_docs = DocumentationContext(
                        content=enhanced_content,
                        token_count=self.doc_processor.count_tokens(enhanced_content),
                        summarized=state.existing_docs.summarized,
                        original_docs=state.existing_docs.original_docs + [guide_content],
                    )

                    # Update state with enhanced docs
                    state.existing_docs = enhanced_docs

                except Exception as e:
                    print(f"Warning: Could not load documentation guide from {guide_path}: {e}")

            return {"completed": True}
        
    def _format_guide_for_context(self, guide: DocumentationGuide) -> str:
        """Format documentation guide for use as context in design document generation."""
        guide_content = f"""Generated on: {guide.generation_date}
    Total documented files: {guide.total_files}

    File Documentation Summary:
    """

        for entry in guide.entries:
            guide_content += f"\n### {entry.original_file_path}\n"
            guide_content += f"Documentation: {entry.doc_file_path}\n"
            guide_content += f"Summary: {entry.summary}\n"

        return guide_content

    def save_results(self, state: PipelineState) -> Dict[str, Any]:
        """Save the summary report and handle any remaining non-incremental saves."""
        print(f"Finalizing documentation in: {state.request.output_path}")

        output_path = state.request.output_path
        output_path.mkdir(parents=True, exist_ok=True)

        # Create design documentation directory if design docs were generated
        if state.request.generate_design_docs and state.design_documentation_state:
            design_docs_path = output_path / "design_documentation"
            design_docs_path.mkdir(parents=True, exist_ok=True)

        # Only save individual files if incremental saving was disabled
        save_incrementally = state.request.config.processing.get(
            "save_incrementally", True
        )
        if not save_incrementally:
            print("Saving all documentation files...")
            # Save individual file documentation
            for result in state.results:
                if result.success:
                    self.save_single_result(state, result)

        # Generate summary report
        self._generate_summary_report(state)

        successful_count = len([r for r in state.results if r.success])
        failed_count = len([r for r in state.results if not r.success])

        print(f"Documentation generation completed!")
        print(f"✓ {successful_count} files documented successfully")
        if failed_count > 0:
            print(f"✗ {failed_count} files failed")

        # Report on design documentation if generated
        if state.design_documentation_state:
            self._report_design_documentation_status(state)

        return {"completed": True}
    
    def _report_design_documentation_status(self, state: PipelineState):
        """Report on the status of design documentation generation."""
        design_state = state.design_documentation_state
        if not design_state:
            return

        successful_docs = len([doc for doc in design_state.documents if doc.success])
        failed_docs = len([doc for doc in design_state.documents if not doc.success])
        total_docs = len(design_state.documents)

        print(f"\n🎨 Design Documentation Status:")
        print(f"   ✓ {successful_docs}/{total_docs} documents generated successfully")

        if failed_docs > 0:
            print(f"   ✗ {failed_docs} documents failed")
            for doc in design_state.documents:
                if not doc.success:
                    print(f"     - {doc.name}: {doc.error_message}")

        # Report section-level details
        total_sections = sum(len(doc.sections) for doc in design_state.documents)
        successful_sections = sum(
            len([s for s in doc.sections if s.success]) 
            for doc in design_state.documents
        )
        failed_sections = total_sections - successful_sections

        print(f"   📝 {successful_sections}/{total_sections} sections generated")
        if failed_sections > 0:
            print(f"   ⚠️  {failed_sections} sections failed")

    def _generate_summary_report(self, state: PipelineState):
        """Generate a summary report of the documentation process."""
        successful = [
            r
            for r in state.results
            if r.success and r.documentation != "[SKIPPED - No changes detected]"
        ]
        skipped = [
            r
            for r in state.results
            if r.success and r.documentation == "[SKIPPED - No changes detected]"
        ]
        failed = [r for r in state.results if not r.success]

        report_content = f"""# Documentation Generation Report

## Summary
- **Total files processed**: {len(state.results)}
- **Successfully documented**: {len(successful)}
- **Skipped (unchanged)**: {len(skipped)}
- **Failed**: {len(failed)}

## Successfully Documented Files
"""

        for result in successful:
            relative_path = result.file_path.relative_to(state.request.repo_path)
            report_content += f"- {relative_path}\n"

        if skipped:
            report_content += "\n## Skipped Files (No Changes)\n"
            for result in skipped:
                relative_path = result.file_path.relative_to(state.request.repo_path)
                report_content += f"- {relative_path}\n"

        if failed:
            report_content += "\n## Failed Files\n"
            for result in failed:
                relative_path = result.file_path.relative_to(state.request.repo_path)
                report_content += f"- {relative_path}: {result.error_message}\n"

        # Add design documentation report
        if state.design_documentation_state:
            report_content += self._generate_design_docs_report_section(state)

        # Add existing documentation info
        if state.existing_docs.content:
            report_content += f"\n## Existing Documentation Context\n"
            report_content += f"- **Token count**: {state.existing_docs.token_count}\n"
            report_content += f"- **Summarized**: {state.existing_docs.summarized}\n"
            report_content += (
                f"- **Original documents**: {len(state.existing_docs.original_docs)}\n"
            )

        # Add processing configuration info
        max_files = state.request.config.processing.get("max_files")
        save_incrementally = state.request.config.processing.get(
            "save_incrementally", True
        )

        report_content += f"\n## Processing Configuration\n"
        report_content += (
            f"- **Max files limit**: {max_files if max_files else 'No limit'}\n"
        )
        report_content += f"- **Incremental saving**: {save_incrementally}\n"
        report_content += f"- **Generate file documentation**: {state.request.generate_file_documentation}\n"
        report_content += f"- **Generate design docs**: {state.request.generate_design_docs}\n"
        report_content += f"- **Generate documentation guide**: {state.request.generate_documentation_guide}\n"
        report_content += f"- **Design docs only**: {state.request.design_docs_only}\n"

        # Save report
        report_path = state.request.output_path / "documentation_report.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report_content)

        print(f"✓ Summary report saved: {report_path}")
    
    def _generate_design_docs_report_section(self, state: PipelineState) -> str:
        """Generate the design documentation section of the summary report."""
        design_state = state.design_documentation_state
        if not design_state:
            return ""

        report_section = "\n## Design Documentation\n"

        successful_docs = [doc for doc in design_state.documents if doc.success]
        failed_docs = [doc for doc in design_state.documents if not doc.success]

        report_section += f"- **Total design documents**: {len(design_state.documents)}\n"
        report_section += f"- **Successfully generated**: {len(successful_docs)}\n"
        report_section += f"- **Failed**: {len(failed_docs)}\n"

        if successful_docs:
            report_section += "\n### Successfully Generated Design Documents\n"
            for doc in successful_docs:
                successful_sections = len([s for s in doc.sections if s.success])
                total_sections = len(doc.sections)
                report_section += f"- **{doc.name}**: {successful_sections}/{total_sections} sections\n"
                if doc.file_path:
                    relative_path = doc.file_path.relative_to(state.request.output_path)
                    report_section += f"  - File: {relative_path}\n"

        if failed_docs:
            report_section += "\n### Failed Design Documents\n"
            for doc in failed_docs:
                report_section += f"- **{doc.name}**: {doc.error_message}\n"

                # Report failed sections
                failed_sections = [s for s in doc.sections if not s.success]
                if failed_sections:
                    report_section += "  - Failed sections:\n"
                    for section in failed_sections:
                        report_section += f"    - {section.name}: {section.error_message}\n"

        # Add section-level statistics
        total_sections = sum(len(doc.sections) for doc in design_state.documents)
        successful_sections = sum(
            len([s for s in doc.sections if s.success]) 
            for doc in design_state.documents
        )

        report_section += f"\n### Section Statistics\n"
        report_section += f"- **Total sections**: {total_sections}\n"
        report_section += f"- **Successful sections**: {successful_sections}\n"
        report_section += f"- **Failed sections**: {total_sections - successful_sections}\n"

        return report_section
    
    def _create_output_directory_structure(self, state: PipelineState):
        """Create the output directory structure for documentation."""
        output_path = state.request.output_path
        output_path.mkdir(parents=True, exist_ok=True)

        # Create design documentation directory if needed
        if state.request.generate_design_docs:
            design_docs_path = output_path / "design_documentation"
            design_docs_path.mkdir(parents=True, exist_ok=True)

            # Create subdirectories for different document types if needed
            # This could be extended in the future for better organization

        print(f"✓ Output directory structure created at: {output_path}")

    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA-256 hash of a file."""
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                # Read file in chunks to handle large files efficiently
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(chunk)
            return sha256_hash.hexdigest()
        except Exception as e:
            print(f"Warning: Could not calculate hash for {file_path}: {e}")
            return "unknown"

    def run(
        self,
        repo_path: Path,
        docs_path: Optional[Path] = None,
        output_path: Optional[Path] = None,
        generate_file_documentation: bool = False,
        generate_design_docs: bool = False,
        generate_documentation_guide: bool = False,
        design_docs_only: bool = False,
    ) -> PipelineState:
        """Run the complete documentation pipeline."""

        if output_path is None:
            output_path = repo_path / "documentation_output"

        # Validate flag combinations
        if design_docs_only and not generate_design_docs:
            raise ValueError(
                "design_docs_only requires generate_design_docs to be True"
            )

        if generate_documentation_guide and not generate_design_docs:
            raise ValueError(
                "generate_documentation_guide requires generate_design_docs to be True"
            )

        request = DocumentationRequest(
            repo_path=repo_path,
            docs_path=docs_path,
            output_path=output_path,
            config=self.config,
            generate_file_documentation=generate_file_documentation,
            generate_design_docs=generate_design_docs,
            generate_documentation_guide=generate_documentation_guide,
            design_docs_only=design_docs_only,
        )

        # Create initial state with empty existing_docs
        initial_docs = DocumentationContext(
            content="", token_count=0, summarized=False, original_docs=[]
        )

        initial_state = PipelineState(request=request, existing_docs=initial_docs)

        pipeline = self.create_pipeline()
        final_state = pipeline.invoke(initial_state)

        return final_state
