<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for src\file_processor.py

# src/file_processor.py Documentation

## Purpose
`FileProcessor` orchestrates the detection of file changes and the generation and saving of documentation files in a repository. It is a core component in a documentation pipeline that:
- Determines whether a given source code file needs updated documentation.
- Writes auto-generated Markdown files with embedded metadata and optional source code snippets.
- Manages output directory creation and structure for generated docs.

---

## Functionality Overview
1. **Change Detection**  
   - `should_generate_documentation(...)`  
     Examines existing documentation metadata, computes new file hashes, and decides if regeneration is necessary.

2. **Documentation Saving**  
   - `save_single_result(...)`  
     Persists a `DocumentationResult` into a Markdown file. Includes header notices, the LLM-generated documentation, optional original code, and a machine-readable metadata footer.

3. **File Hashing**  
   - `calculate_file_hash(...)`  
     Computes a SHA-256 hash of a file’s contents in a streaming fashion.

4. **Directory Setup**  
   - `create_output_directory_structure(...)`  
     Ensures the target output directory (and optional subdirectories) exist before file writes.

---

## Key Components

### Class: FileProcessor
Constructor Signature:
```python
FileProcessor(config)
```
- **config**: A configuration object/dict.  
  - Expects at least `config.output`, a dict with an optional `"include_code"` boolean flag.

#### Methods

1. `should_generate_documentation(state: PipelineState, code_file: CodeFile, guide_generator) -> bool`  
   - **Purpose**: Avoids redundant regeneration by comparing the current file hash and path against metadata in existing docs.  
   - **Workflow**:
     - Builds the expected documentation path from `state.request.output_path` and `code_file.path`.
     - If no doc file exists or no metadata can be extracted, returns `True`.
     - Calculates SHA-256 of the source file.
     - Checks extracted metadata fields `file_hash` and `relative_path`.  
     - Returns `False` if both match; otherwise logs differences and returns `True`.

2. `save_single_result(state: PipelineState, result: DocumentationResult) -> None`  
   - **Purpose**: Writes out the documentation Markdown for a successful generation result, including metadata.  
   - **Behavior**:
     - Skips saving if `result.success` is `False` or if `result.documentation` indicates a skip.
     - Ensures output directories exist.
     - Computes file hash and generation timestamp.
     - Writes out:
       - An auto-generated warning header.
       - A title header referencing the source file.
       - `result.documentation` (LLM output).
       - Optionally, the original source code in a fenced code block if `config.output["include_code"]` is `True`.
       - A YAML-formatted metadata footer containing `file_hash`, `relative_path`, and `generation_date`.
     - Logs successes and errors.

3. `calculate_file_hash(file_path: Path) -> str`  
   - **Purpose**: Generates a SHA-256 digest of a file’s bytes.  
   - **Details**: Reads in 4 KB chunks; on error, returns `"unknown"` and prints a warning.

4. `create_output_directory_structure(state: PipelineState) -> None`  
   - **Purpose**: Prepares the main output folder and optional subfolders before any documentation files are written.  
   - **Details**:
     - Always creates `state.request.output_path`.
     - If `state.request.design_docs` is truthy, also creates `design_documentation/` under the output path.

---

## Dependencies

### Imports
- Standard Library
  - `hashlib` (SHA-256 hashing)
  - `datetime.datetime` (timestamping)
  - `pathlib.Path` (filesystem paths)
  - `logging` (internal logging)
- Typing
  - `Optional`
- Project Models (from `.models`)
  - `PipelineState`  
    Represents the documentation request, including repository path and output settings.
  - `DocumentationResult`  
    Encapsulates results of a single file’s documentation generation (e.g., success flag, content, file path).
  - `CodeFile`  
    Abstraction for a source file, with attributes like `.path`.

### External Interaction
- **guide_generator** (passed into `should_generate_documentation`)  
  Must implement:
  ```python
  extract_metadata_from_doc(doc_path: Path) -> Optional[Dict[str, str]]
  ```
  to parse existing documentation metadata.

### Dependents
- A higher-level pipeline manager that:
  1. Instantiates `FileProcessor`
  2. Iterates over source files (`CodeFile` instances)
  3. Invokes `should_generate_documentation(...)`
  4. Generates new docs via an LLM or other system
  5. Calls `save_single_result(...)`

---

## Usage Examples

```python
from pathlib import Path
import logging
from src.file_processor import FileProcessor
from src.models import PipelineState, DocumentationResult, CodeFile

# --- Setup ---
config = {
    "output": {
        "include_code": True
    }
}
processor = FileProcessor(config)
logging.basicConfig(level=logging.DEBUG)

# Create or verify output folders
state = PipelineState(
    request=SomeRequestObject(
        repo_path=Path("/home/user/myrepo"),
        output_path=Path("/home/user/myrepo/docs"),
        design_docs=False
    )
)
processor.create_output_directory_structure(state)

# Example code file representation
code_file = CodeFile(path=Path("/home/user/myrepo/src/my_module.py"))

# Decide if we need to regen docs
if processor.should_generate_documentation(state, code_file, guide_generator):
    # Suppose generate_documentation returns a DocumentationResult
    result = generate_documentation(code_file)  
    # Save the new docs
    processor.save_single_result(state, result)
else:
    print("Skipping unchanged file:", code_file.path)
```

In a real pipeline, `generate_documentation` would invoke a language model or other doc-gen logic and return a `DocumentationResult` object containing:
- `file_path`: the same path as `code_file.path`
- `success`: boolean
- `documentation`: the Markdown content string

---

End of Documentation for `src/file_processor.py`

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: 911b4dd0937a8be81277064693c1f35484044e2ea1aad9a785355bc7d27f2aba
relative_path: src\file_processor.py
generation_date: 2025-06-10T22:38:01.204461
```
<!-- END GENERATION METADATA -->
