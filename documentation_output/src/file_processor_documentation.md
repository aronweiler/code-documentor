<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for src/file_processor.py

# file_processor.py

## Purpose

The `file_processor.py` module encapsulates the core logic for processing source code files in a documentation generation pipeline. It detects file changes, determines when to regenerate documentation, calculates file hashes for change detection, manages output directory structures, and handles the saving of generated documentation (including metadata and original code snippets).

This module is a crucial component for automated documentation systems, ensuring documentation is always in sync with the codebase and is only regenerated when necessary.

---

## Functionality

### Main Responsibilities

- **Change Detection:** Determines if a code file has changed and if its documentation needs regeneration.
- **Saving Results:** Writes generated documentation to disk in the appropriate structure, with standard headers, optionally including original code, and machine-readable metadata.
- **File Hashing:** Provides reliable and efficient hashing of files to check for changes without false positives.
- **Output Directories:** Ensures the necessary directory structure exists for saving documentation files and design documents.

---

## Key Components

### Classes

#### `FileProcessor`

Handles all file-related operations for the documentation pipeline. Key methods include:

- **`__init__(self, config)`**:  
  Stores configuration settings and sets up a logger.

- **`should_generate_documentation(self, state, code_file, guide_generator) -> bool`**:  
  Checks, using file hash comparison and metadata, whether documentation needs to be generated for a given source file.

- **`save_single_result(self, state, result)`**:  
  Saves a single `DocumentationResult` object as a documentation file, including headers, footers with metadata, and optionally the source code.

- **`calculate_file_hash(self, file_path: Path) -> str`**:  
  Computes the SHA-256 hash of a file efficiently in chunks.

- **`create_output_directory_structure(self, state)`**:  
  Creates the output directory tree, including optional `design_documentation` structure if required.

---

### Key Methods and Utilities

- **`should_generate_documentation(...)`**  
  - Compares the current hash and path of a code file with values stored in metadata of the previously generated documentation.
  - Returns `True` if documentation must be (re)generated, or `False` otherwise.
  - Uses the `guide_generator.extract_metadata_from_doc()` method to extract YAML metadata.

- **`save_single_result(...)`**  
  - Checks if a result is successful before saving.
  - Generates markdown documentation files, prepending a header and appending machine-parsable YAML metadata.
  - Tracks whether to include original code in the output based on configuration.
  - Manages all file operations and error handling for robustness.

- **`calculate_file_hash(...)`**  
  - Safely computes the hash of a file and returns `"unknown"` if the operation fails.

- **`create_output_directory_structure(...)`**  
  - Ensures the output directory tree exists before saving any documentation.

---

### Important Variables

- **`self.config`**  
  Configuration dictionary for output and formatting options.

- **`state`**  
  An object managing the pipeline's global state (see dependencies).

- **`result`**  
  An instance containing documentation generation results for a specific file.

---

## Dependencies

### External Modules

- **Standard Library:**
  - `hashlib` (file hashing)
  - `datetime` (timestamps)
  - `pathlib.Path` (file system operations)
  - `logging` (for debug and error output)
- **Internal Project Modules:**
  - `.models` containing:
    - `PipelineState` (pipeline runtime context)
    - `DocumentationResult` (individual documentation outcome)
    - `CodeFile` (represents a code file to process)

### What Depends on This

Other parts of the documentation pipeline will instantiate and use `FileProcessor` to:
- Determine if files require new documentation.
- Save results after running LLMs or other doc generators.
- Ensure output directories are created ahead of file writes.

---

## Usage Examples

### 1. Change Detection Before Generation

```python
from src.file_processor import FileProcessor
from src.models import PipelineState, CodeFile

processor = FileProcessor(config)
if processor.should_generate_documentation(state, code_file, guide_generator):
    # Generate documentation and then save
    result = ...  # obtain DocumentationResult for code_file
    processor.save_single_result(state, result)
```

### 2. Saving Documentation Result

```python
result = DocumentationResult(
    file_path=Path("src/example.py"),
    documentation="## Usage ...",
    success=True
)
processor.save_single_result(state, result)
```

### 3. Creating Output Directories

```python
processor.create_output_directory_structure(state)
```

---

## Notes

- Documentation files are saved as `<original_filename>_documentation.md` in a mirrored directory structure under the configured output directory.
- Each documentation file includes an auto-generation notice and a YAML metadata block identifying file hash, path, and generation date for robust change tracking.
- If `include_code` is set in the configuration, the original code is embedded beneath the generated documentation.
- `guide_generator` must implement an `extract_metadata_from_doc(path)` method to extract YAML blocks from documentation files.
- All file writes and directory operations are robust to I/O errors and failures are logged using the Python logging module.

---

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: 911b4dd0937a8be81277064693c1f35484044e2ea1aad9a785355bc7d27f2aba
relative_path: src/file_processor.py
generation_date: 2025-06-30T00:06:51.512876
```
<!-- END GENERATION METADATA -->
