<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for src\file_processor.py

# File: `src/file_processor.py`

## Purpose

This module (`file_processor.py`) is responsible for handling source code file processing in a documentation generation pipeline. Its primary responsibilities are:

- Detecting when documentation for a code file needs to be regenerated.
- Processing, saving, and organizing generated documentation files (including metadata and optional code snippets).
- Managing output directories and structure for generated documentation.
- Supporting the pipeline with efficient and robust file operations.

This file exists to encapsulate all logic specific to file-related tasks within the documentation generation process.

---

## Functionality

### Main Class: `FileProcessor`

This class serves as the main abstraction for file-related operations in the documentation pipeline. It is initialized with a configuration object and uses logging for diagnostics.

#### Key Methods

- **`should_generate_documentation(state, code_file, guide_generator) -> bool`**  
  Determines whether documentation should be (re)generated for a given file. It checks:
  - If the documentation for the file already exists.
  - If the file or its location has changed (using file hashing and metadata).
  - If necessary, triggers a regeneration of documentation.

- **`save_single_result(state, result)`**  
  Safely saves the documentation for a single file:
  - Writes header notices, the generated documentation body, optional original code, and a YAML footer with metadata.
  - Handles output directory creation and error catching.
  - Skips saving for unsuccessful or unchanged files for efficiency.

- **`calculate_file_hash(file_path) -> str`**  
  Computes the SHA-256 hash of a file, used for efficient change detection in determining whether to regenerate documentation.

- **`create_output_directory_structure(state)`**  
  Ensures that the necessary directory structure for storing documentation is present. Optionally also creates a "design_documentation" subfolder if requested by the pipeline state.

---

## Key Components

- **Class: `FileProcessor`**
  - Encapsulates all file-based logic for the documentation pipeline.
  - Uses logging for activity tracking and error reporting.
  - Accepts a configuration object upon construction.

- **Functions:**
  - `should_generate_documentation`: Core of change detection and regeneration necessity.
  - `save_single_result`: Handles all details of documentation file creation.
  - `calculate_file_hash`: Utility for SHA-256 hashing of files.
  - `create_output_directory_structure`: Ensures output path(s) exist.

- **Important Variables and Types:**
  - **`config`**: Configuration data, typically a dict or object, passed during initialization.
  - **`PipelineState`, `DocumentationResult`, `CodeFile`**: Data models imported from `.models`, represent the pipeline's current state, individual documentation outcome, and code files respectively.
  - **`logger`**: Logger instance for diagnostics.

---

## Dependencies

### Imports

- **Standard Library:**
  - `hashlib` (SHA-256 hashing)
  - `datetime` (Timestamping)
  - `pathlib.Path` (Filesystem paths)
  - `typing.Optional` (Type hinting)
  - `logging` (Event logging/diagnostics)
- **Local to project:**
  - `.models` with classes:
    - `PipelineState`
    - `DocumentationResult`
    - `CodeFile`

### External Access

- **Depends on:**  
  - The models defined in `.models`.
  - A `guide_generator` object with a method `extract_metadata_from_doc(doc_path)` (passed into `should_generate_documentation`).
  - A `config` object (structure expected: has an `output` dict key, including `include_code`).

- **Depended upon by:**  
  - The main documentation generation pipeline/process which uses file detection, output management, and persistence functionality.

---

## Usage Examples

### 1. **Typical Use in a Documentation Pipeline**

```python
from file_processor import FileProcessor
from models import PipelineState, DocumentationResult, CodeFile

# Assume config, state, code_file, and guide_generator objects are defined elsewhere

file_processor = FileProcessor(config)

# Check if documentation should be (re)generated based on file/entity state
if file_processor.should_generate_documentation(state, code_file, guide_generator):
    # ... generate documentation (using LLM or template)
    result = DocumentationResult(
        file_path=code_file.path,
        documentation=generated_markdown,
        success=True
    )
    file_processor.save_single_result(state, result)

# (before processing many files, create the output directory structure)
file_processor.create_output_directory_structure(state)
```

### 2. **Manual Hash Calculation Example**

```python
hash_str = file_processor.calculate_file_hash(Path("src/example.py"))
print("SHA-256:", hash_str)
```

---

## Additional Notes

- **Metadata Handling:**  
  Each generated documentation file is prefixed with auto-generation notices and suffixed with a YAML block containing (at minimum):
    - File hash
    - Relative path
    - Generation timestamp

- **Change Detection:**  
  Uses both the file content hash and file location to determine if regeneration is needed, supporting scenarios where files are renamed or moved.

- **Error Handling:**  
  Robust error catching and logging for saving output files; skips failed or unnecessary saves.

- **Configurable Output:**  
  Optionally embeds original code in the documentation markdown if enabled in config (`include_code`).

- **Design Documentation Support:**  
  If requested, a separate subdirectory for design documents is created alongside normal documentation output.

---

**End of file documentation.**

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: 911b4dd0937a8be81277064693c1f35484044e2ea1aad9a785355bc7d27f2aba
relative_path: src\file_processor.py
generation_date: 2025-07-01T22:14:01.781366
```
<!-- END GENERATION METADATA -->
