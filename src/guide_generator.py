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
    ChangeSet,
)
from .document_processor import DocumentProcessor
from .guide_metadata_manager import GuideMetadataManager


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
        self.metadata_manager = None  # Will be initialized when needed

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

        # If force_full_guide is enabled, load all existing documentation files
        # instead of only processing results from this run
        if state.request.force_full_guide:
            print("Force full guide enabled - loading all existing docs...")
            successful_results = self.load_existing_documentation_results(state)
        else:
            # Process each successful documentation result from this run
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

        # Update metadata for all generated entries
        metadata_manager = self._get_metadata_manager(state.request.output_path)
        generated_entries = {entry.original_file_path: entry.summary for entry in guide_entries}
        metadata_manager.update_metadata_after_generation(state, generated_entries)

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
    
    # ========================
    # Incremental Guide Generation Methods
    # ========================
    
    def _get_metadata_manager(self, output_path: Path) -> GuideMetadataManager:
        """Get or create metadata manager for the output path."""
        if self.metadata_manager is None or self.metadata_manager.output_path != output_path:
            self.metadata_manager = GuideMetadataManager(output_path)
        return self.metadata_manager
    
    def detect_guide_changes(self, state: PipelineState) -> ChangeSet:
        """Detect what files need guide updates.
        
        Args:
            state: Current pipeline state
            
        Returns:
            ChangeSet describing what needs updating
        """
        metadata_manager = self._get_metadata_manager(state.request.output_path)
        
        # Get successful results that aren't skipped
        current_results = [
            r for r in state.results
            if r.success and r.documentation != "[SKIPPED - No changes detected]"
        ]
        
        changeset = metadata_manager.detect_changes(state, current_results)
        
        # Store changeset in state for later use
        state.guide_change_set = changeset
        
        return changeset
    
    def generate_incremental_guide(self, state: PipelineState) -> DocumentationGuide:
        """Generate documentation guide incrementally, only updating changed files.
        
        Args:
            state: Current pipeline state with changeset information
            
        Returns:
            Updated DocumentationGuide
        """
        if not state.guide_change_set:
            self.logger.warning("No changeset found, falling back to full generation")
            return self.generate_documentation_guide(state)
        
        changeset = state.guide_change_set
        metadata_manager = self._get_metadata_manager(state.request.output_path)
        
        # Check if full rebuild is needed
        if metadata_manager.should_force_full_rebuild(changeset):
            self.logger.info("Full rebuild required, regenerating entire guide")
            return self.generate_documentation_guide(state)
        
        print("Generating incremental documentation guide...")
        self.logger.info(f"Incremental update: {len(changeset.new_files)} new, {len(changeset.modified_files)} modified, {len(changeset.deleted_files)} deleted")
        
        # Load existing guide
        existing_guide = self._load_existing_guide(state)
        if not existing_guide:
            self.logger.info("No existing guide found, generating full guide")
            return self.generate_documentation_guide(state)
        
        # Create map of existing entries by source file path
        existing_entries = {entry.original_file_path: entry for entry in existing_guide.entries}
        
        # Files that need new guide entries
        files_to_process = changeset.new_files + changeset.modified_files
        
        # Generate new guide entries for changed files
        new_generated_entries = {}
        for relative_path in files_to_process:
            guide_entry = self._generate_guide_entry_for_file(state, relative_path)
            if guide_entry:
                existing_entries[relative_path] = guide_entry
                new_generated_entries[relative_path] = guide_entry.summary
                self.logger.debug(f"Updated guide entry for: {relative_path}")
        
        # Remove entries for deleted files
        for deleted_file in changeset.deleted_files:
            if deleted_file in existing_entries:
                del existing_entries[deleted_file]
                self.logger.debug(f"Removed guide entry for deleted file: {deleted_file}")
        
        # Create updated guide
        updated_entries = list(existing_entries.values())
        updated_guide = DocumentationGuide(
            entries=updated_entries,
            total_files=len(updated_entries),
            generation_date=datetime.now().isoformat(),
        )
        
        # Update metadata
        metadata_manager.update_metadata_after_generation(state, new_generated_entries)
        
        total_changes = len(files_to_process) + len(changeset.deleted_files)
        print(f"Updated documentation guide: {total_changes} changes, {len(updated_entries)} total entries")
        self.logger.info(f"Incremental guide generation complete: {total_changes} changes processed")
        
        return updated_guide
    
    def _load_existing_guide(self, state: PipelineState) -> Optional[DocumentationGuide]:
        """Load existing documentation guide from file.
        
        Args:
            state: Current pipeline state
            
        Returns:
            Existing DocumentationGuide or None if not found/invalid
        """
        guide_path = state.request.output_path / "documentation_guide.md"
        
        if not guide_path.exists():
            self.logger.debug("No existing guide file found")
            return None
        
        try:
            with open(guide_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Parse the existing guide to extract entries
            entries = self._parse_guide_entries(content)
            
            if not entries:
                self.logger.warning("No valid entries found in existing guide")
                return None
            
            return DocumentationGuide(
                entries=entries,
                total_files=len(entries),
                generation_date=""  # Will be updated when saving
            )
            
        except Exception as e:
            self.logger.error(f"Failed to load existing guide: {e}")
            return None
    
    def _parse_guide_entries(self, guide_content: str) -> List[DocumentationGuideEntry]:
        """Parse guide entries from existing guide content.
        
        Args:
            guide_content: Content of existing guide file
            
        Returns:
            List of DocumentationGuideEntry objects
        """
        entries = []
        
        # Pattern to match guide entries
        # Looking for sections like:
        # ### path/to/file.py
        # **Documentation:** `path/to/file_documentation.md`
        # **Summary:** Summary text here
        entry_pattern = r"### (.+?)\n\n\*\*Documentation:\*\* `(.+?)`\n\n\*\*Summary:\*\* (.+?)\n\n---"
        
        matches = re.findall(entry_pattern, guide_content, re.DOTALL)
        
        for match in matches:
            original_file_path = match[0].strip()
            doc_file_path = match[1].strip()
            summary = match[2].strip()
            
            entry = DocumentationGuideEntry(
                doc_file_path=doc_file_path,
                summary=summary,
                original_file_path=original_file_path
            )
            entries.append(entry)
        
        self.logger.debug(f"Parsed {len(entries)} entries from existing guide")
        return entries
    
    def _generate_single_guide_entry(self, state: PipelineState, result: DocumentationResult) -> Optional[DocumentationGuideEntry]:
        """Generate a single guide entry for a documentation result.
        
        Args:
            state: Current pipeline state
            result: Documentation result to create entry for
            
        Returns:
            DocumentationGuideEntry or None if generation fails
        """
        try:
            relative_source_path = result.file_path.relative_to(state.request.repo_path)
            doc_filename = f"{relative_source_path.stem}_documentation.md"
            doc_relative_path = relative_source_path.parent / doc_filename
            
            # Read the generated documentation
            doc_full_path = state.request.output_path / doc_relative_path
            
            if not doc_full_path.exists():
                self.logger.warning(f"Documentation file not found: {doc_full_path}")
                return None
            
            with open(doc_full_path, "r", encoding="utf-8") as f:
                doc_content = f.read()
            
            # Clean the content (same logic as original method)
            clean_content = self._clean_documentation_content(doc_content)
            
            # Generate summary using LLM
            summary = self._generate_doc_summary(clean_content, str(relative_source_path))
            
            return DocumentationGuideEntry(
                doc_file_path=str(doc_relative_path),
                summary=summary,
                original_file_path=str(relative_source_path),
            )
            
        except Exception as e:
            self.logger.error(f"Failed to generate guide entry for {result.file_path}: {e}")
            return None
    
    def _clean_documentation_content(self, doc_content: str) -> str:
        """Clean documentation content by removing metadata and code sections.
        
        Args:
            doc_content: Raw documentation content
            
        Returns:
            Cleaned content suitable for summarization
        """
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
        
        return clean_content.strip()
    
    def _generate_guide_entry_for_file(self, state: PipelineState, relative_path: str) -> Optional[DocumentationGuideEntry]:
        """Generate a guide entry for any file by relative path, not just from state.results.
        
        Args:
            state: Current pipeline state
            relative_path: Relative path to the source file
            
        Returns:
            DocumentationGuideEntry or None if generation fails
        """
        try:
            # Calculate documentation file path
            path_obj = Path(relative_path)
            doc_filename = f"{path_obj.stem}_documentation.md"
            doc_relative_path = path_obj.parent / doc_filename
            doc_full_path = state.request.output_path / doc_relative_path
            
            if not doc_full_path.exists():
                self.logger.warning(f"Documentation file not found: {doc_full_path}")
                return None
            
            # Read the documentation content
            with open(doc_full_path, "r", encoding="utf-8") as f:
                doc_content = f.read()
            
            # Clean the content
            clean_content = self._clean_documentation_content(doc_content)
            
            # Generate summary using LLM
            summary = self._generate_doc_summary(clean_content, relative_path)
            
            return DocumentationGuideEntry(
                doc_file_path=str(doc_relative_path),
                summary=summary,
                original_file_path=relative_path,
            )
            
        except Exception as e:
            self.logger.error(f"Failed to generate guide entry for {relative_path}: {e}")
            return None