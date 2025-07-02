<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for src\guide_metadata_manager.py

# guide_metadata_manager.py

## Purpose

This file implements the **GuideMetadataManager** class, which is responsible for tracking and managing metadata related to the incremental generation of documentation guides for a codebase. By detecting file changes, tracking documentation generation status, and efficiently persisting this information, it enables incremental doc generation—only regenerating guides or documentation files when necessary.

The manager also provides APIs to coordinate state between documentation runs and ensures metadata consistency across guide builds.

---

## Functionality

### Main Responsibilities

- **Metadata Persistence:** Loads and saves metadata about files and guides to disk, enabling incremental builds.
- **Change Detection:** Compares previous documentation state with the current state to identify new, modified, and deleted source files that require guide updates.
- **File Tracking:** Maintains metadata about each documented file, such as its modification time, documentation file location, content hashes, and generation times.
- **Guide Structure Updates:** Calculates hashes of guide entries and tracks when they were generated.

---

## Key Components

### Classes

#### `GuideMetadataManager`

The core class, which provides all metadata management functions required by the documentation generation pipeline.

##### Constructor

```python
def __init__(self, output_path: Path)
```
- **output_path**: Directory where documentation files and metadata are stored.

##### Methods

- **`load_metadata() -> GuideMetadata`**  
  Loads persisted guide metadata or initializes a new one if not found.

- **`save_metadata(metadata: GuideMetadata) -> None`**  
  Saves the provided metadata object to disk atomically to minimize the risk of corruption.

- **`detect_changes(state: PipelineState, current_results: List[DocumentationResult]) -> ChangeSet`**  
  Determines which source files are new, modified, or deleted since the last guide generation by comparing metadata and the current repo state.

- **`_discover_all_documentation_files(state: PipelineState) -> List[str]`**  
  Discovers all existing documentation files in the output directory and maps them to their corresponding source files.

- **`update_file_metadata(relative_path: str, result: DocumentationResult, state: PipelineState, guide_entry_content: str) -> FileMetadata`**  
  Updates and returns the metadata entry for an individual file, calculating all necessary hashes and timestamps.

- **`update_metadata_after_generation(state: PipelineState, generated_entries: Dict[str, str]) -> None`**  
  After a guide is generated, updates metadata for all affected files and persists the changes.

- **`update_file_metadata_for_existing_doc(relative_path: str, state: PipelineState, guide_entry_content: str) -> Optional[FileMetadata]`**  
  When a guide entry wasn't just generated (i.e., the documentation file already existed), updates its metadata using existing files.

- **`_calculate_file_hash(file_path: Path) -> str`**  
  Utility for calculating a SHA-256 hash of a file's content.

- **`_calculate_string_hash(content: str) -> str`**  
  Utility for calculating a SHA-256 hash of a string (e.g., a guide entry).

- **`should_force_full_rebuild(changeset: ChangeSet) -> bool`**  
  Decides if a full documentation rebuild is needed based on the number/proportion of changed files or special indicators in the changeset.


### Data Structures

The class relies extensively on dataclasses (imported from `.models`) to manage structured state:

- **GuideMetadata**: Tracks the last generation time, version, a map of tracked files, and a guide structure hash.
- **FileMetadata**: Captures all state about an individual documented file.
- **ChangeSet**: Lists of new, modified, and deleted files for incremental builds.
- **PipelineState**: Contains information about the user's request, configuration, and build results.
- **DocumentationResult**: Per-file result from the documentation process, including success flag, file paths, and output.


### Variables

- **`self.output_path`**: Output directory for documentation and metadata.
- **`self.metadata_dir`**: Hidden subdirectory for internal metadata storage.
- **`self.metadata_file`**: Path to the main guide metadata JSON file.
- **`self.logger`**: Logger for reporting informational and error messages.


---

## Dependencies

### Imports

- **Standard Library:**  
  - `json`, `hashlib`, `os`, `time`, `logging`, `pathlib.Path`
- **Type Hints:**  
  - `Dict`, `List`, `Optional`, `Tuple`
- **Internal Models:**  
  - `.models.FileMetadata`
  - `.models.GuideMetadata`
  - `.models.ChangeSet`
  - `.models.PipelineState`
  - `.models.DocumentationResult`

### Internal Interactions

- This file assumes it is used as a utility within a larger documentation generation system.
- It reads/writes metadata to `.documentation_state/guide_metadata.json` within the documentation output directory.
- GuideMetadataManager is intended to be used by the main documentation pipeline; no other file imports this manager directly in the source snippet.

---

## Usage Examples

### Basic Usage

```python
from pathlib import Path
from guide_metadata_manager import GuideMetadataManager
from .models import PipelineState, DocumentationResult

# Set up output directory
output_dir = Path("docs_output")

# Initialize the manager
manager = GuideMetadataManager(output_dir)

# Load previous metadata, if available
metadata = manager.load_metadata()

# After generating documentation:
change_set = manager.detect_changes(state, doc_results)

# To update all metadata after generation of the guide:
manager.update_metadata_after_generation(state, generated_entries)

# To determine if a full rebuild is needed:
if manager.should_force_full_rebuild(change_set):
    # Regenerate entire guide from scratch
    ...
```

### Incremental Build Logic (High-level)

```python
# 1. Initialize manager
manager = GuideMetadataManager(doc_output_path)

# 2. Detect what changed
changes = manager.detect_changes(current_state, doc_results)

# 3. If full rebuild is needed, trigger complete regeneration
if manager.should_force_full_rebuild(changes):
    rebuild_all_docs()
else:
    update_just_changed_docs(changes)

# 4. After guide and documentation files are generated/updated
manager.update_metadata_after_generation(current_state, generated_entries)
```

---

## Notes

- **Atomic Writes**: Metadata files are written atomically via a temp file and replace operation.
- **Incremental Optimization**: Only changed or deleted files are rebuilt; others leverage cached data for performance.
- **Extensibility**: Additional logic may be added to handle advanced file matching, handle custom extensions, or more complex guide structures.

---

## Summary

**`guide_metadata_manager.py`** is a central component for efficient and consistent generation of documentation guides in a code repository. It enables smart change detection and incremental builds, ensuring the documentation process is both fast and reliable for large projects.

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: 0fe104d428c31370a83bdd05c400ab522c3a72951be387154eb3b1421dc503f3
relative_path: src\guide_metadata_manager.py
generation_date: 2025-07-01T22:14:54.850299
```
<!-- END GENERATION METADATA -->
