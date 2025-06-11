from datetime import datetime
import hashlib
import logging
import re
from typing import Dict, Any, List, Optional, Union
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from pathlib import Path

from .prompts.generate_doc_summary_system_message import GENERATE_DOC_SUMMARY_SYSTEM_MESSAGE

from .models import (
    DocumentationGuide,
    DocumentationGuideEntry,
    PipelineConfig,
    PipelineState,
    DocumentationResult,
)
from .document_processor import DocumentProcessor


class GuideGenerator:
    def __init__(
        self,
        llm: Union[ChatAnthropic, ChatOpenAI],
        config: PipelineConfig,
        doc_processor: DocumentProcessor,
    ):
        """Initialize the GuideGenerator.

        Args:
            llm: The language model instance (ChatOpenAI or ChatAnthropic)
            config: Configuration object containing settings
            doc_processor: DocumentProcessor instance for token counting and context preparation
            logger: Optional logger instance. If None, will create a new one.
        """
        self.llm = llm
        self.config = config
        self.doc_processor = doc_processor

        self.logger = logging.getLogger(__name__)

    def load_existing_documentation(self, state: PipelineState) -> Dict[str, Any]:
        """Load existing documentation files instead of generating new ones with error handling."""
        self.logger.info("Loading existing documentation for design docs generation...")
        print("Loading existing documentation for design docs generation...")

        try:
            # Load existing documentation results
            existing_results = self.load_existing_documentation_results(state)

            if not existing_results:
                error_msg = (
                    f"No existing documentation found at {state.request.output_path}. "
                    "Please generate individual file documentation first."
                )
                self.logger.error(error_msg)
                raise ValueError(error_msg)

            # Also load existing docs context if available
            docs_path = state.request.docs_path
            docs = self.doc_processor.load_existing_docs(docs_path)

            self.logger.info(
                f"Successfully loaded {len(existing_results)} existing documentation files"
            )

            return {
                "existing_docs": docs,
                "results": existing_results,
                "code_files": [],  # Empty since we're not processing source files
                "current_file_index": len(existing_results),  # Set to end
                "completed": False,
            }

        except Exception as e:
            self.logger.error(
                f"Failed to load existing documentation: {e}", exc_info=True
            )
            raise

    def load_existing_documentation_results(
        self, state: PipelineState
    ) -> List[DocumentationResult]:
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
                metadata = self.extract_metadata_from_doc(doc_file)
                if not metadata:
                    self.logger.warning(f"No metadata found in {doc_file}, skipping")
                    print(f"Warning: No metadata found in {doc_file}, skipping")
                    failed_loads += 1
                    continue

                relative_path = metadata.get("relative_path")
                if not relative_path:
                    self.logger.warning(
                        f"No relative_path in metadata for {doc_file}, skipping"
                    )
                    print(
                        f"Warning: No relative_path in metadata for {doc_file}, skipping"
                    )
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

        self.logger.info(
            f"Loaded {len(results)} existing documentation files, {failed_loads} failed to load"
        )
        print(f"Loaded {len(results)} existing documentation files")

        if failed_loads > 0:
            print(f"Warning: {failed_loads} documentation files failed to load")

        return results

    def generate_documentation_guide(self, state: PipelineState) -> DocumentationGuide:
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
                    content=GENERATE_DOC_SUMMARY_SYSTEM_MESSAGE
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

    def save_documentation_guide(
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

    def extract_metadata_from_doc(self, doc_path: Path) -> Optional[Dict[str, str]]:
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
                self.logger.debug(
                    f"Successfully extracted YAML metadata from {doc_path}"
                )
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
                self.logger.debug(
                    f"Successfully extracted HTML metadata from {doc_path}"
                )
                return metadata

            self.logger.warning(f"No metadata found in documentation file: {doc_path}")
            return None

        except Exception as e:
            error_msg = f"Could not read metadata from {doc_path}: {e}"
            self.logger.error(error_msg, exc_info=True)
            print(f"Warning: {error_msg}")
            return None