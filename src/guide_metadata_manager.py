import json
import hashlib
import os
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging

from .models import (
    FileMetadata,
    GuideMetadata,
    ChangeSet,
    PipelineState,
    DocumentationResult,
)


class GuideMetadataManager:
    """Manages metadata for incremental guide generation."""
    
    def __init__(self, output_path: Path):
        """Initialize the metadata manager.
        
        Args:
            output_path: Path where documentation is output
        """
        self.output_path = output_path
        self.metadata_dir = output_path / ".documentation_state"
        self.metadata_file = self.metadata_dir / "guide_metadata.json"
        self.logger = logging.getLogger(__name__)
        
        # Ensure metadata directory exists
        self.metadata_dir.mkdir(exist_ok=True)
    
    def load_metadata(self) -> GuideMetadata:
        """Load existing guide metadata or create new if none exists."""
        if not self.metadata_file.exists():
            self.logger.info("No existing guide metadata found, creating new")
            return GuideMetadata(
                guide_last_generated=0.0,
                guide_version=1,
                tracked_files={},
                guide_structure_hash=""
            )
        
        try:
            with open(self.metadata_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Convert dict to GuideMetadata, handling nested FileMetadata objects
            tracked_files = {}
            for file_path, file_data in data.get('tracked_files', {}).items():
                tracked_files[file_path] = FileMetadata(**file_data)
            
            metadata = GuideMetadata(
                guide_last_generated=data.get('guide_last_generated', 0.0),
                guide_version=data.get('guide_version', 1),
                tracked_files=tracked_files,
                guide_structure_hash=data.get('guide_structure_hash', "")
            )
            
            self.logger.info(f"Loaded guide metadata with {len(metadata.tracked_files)} tracked files")
            return metadata
            
        except Exception as e:
            self.logger.error(f"Failed to load guide metadata: {e}")
            self.logger.info("Creating new metadata")
            return GuideMetadata(
                guide_last_generated=0.0,
                guide_version=1,
                tracked_files={},
                guide_structure_hash=""
            )
    
    def save_metadata(self, metadata: GuideMetadata) -> None:
        """Save guide metadata to disk."""
        try:
            # Convert to dict for JSON serialization
            data = {
                'guide_last_generated': metadata.guide_last_generated,
                'guide_version': metadata.guide_version,
                'guide_structure_hash': metadata.guide_structure_hash,
                'tracked_files': {}
            }
            
            for file_path, file_metadata in metadata.tracked_files.items():
                data['tracked_files'][file_path] = {
                    'source_file_path': file_metadata.source_file_path,
                    'source_file_modified': file_metadata.source_file_modified,
                    'doc_file_path': file_metadata.doc_file_path,
                    'doc_generated': file_metadata.doc_generated,
                    'doc_file_hash': file_metadata.doc_file_hash,
                    'guide_entry_generated': file_metadata.guide_entry_generated,
                    'guide_entry_hash': file_metadata.guide_entry_hash
                }
            
            # Atomic write to prevent corruption
            temp_file = self.metadata_file.with_suffix('.tmp')
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            
            temp_file.replace(self.metadata_file)
            self.logger.debug(f"Saved guide metadata with {len(metadata.tracked_files)} tracked files")
            
        except Exception as e:
            self.logger.error(f"Failed to save guide metadata: {e}")
            raise
    
    def detect_changes(self, state: PipelineState, current_results: List[DocumentationResult]) -> ChangeSet:
        """Detect what files have changed since last guide generation.
        
        Args:
            state: Current pipeline state
            current_results: Results from current documentation generation
            
        Returns:
            ChangeSet describing what needs to be updated
        """
        metadata = self.load_metadata()
        changeset = ChangeSet()
        
        # Build map of current results by relative path (only newly generated files)
        current_generated_files = {}
        for result in current_results:
            if result.success and result.documentation != "[SKIPPED - No changes detected]":
                relative_path = str(result.file_path.relative_to(state.request.repo_path))
                current_generated_files[relative_path] = result
        
        # Find ALL existing documentation files (not just current generation results)
        all_existing_doc_files = self._discover_all_documentation_files(state)
        
        # Build complete map of all documented files
        all_documented_files = set()
        
        # Add newly generated files
        for relative_path in current_generated_files:
            all_documented_files.add(relative_path)
        
        # Add files that have existing documentation but weren't generated this run
        for relative_path in all_existing_doc_files:
            all_documented_files.add(relative_path)
        
        # Check for new and modified files among ALL documented files
        for relative_path in all_documented_files:
            if relative_path not in metadata.tracked_files:
                # New file (either just generated or existing doc without metadata)
                changeset.new_files.append(relative_path)
                self.logger.debug(f"Detected new file: {relative_path}")
            else:
                # Check if file has been modified
                file_metadata = metadata.tracked_files[relative_path]
                
                # If this file was just generated, it's definitely modified
                if relative_path in current_generated_files:
                    changeset.modified_files.append(relative_path)
                    self.logger.debug(f"Detected modified file (just generated): {relative_path}")
                else:
                    # Check if documentation file has changed since last guide generation
                    doc_path = self.output_path / file_metadata.doc_file_path
                    if doc_path.exists():
                        current_doc_hash = self._calculate_file_hash(doc_path)
                        if current_doc_hash != file_metadata.doc_file_hash:
                            changeset.modified_files.append(relative_path)
                            self.logger.debug(f"Detected modified documentation: {relative_path}")
        
        # Check for deleted files
        for relative_path in metadata.tracked_files:
            if relative_path not in all_documented_files:
                source_file = state.request.repo_path / relative_path
                if not source_file.exists():
                    changeset.deleted_files.append(relative_path)
                    self.logger.debug(f"Detected deleted file: {relative_path}")
        
        # Check if this is the first run (no previous guide)
        guide_path = self.output_path / "documentation_guide.md"
        if not guide_path.exists() or len(metadata.tracked_files) == 0:
            changeset.force_full_rebuild = True
            self.logger.info("First run or missing guide - forcing full rebuild")
        
        total_changes = len(changeset.new_files) + len(changeset.modified_files) + len(changeset.deleted_files)
        total_documented = len(all_documented_files)
        self.logger.info(f"Change detection: {len(changeset.new_files)} new, {len(changeset.modified_files)} modified, {len(changeset.deleted_files)} deleted files out of {total_documented} total documented files")
        
        return changeset
    
    def _discover_all_documentation_files(self, state: PipelineState) -> List[str]:
        """Discover all existing documentation files and map them back to source files.
        
        Args:
            state: Current pipeline state
            
        Returns:
            List of relative source file paths that have documentation
        """
        documented_files = []
        
        if not self.output_path.exists():
            return documented_files
        
        # Find all documentation files
        for doc_file in self.output_path.rglob("*_documentation.md"):
            try:
                # Try to extract the original source file path from the doc file structure
                # Documentation path: output_path/src/module_documentation.md
                # Source path: repo_path/src/module.py (or other extension)
                
                relative_doc_path = doc_file.relative_to(self.output_path)
                
                # Remove '_documentation.md' suffix
                if relative_doc_path.name.endswith('_documentation.md'):
                    base_name = relative_doc_path.name[:-16]  # Remove '_documentation.md'
                    parent_dir = relative_doc_path.parent
                    
                    # Look for the corresponding source file with any supported extension
                    potential_source_dir = state.request.repo_path / parent_dir
                    
                    if potential_source_dir.exists():
                        # Try different extensions
                        supported_extensions = state.request.config.file_processing.get('supported_extensions', ['.py'])
                        
                        for ext in supported_extensions:
                            potential_source = potential_source_dir / f"{base_name}{ext}"
                            if potential_source.exists():
                                relative_source = str(potential_source.relative_to(state.request.repo_path))
                                documented_files.append(relative_source)
                                self.logger.debug(f"Found documented file: {relative_source}")
                                break
                        else:
                            # Fallback: try to extract from metadata in the doc file
                            try:
                                with open(doc_file, 'r', encoding='utf-8') as f:
                                    content = f.read()
                                    
                                # Look for metadata with original file path
                                import re
                                metadata_pattern = r"relative_path:\s*(.+?)(?:\n|$)"
                                match = re.search(metadata_pattern, content)
                                if match:
                                    relative_source = match.group(1).strip()
                                    documented_files.append(relative_source)
                                    self.logger.debug(f"Found documented file from metadata: {relative_source}")
                            except Exception as e:
                                self.logger.warning(f"Could not extract metadata from {doc_file}: {e}")
                
            except Exception as e:
                self.logger.warning(f"Could not process documentation file {doc_file}: {e}")
        
        self.logger.info(f"Discovered {len(documented_files)} existing documented files")
        return documented_files
    
    def update_file_metadata(self, 
                           relative_path: str, 
                           result: DocumentationResult,
                           state: PipelineState,
                           guide_entry_content: str) -> FileMetadata:
        """Update metadata for a single file.
        
        Args:
            relative_path: Relative path to source file
            result: Documentation result for this file
            state: Current pipeline state
            guide_entry_content: Content of the guide entry for this file
            
        Returns:
            Updated FileMetadata object
        """
        source_file = state.request.repo_path / relative_path
        doc_filename = f"{Path(relative_path).stem}_documentation.md"
        doc_relative_path = str(Path(relative_path).parent / doc_filename)
        doc_full_path = self.output_path / doc_relative_path
        
        # Calculate hashes and timestamps
        source_mtime = source_file.stat().st_mtime if source_file.exists() else 0.0
        doc_hash = self._calculate_file_hash(doc_full_path) if doc_full_path.exists() else ""
        guide_entry_hash = self._calculate_string_hash(guide_entry_content)
        current_time = time.time()
        
        return FileMetadata(
            source_file_path=relative_path,
            source_file_modified=source_mtime,
            doc_file_path=doc_relative_path,
            doc_generated=current_time,
            doc_file_hash=doc_hash,
            guide_entry_generated=current_time,
            guide_entry_hash=guide_entry_hash
        )
    
    def update_metadata_after_generation(self, 
                                        state: PipelineState, 
                                        generated_entries: Dict[str, str]) -> None:
        """Update metadata after guide generation.
        
        Args:
            state: Current pipeline state
            generated_entries: Map of relative_path -> guide_entry_content for generated entries
        """
        metadata = self.load_metadata()
        current_time = time.time()
        
        # Update metadata for generated entries
        for relative_path, guide_entry_content in generated_entries.items():
            # Find corresponding result from current generation
            result = None
            for r in state.results:
                if r.success and str(r.file_path.relative_to(state.request.repo_path)) == relative_path:
                    result = r
                    break
            
            if result:
                # File was just generated in this run
                file_metadata = self.update_file_metadata(
                    relative_path, result, state, guide_entry_content
                )
                metadata.tracked_files[relative_path] = file_metadata
            else:
                # File has existing documentation but wasn't generated this run
                file_metadata = self.update_file_metadata_for_existing_doc(
                    relative_path, state, guide_entry_content
                )
                if file_metadata:
                    metadata.tracked_files[relative_path] = file_metadata
        
        # Remove metadata for deleted files
        if state.guide_change_set and state.guide_change_set.deleted_files:
            for deleted_file in state.guide_change_set.deleted_files:
                if deleted_file in metadata.tracked_files:
                    del metadata.tracked_files[deleted_file]
                    self.logger.debug(f"Removed metadata for deleted file: {deleted_file}")
        
        # Update guide metadata
        metadata.guide_last_generated = current_time
        metadata.guide_version += 1
        
        # Save updated metadata
        self.save_metadata(metadata)
        self.logger.info(f"Updated metadata for {len(generated_entries)} files")
    
    def update_file_metadata_for_existing_doc(self, 
                                            relative_path: str, 
                                            state: PipelineState,
                                            guide_entry_content: str) -> Optional[FileMetadata]:
        """Update metadata for a file that has existing documentation but wasn't generated this run.
        
        Args:
            relative_path: Relative path to source file
            state: Current pipeline state
            guide_entry_content: Content of the guide entry for this file
            
        Returns:
            Updated FileMetadata object or None if file not found
        """
        try:
            source_file = state.request.repo_path / relative_path
            doc_filename = f"{Path(relative_path).stem}_documentation.md"
            doc_relative_path = str(Path(relative_path).parent / doc_filename)
            doc_full_path = self.output_path / doc_relative_path
            
            if not doc_full_path.exists():
                self.logger.warning(f"Documentation file not found: {doc_full_path}")
                return None
            
            # Calculate hashes and timestamps
            source_mtime = source_file.stat().st_mtime if source_file.exists() else 0.0
            doc_hash = self._calculate_file_hash(doc_full_path)
            guide_entry_hash = self._calculate_string_hash(guide_entry_content)
            
            # For existing docs, use the doc file's modification time as doc_generated
            doc_mtime = doc_full_path.stat().st_mtime
            current_time = time.time()
            
            return FileMetadata(
                source_file_path=relative_path,
                source_file_modified=source_mtime,
                doc_file_path=doc_relative_path,
                doc_generated=doc_mtime,  # Use existing doc's timestamp
                doc_file_hash=doc_hash,
                guide_entry_generated=current_time,  # Guide entry generated now
                guide_entry_hash=guide_entry_hash
            )
            
        except Exception as e:
            self.logger.error(f"Failed to update metadata for existing doc {relative_path}: {e}")
            return None
    
    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA-256 hash of a file."""
        if not file_path.exists():
            return ""
        
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            return hashlib.sha256(content).hexdigest()
        except Exception as e:
            self.logger.error(f"Failed to calculate hash for {file_path}: {e}")
            return ""
    
    def _calculate_string_hash(self, content: str) -> str:
        """Calculate SHA-256 hash of a string."""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    def should_force_full_rebuild(self, changeset: ChangeSet) -> bool:
        """Determine if a full rebuild is needed based on changeset.
        
        Args:
            changeset: Detected changes
            
        Returns:
            True if full rebuild is recommended
        """
        if changeset.force_full_rebuild:
            return True
        
        # Force full rebuild if too many files changed (e.g., >50% of tracked files)
        total_changes = len(changeset.new_files) + len(changeset.modified_files) + len(changeset.deleted_files)
        metadata = self.load_metadata()
        
        if len(metadata.tracked_files) > 0:
            change_ratio = total_changes / len(metadata.tracked_files)
            if change_ratio > 0.5:  # More than 50% changed
                self.logger.info(f"Too many changes ({change_ratio:.1%}), forcing full rebuild")
                return True
        
        return False