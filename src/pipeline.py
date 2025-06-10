from datetime import datetime
import hashlib
import re
import yaml
from typing import Dict, Any, Optional
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from pathlib import Path

from .models import (
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

    def create_pipeline(self):
        """Create the LangGraph pipeline."""
        workflow = StateGraph(PipelineState)

        # Add nodes
        workflow.add_node("load_existing_docs", self.load_existing_docs)
        workflow.add_node("summarize_docs", self.summarize_docs)
        workflow.add_node("scan_repository", self.scan_repository)
        workflow.add_node("generate_documentation", self.generate_documentation)
        workflow.add_node("save_results", self.save_results)

        # Add edges
        workflow.set_entry_point("load_existing_docs")
        workflow.add_conditional_edges(
            "load_existing_docs",
            self.should_summarize,
            {"summarize": "summarize_docs", "continue": "scan_repository"},
        )
        workflow.add_edge("summarize_docs", "scan_repository")
        workflow.add_edge("scan_repository", "generate_documentation")
        workflow.add_conditional_edges(
            "generate_documentation",
            self.has_more_files,
            {"continue": "generate_documentation", "finish": "save_results"},
        )
        workflow.add_edge("save_results", END)

        return workflow.compile()

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
        """Summarize existing documentation if it's too large."""
        print("Summarizing existing documentation...")

        docs = state.existing_docs
        chunks = self.doc_processor.create_chunks(docs.content)

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
        for chunk in chunks:
            try:
                messages = summarization_prompt.format_messages(chunk=chunk)
                response = self.llm.invoke(messages)
                # Handle different response types
                if hasattr(response, "content"):
                    content = response.content
                else:
                    content = str(response)
                summaries.append(content)
            except Exception as e:
                print(f"Error summarizing chunk: {e}")
                summaries.append(chunk[:500] + "...")  # Fallback truncation

        summarized_content = "\n\n".join(summaries)
        summarized_docs = DocumentationContext(
            content=summarized_content,
            token_count=self.doc_processor.count_tokens(summarized_content),
            summarized=True,
            original_docs=docs.original_docs,
        )

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
        """Save documentation for a single file immediately."""
        if not result.success:
            return

        # Skip saving if this was a skipped file
        if result.documentation == "[SKIPPED - No changes detected]":
            return

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
            f.write("<!-- This file was automatically generated and should not be manually edited -->\n")
            f.write("<!-- To update this documentation, regenerate it using the documentation pipeline -->\n\n")

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

        print(f"  ✓ Saved documentation: {doc_path}")

    def generate_documentation(self, state: PipelineState) -> Dict[str, Any]:
        """Generate documentation for the current code file."""
        if state.current_file_index >= len(state.code_files):
            return {"completed": True}

        current_file = state.code_files[state.current_file_index]
        total_files = len(state.code_files)
        current_index = state.current_file_index + 1

        print(
            f"Generating documentation for: {current_file.relative_path} ({current_index}/{total_files})"
        )

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

        try:
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
                self.save_single_result(state, result)

        except Exception as e:
            result = DocumentationResult(
                file_path=current_file.path,
                documentation="",
                success=False,
                error_message=str(e),
            )
            print(
                f"Error generating documentation for {current_file.relative_path}: {e}"
            )

        # Update results and move to next file
        new_results = state.results + [result]
        new_index = state.current_file_index + 1

        return {"results": new_results, "current_file_index": new_index}

    def has_more_files(self, state: PipelineState) -> str:
        """Check if there are more files to process."""
        if state.current_file_index >= len(state.code_files):
            return "finish"
        return "continue"

    def _extract_metadata_from_doc(self, doc_path: Path) -> Optional[Dict[str, str]]:
        """Extract generation metadata from an existing documentation file."""
        if not doc_path.exists():
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
                return metadata

            return None

        except Exception as e:
            print(f"Warning: Could not read metadata from {doc_path}: {e}")
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
        """Generate documentation for the current code file."""
        if state.current_file_index >= len(state.code_files):
            return {"completed": True}

        current_file = state.code_files[state.current_file_index]
        total_files = len(state.code_files)
        current_index = state.current_file_index + 1

        print(
            f"Processing file: {current_file.relative_path} ({current_index}/{total_files})"
        )

        # Check if we should generate documentation for this file
        if not self._should_generate_documentation(state, current_file):
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

        print(f"  → Generating documentation...")

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

        try:
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
                self.save_single_result(state, result)

        except Exception as e:
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

        return {"results": new_results, "current_file_index": new_index}

    def save_results(self, state: PipelineState) -> Dict[str, Any]:
        """Save the summary report and handle any remaining non-incremental saves."""
        print(f"Finalizing documentation in: {state.request.output_path}")

        output_path = state.request.output_path
        output_path.mkdir(parents=True, exist_ok=True)

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

        return {"completed": True}

    def _generate_summary_report(self, state: PipelineState):
        """Generate a summary report of the documentation process."""
        successful = [r for r in state.results if r.success and r.documentation != "[SKIPPED - No changes detected]"]
        skipped = [r for r in state.results if r.success and r.documentation == "[SKIPPED - No changes detected]"]
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
        save_incrementally = state.request.config.processing.get("save_incrementally", True)

        report_content += f"\n## Processing Configuration\n"
        report_content += f"- **Max files limit**: {max_files if max_files else 'No limit'}\n"
        report_content += f"- **Incremental saving**: {save_incrementally}\n"

        # Save report
        report_path = state.request.output_path / "documentation_report.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report_content)

        print(f"✓ Summary report saved: {report_path}")

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
    ) -> PipelineState:
        """Run the complete documentation pipeline."""

        if output_path is None:
            output_path = repo_path / "documentation_output"

        request = DocumentationRequest(
            repo_path=repo_path,
            docs_path=docs_path,
            output_path=output_path,
            config=self.config,
        )

        # Create initial state with empty existing_docs
        initial_docs = DocumentationContext(
            content="", token_count=0, summarized=False, original_docs=[]
        )

        initial_state = PipelineState(request=request, existing_docs=initial_docs)

        pipeline = self.create_pipeline()
        final_state = pipeline.invoke(
            initial_state,
            config={"recursion_limit": self.config.processing.get("max_files", 1000)},
        )

        return final_state
