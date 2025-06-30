<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for src\guide_metadata_manager.py

# guide_metadata_manager.py

## Purpose

The `guide_metadata_manager.py` file provides an API for managing and tracking metadata related to incremental guide (documentation) generation in a codebase. Its primary function is to ensure efficient, consistent, and correct updates to both per-file documentation and the overall documentation guide by detecting changes, updating tracking records, handling metadata persistence, and facilitating incremental rebuilds only as needed.

This component supports:  
- Faster generation of documentation by avoiding unnecessary rewrites  
- Accurate detection of when source files or documentation files change  
- Robustness against data corruption and deleted/moved files  
- Automatic management of guide versioning and timestamping

---

## Functionality

The central class, `GuideMetadataManager`, encapsulates all logic for loading, saving, updating, and synchronizing guide-related metadata with the actual state of source code and generated documentation. This includes:

- Loading existing metadata or initializing new metadata for fresh runs
- Saving changes atomically to prevent state corruption
- Detecting changes (new, modified, deleted files) since the last run
- Updating metadata after a successful documentation generation
- Determining if a full guide rebuild is required
- Hashing content/files to check for actual changes
- Discovering all documented files, even if metadata went missing

All API methods are designed for integration with a larger documentation pipeline (as suggested by references to objects like `PipelineState` and `DocumentationResult`).

---

## Key Components

### Classes

#### `GuideMetadataManager`
- **Constructor**
  - `__init__(self, output_path: Path)`
    - Initializes the manager, sets up metadata directory, and ensures its existence.

- **Metadata Persistence**
  - `load_metadata(self) -> GuideMetadata`
    - Loads metadata from disk or creates a new record if not available or corrupted.
  - `save_metadata(self, metadata: GuideMetadata) -> None`
    - Writes metadata to disk with atomic file replacement for data integrity.

- **Change Detection**
  - `detect_changes(self, state: PipelineState, current_results: List[DocumentationResult]) -> ChangeSet`
    - Analyzes current source/doc state against stored metadata and returns a `ChangeSet` summarizing new, modified, and deleted files.

- **Discovering Documentation**
  - `_discover_all_documentation_files(self, state: PipelineState) -> List[str]`
    - Scans output directory, deduces which source files have documentation even if metadata is inconsistent.

- **Metadata Update**
  - `update_file_metadata(...) -> FileMetadata`
    - Populates a `FileMetadata` instance for a newly generated or updated doc/result.
  - `update_metadata_after_generation(...) -> None`
    - Applies changes to the persisted metadata after guide (re-)generation finishes.
  - `update_file_metadata_for_existing_doc(...) -> Optional[FileMetadata]`
    - Regenerates metadata for doc files not touched in the current run, using file properties and provided content.

- **Hashing Helpers**
  - `_calculate_file_hash(self, file_path: Path) -> str`
    - SHA-256 hash for files, for fast change detection.
  - `_calculate_string_hash(self, content: str) -> str`
    - SHA-256 hashes of in-memory guide entries.

- **Rebuild Policy**
  - `should_force_full_rebuild(self, changeset: ChangeSet) -> bool`
    - Decides if a full rebuild is warranted (either by flag or by high ratio of changes).

### Data Structures (from `.models`)

- `FileMetadata`: Tracks metadata for an individual file (source and doc).
- `GuideMetadata`: Global guide state including all tracked file metadata.
- `ChangeSet`: Lists new, modified, deleted files plus a force rebuild flag.
- `PipelineState`, `DocumentationResult`: Represent state/results of doc pipeline.

### Key Variables

- `self.metadata_dir`, `self.metadata_file`: Disk location for persistence layer.
- `self.logger`: Logging for debugging and audit.

---

## Dependencies

### External Modules

- `json`: For metadata serialization.
- `hashlib`: SHA-256 hashing.
- `os`, `pathlib.Path`, `time`: Filesystem and time operations.
- `logging`: For internal logs.

### Internal/Local

- `.models`: Imports all data model/dataclass entities (`FileMetadata`, etc.) used for metadata representation and change tracking.

### Usage Context

- **Depends on**: The output directory for documentation, a consistent `.models` file for data structures used across the pipeline, and pipeline invocation via `PipelineState` and related classes.
- **Consumed by**: The documentation build process – typically called during stepwise doc generation and guide reassembly.

---

## Usage Examples

### Basic: Initialize Manager and Load Metadata

```python
from pathlib import Path
from src.guide_metadata_manager import GuideMetadataManager

output_path = Path("docs")
manager = GuideMetadataManager(output_path)
metadata = manager.load_metadata()
```

### Detect Changes and Decide If Rebuild Is Needed

```python
state = PipelineState(...)  # prepare pipeline state
current_results = [...]     # list of DocumentationResult objects

changeset = manager.detect_changes(state, current_results)
if manager.should_force_full_rebuild(changeset):
    print("Full documentation guide rebuild required.")
else:
    print(f"Partial update: {changeset}")
```

### Update Per-file Metadata After Documentation Generation

```python
generated_entries = {
    "src/module.py": "Guide entry for module.py...",
    # ...
}
manager.update_metadata_after_generation(state, generated_entries)
```

### Hashing a File

```python
hash_str = manager._calculate_file_hash(Path("docs/src/module_documentation.md"))
```

---

## Additional Notes

- **First Run:** If no metadata file exists, the manager will create new metadata and force a full rebuild.
- **Robustness:** The manager handles partial or missing metadata gracefully, rebuilding/re-syncing as needed.
- **Supported Extensions:** Discovered doc/source mapping supports arbitrary file extensions as configured.
- **Concurrency:** Metadata writes use atomic replacement to avoid partial writes/corruption.
- **Logging:** All major actions, errors, and change detections are logged.
- **Integration:** This class is meant to be used solely from within a documentation/build system pipeline, not as a general-purpose metadata manager.

---

**See also:**  
- `.models` for the definitions of `FileMetadata`, `GuideMetadata`, and associated types used throughout this manager.  
- The main pipeline entrypoint for where/how `GuideMetadataManager` is invoked.

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: 0fe104d428c31370a83bdd05c400ab522c3a72951be387154eb3b1421dc503f3
relative_path: src\guide_metadata_manager.py
generation_date: 2025-06-29T16:52:23.123083
```
<!-- END GENERATION METADATA -->
