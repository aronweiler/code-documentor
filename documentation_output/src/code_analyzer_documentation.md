<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for src\code_analyzer.py

# src\code_analyzer.py

## Purpose

The `code_analyzer.py` module provides the core logic for scanning source code repositories and extracting information about code files relevant for documentation generation. Its main purpose is to identify, filter, and analyze code files in a repository based on configurable parameters (such as file extensions and exclude patterns) to support automated documentation workflows.

This module is integral to the documentation toolkit, as it creates structured metadata about code files which downstream processes (such as documentation generators or analyzers) rely upon.

---

## Functionality

### Main Class: `CodeAnalyzer`

#### Overview

`CodeAnalyzer` is a high-level utility class designed to:

- Recursively scan a repository directory tree
- Identify code files for documentation, applying inclusion/exclusion criteria
- Read file contents in a robust and encoding-agnostic manner
- Produce structured summaries and statistics about the codebase (file count, distribution, largest files, etc.)

#### Initialization

```python
def __init__(self, config: PipelineConfig):
```
- Accepts a `PipelineConfig` object which contains configuration options, especially under `file_processing`, dictating which files to include/exclude.

#### Main Methods

##### 1. `scan_repository(self, repo_path: Path) -> List[CodeFile]`

- **Purpose:**  
  Traverse the given repository path recursively, collecting all code files that should be documented according to the configuration.
- **Key Features:**  
  - Filters files by supported extensions.
  - Ignores files matching exclude patterns.
  - Skips directories, inaccessible, or empty files.
  - Reads file contents using multiple encodings and handles errors gracefully.
  - Returns a sorted list of `CodeFile` objects, with metadata.

##### 2. `_should_include_file(self, file_path: Path, supported_extensions: List[str], exclude_patterns: List[str]) -> bool`

- **Purpose:**  
  Determines whether a given file should be considered for documentation, based on extension filtering, exclude patterns, existence, file type, and file size.
- **Details:**  
  Returns `True` if the file is a non-empty, accessible, non-directory file with an accepted extension and not excluded by any patterns.

##### 3. `_read_code_file(self, file_path: Path) -> str`

- **Purpose:**  
  Attempts to robustly read the contents of a file, trying several common encodings before falling back to binary mode and ignoring unreadable characters.
- **Details:**  
  Prevents the process from halting due to encoding issues.

##### 4. `analyze_file_structure(self, code_files: List[CodeFile]) -> dict`

- **Purpose:**  
  Given a list of `CodeFile` objects, compute summary statistics about the codebase: total files, counts by extension, counts by directory, and the 10 largest files by content length.

---

## Key Components

- **`CodeAnalyzer`**: The central class for directory scanning and analysis.
- **`scan_repository`**: Main function to gather code files for documentation.
- **`_should_include_file`**: Helper for determining inclusion/exclusion of files.
- **`_read_code_file`**: Robust file reader with encoding fallback logic.
- **`analyze_file_structure`**: Generates a breakdown of the codebase's file structure.
- **`PipelineConfig`** (from `.models`): Supplies configuration for file inclusion/exclusion.
- **`CodeFile`** (from `.models`): Represents a code file record (including path, contents, metadata).
- **Dependencies**
  - `os`
  - `Path` from `pathlib`
  - `List` from `typing`
  - Custom models: `CodeFile`, `PipelineConfig` (imported from `.models`)

---

## Dependencies

- **External Modules:**
  - `os`, `pathlib.Path`, `typing.List`
- **Project Modules:**
  - `.models`:
     - **`CodeFile`**  
       Data structure representing a source code file with attributes: path, content, extension, relative_path.
     - **`PipelineConfig`**  
       Configuration data class with a `.file_processing` dict that must at least contain:
         - `'supported_extensions'`: only files with these extensions are considered.
         - `'exclude_patterns'`: substring patterns in paths to be ignored.

- **Downstream Dependents:**  
  Other documentation tools and the generation pipeline depend on the outputs of `CodeAnalyzer.scan_repository`.

---

## Usage Examples

### Example 1: Basic Repository Scan

```python
from src.code_analyzer import CodeAnalyzer
from src.models import PipelineConfig

from pathlib import Path

# Prepare configuration
config = PipelineConfig(
    file_processing={
        "supported_extensions": [".py", ".js"],
        "exclude_patterns": ["test_", "__pycache__"]
    }
)

# Instantiate analyzer
analyzer = CodeAnalyzer(config)

# Scan repository for code files
repo_path = Path("/path/to/your/repository")
code_files = analyzer.scan_repository(repo_path)

print(f"Found {len(code_files)} code files to document.")
```

### Example 2: Analyzing File Structure

```python
# After scanning the repository with analyzer.scan_repository(...)
structure = analyzer.analyze_file_structure(code_files)
print("By extension:", structure["by_extension"])
print("By directory:", structure["by_directory"])
print("Largest files:", structure["largest_files"])
```

---

## Additional Notes

- **File Inclusion Logic:**  
  The `CodeAnalyzer` expects the configuration to drive what is included; no hard-coded file types—this makes it adaptable to diverse codebases.
- **Robustness:**  
  The analyzer is resilient to unreadable files, permission issues, and encoding errors. It logs warnings rather than failing.
- **Sorting:**  
  The final list of `CodeFile` records is sorted by relative path for consistency and predictable processing.

---

## Summary Table

| Component         | Description                                                                    |
|-------------------|--------------------------------------------------------------------------------|
| `CodeAnalyzer`    | Scans repos, finds & reads code files for documentation                        |
| `scan_repository` | Recursively locates files through filtering rules, returns `CodeFile`s         |
| `_should_include_file` | Evaluates if a file is eligible (extension, patterns, size, etc.)         |
| `_read_code_file` | Reads file with various encodings, robust to encoding issues                   |
| `analyze_file_structure` | Summarizes code file stats by extension, directory, largest files       |
| `PipelineConfig`  | Supplies which files to process, based on extensions and exclude patterns      |
| `CodeFile`        | Stores code file metadata and content                                          |

---

**This file is a central building block for the documentation workflow, responsible for accurate and robust codebase scanning and analysis to enable reliable downstream documentation generation.**

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: f8bdbfd26916ff0c37fce9ace6f6952fd5c870503b1cb9b8474b94f4d7810839
relative_path: src\code_analyzer.py
generation_date: 2025-07-01T23:05:02.639720
```
<!-- END GENERATION METADATA -->
