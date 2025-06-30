<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for src/guide_metadata_manager.py

# guide_metadata_manager.py

## Purpose

This file provides the `GuideMetadataManager` class, responsible for tracking and managing metadata associated with incremental documentation and guide generation for source code repositories. It enables efficient change detection (new, modified, or deleted files) and supports incremental rather than full documentation regeneration, optimizing the documentation workflow.

## Functionality

The core responsibilities of the `GuideMetadataManager` include:
- Maintaining up-to-date metadata about source files, generated documentation, and guide entries.
- Detecting changes to inform incremental or full rebuilds of documentation or guides.
- Providing serialization/deserialization logic for reading and writing metadata to disk.
- Supporting functions for efficiently updating and synchronizing the metadata after documentation generation.

This manager is designed to work inside an automated documentation pipeline, keeping track of which files need (re)generation to avoid unnecessary work.

## Key Components

### 1. Classes

#### `GuideMetadataManager`
The central class handling metadata lifecycle, including creation, update, change detection, and persistence.

**Key Methods:**
- `__init__(self, output_path: Path)`
  - Sets up paths and logging, prepares storage directory.
- `load_metadata(self) -> GuideMetadata`
  - Loads guide metadata from disk, or initializes new metadata if not found.
- `save_metadata(self, metadata: GuideMetadata) -> None`
  - Serializes and saves the current metadata state to disk atomically.
- `detect_changes(self, state: PipelineState, current_results: List[DocumentationResult]) -> ChangeSet`
  - Compares current files and docs to metadata, returns a `ChangeSet` with new/modified/deleted files, and flags if a full rebuild is needed.
- `_discover_all_documentation_files(self, state: PipelineState) -> List[str]`
  - Scans for all documentation files and infers corresponding source files.
- `update_file_metadata(self, relative_path, result, state, guide_entry_content) -> FileMetadata`
  - Computes new `FileMetadata` for a given source file.
- `update_metadata_after_generation(self, state, generated_entries)`
  - Updates guide metadata after completion of documentation generation, also removing metadata for deleted files.
- `update_file_metadata_for_existing_doc(self, relative_path, state, guide_entry_content) -> Optional[FileMetadata]`
  - Updates `FileMetadata` for a documentation file that was not regenerated in the latest run.
- `_calculate_file_hash(self, file_path: Path) -> str`
  - Returns SHA-256 hash for the file contents.
- `_calculate_string_hash(self, content: str) -> str`
  - Returns SHA-256 hash of a string (used for guide entry content).
- `should_force_full_rebuild(self, changeset: ChangeSet) -> bool`
  - Determines if a full documentation rebuild should occur based on change counts or special conditions.

### 2. Data Classes and Structures

These are imported from `.models`:
- `FileMetadata`: Stores metadata for each single tracked file.
- `GuideMetadata`: Aggregates state across all tracked files, and global info (version, structure hash, etc.).
- `ChangeSet`: Encapsulates lists of new, modified, deleted files and flags if a full rebuild is needed.
- `PipelineState`: Contains state for the current documentation pipeline execution.
- `DocumentationResult`: Describes the result of attempting to generate documentation for a file.

### 3. Notable Variables

- `self.output_path`: Root of generated documentation.
- `self.metadata_dir`, `self.metadata_file`: Subdirectory and file for storing metadata.
- `self.logger`: Logger scoped to this module for all internal logs.

## Dependencies

### Internal Dependencies

- `.models`
  - Implicitly depends on data classes for `FileMetadata`, `GuideMetadata`, `ChangeSet`, `PipelineState`, and `DocumentationResult`.
- Assumes `state` and various `PipelineState` members conform to the overall pipeline API.

### External/Standard Library

- `json`, `hashlib`, `os`, `time`, `logging`
- `pathlib.Path`
- `typing` (for type annotations)

### What Depends on This

- The main documentation generation pipeline, which will:
  - Use this class to load/update metadata and to detect what files require documentation/guide (re)generation.
  - Use detected `ChangeSet` to determine incremental vs. full guide/documentation builds.

## Usage Examples

### Basic: Detecting and Processing Changes

```python
from pathlib import Path
from src.guide_metadata_manager import GuideMetadataManager
# ...import models as needed

output_path = Path('docs/')
manager = GuideMetadataManager(output_path)

# Assuming pipeline_state and results have been computed earlier
changeset = manager.detect_changes(pipeline_state, documentation_results)

if manager.should_force_full_rebuild(changeset):
    # trigger full regeneration of documentation/guide
    pass
else:
    # perform incremental documentation/guide updates
    pass
```

### After Documentation Generation

```python
# After generating documentation entries
generated_entries = {
    # relative_path: guide_entry_content,
    'src/module.py': 'Guide entry content here',
}
manager.update_metadata_after_generation(pipeline_state, generated_entries)
```

### Manual Metadata Inspection

```python
metadata = manager.load_metadata()
for relpath, filemeta in metadata.tracked_files.items():
    print(f"{relpath}: last modified {filemeta.source_file_modified}")
```

## Additional Notes

- The metadata state is kept in `output_path/.documentation_state/guide_metadata.json`.
- The logic is robust to first runs, missing files, or major structural changes.
- All writes to the metadata file are atomic to avoid corruption.
- Logging is employed at all significant events for easy tracing/debugging.
- Changing >50% of tracked files triggers a full rebuild recommendation.
- The file supports flexible configuration for source code extensions and expects integration with a broader documentation pipeline system.

---

**This file is foundational to robust, incremental, and scalable documentation pipelines, enabling selective and efficient guide/documentation regeneration across large codebases.**

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: 0fe104d428c31370a83bdd05c400ab522c3a72951be387154eb3b1421dc503f3
relative_path: src/guide_metadata_manager.py
generation_date: 2025-06-30T00:07:47.110209
```
<!-- END GENERATION METADATA -->
