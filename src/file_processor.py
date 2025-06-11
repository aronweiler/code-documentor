import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional
import logging

from .models import PipelineState, DocumentationResult, CodeFile


class FileProcessor:
    """Handles file processing, change detection, and saving of documentation files."""

    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)

    def should_generate_documentation(
        self, state: PipelineState, code_file: CodeFile, guide_generator
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
        existing_metadata = guide_generator.extract_metadata_from_doc(doc_path)
        if not existing_metadata:
            print(f"  → No metadata found in existing documentation, will regenerate")
            return True

        # Calculate current file hash
        current_hash = self.calculate_file_hash(code_file.path)
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

    def save_single_result(
        self, state: PipelineState, result: DocumentationResult
    ) -> None:
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
            file_hash = self.calculate_file_hash(result.file_path)
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

    def calculate_file_hash(self, file_path: Path) -> str:
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

    def create_output_directory_structure(self, state: PipelineState):
        """Create the output directory structure for documentation."""
        output_path = state.request.output_path
        output_path.mkdir(parents=True, exist_ok=True)

        # Create design documentation directory if needed
        if state.request.design_docs:
            design_docs_path = output_path / "design_documentation"
            design_docs_path.mkdir(parents=True, exist_ok=True)

            # Create subdirectories for different document types if needed
            # This could be extended in the future for better organization

        print(f"✓ Output directory structure created at: {output_path}")