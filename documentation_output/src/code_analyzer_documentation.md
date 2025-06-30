<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for src\code_analyzer.py

# code_analyzer.py

## Purpose

This module provides functionality for analyzing code repositories, primarily for the purpose of preparing source files for automated documentation generation. It is responsible for scanning a given repository, filtering and extracting relevant code files according to configurable parameters, and analyzing overall file structure to supply context useful for documentation tools.

---

## Functionality

### Main Class: `CodeAnalyzer`

The `CodeAnalyzer` class is the core of this module, offering the following capabilities:

- **Repository Scanning**: Traverses a codebase recursively to locate files relevant for documentation.
- **File Filtering**: Selects files by extension and path, supporting exclusion patterns and empty-file skipping.
- **File Reading**: Robustly reads file contents using multiple encoding fallbacks.
- **Structure Analysis**: Aggregates statistics about the codebase, such as files by extension, by directory, and the largest files.

#### Initialization

```python
def __init__(self, config: PipelineConfig):
    self.config = config
```

Creates an analyzer instance with a provided configuration, typically specifying file types to include/exclude.

#### scan_repository

```python
def scan_repository(self, repo_path: Path) -> List[CodeFile]:
```
- **Purpose**: Scans `repo_path` for source files of interest.
- **Returns**: List of `CodeFile` objects, sorted by their relative path.
- **Logic**:
  - Reads supported extensions and exclude patterns from configuration.
  - Recursively traverses all files (non-directory) beneath `repo_path`.
  - Checks each file via `_should_include_file`.
  - Reads included files' content and wraps them as `CodeFile` instances.

#### _should_include_file

```python
def _should_include_file(self, file_path: Path, supported_extensions: List[str], exclude_patterns: List[str]) -> bool:
```
- **Purpose**: Central logic for file inclusion/exclusion.
- **Checks**:
  - File is accessible and is a regular file.
  - Extension is in supported list (if provided).
  - Path does not match any exclude pattern.
  - File is not empty.

#### _read_code_file

```python
def _read_code_file(self, file_path: Path) -> str:
```
- **Purpose**: Reads a file with robustness to encoding issues.
- **Approach**:
  - Tries several common encodings (`utf-8`, `utf-16`, `cp1252`, `iso-8859-1`) in sequence.
  - As a fallback, reads raw bytes and decodes with utf-8, ignoring errors.

#### analyze_file_structure

```python
def analyze_file_structure(self, code_files: List[CodeFile]) -> dict:
```
- **Purpose**: Produces an overall structure summary of scanned code files.
- **Returns**: Dictionary with:
  - `total_files`: Count of files found.
  - `by_extension`: Frequency of files per extension.
  - `by_directory`: Frequency of files per directory.
  - `largest_files`: The 10 largest files (by content length), as tuples of `(relative_path, size)`.

---

## Key Components

### Classes & Types

- **`CodeAnalyzer`**: Main class performing scanning, file selection, content reading, and structure analysis.
- **`CodeFile`** (`from .models`): Dataclass or model representing a code file's path, content, extension, and relative path.
- **`PipelineConfig`** (`from .models`): Configuration object specifying how files should be processed (e.g., supported extensions, exclude patterns).

### Configuration

Expects `PipelineConfig` to supply at least:
- `file_processing['supported_extensions']`: List of file suffixes to include.
- `file_processing['exclude_patterns']`: List of path substrings to filter out.

---

## Dependencies

### Imports

- `os`, `pathlib.Path`: Filesystem traversal and manipulation.
- `typing.List`: Type hinting for collections.
- `.models.CodeFile`, `.models.PipelineConfig`: Local project models for representing code files and pipeline configuration.

### What Depends on This

- Any component of the documentation pipeline needing to enumerate or analyze files in a source repository.
- Documentation generation or processing logic that requires input as `CodeFile` objects.

---

## Usage Examples

### Basic Usage

```python
from pathlib import Path
from src.code_analyzer import CodeAnalyzer
from src.models import PipelineConfig

config = PipelineConfig(
    file_processing={
        'supported_extensions': ['.py', '.js'],
        'exclude_patterns': ['test/', 'migrations/']
    }
)

analyzer = CodeAnalyzer(config)
repo_path = Path('/path/to/repository')

# Scan repository for code files
code_files = analyzer.scan_repository(repo_path)

# Analyze file structure
structure = analyzer.analyze_file_structure(code_files)

print(f"Total code files: {structure['total_files']}")
print("Files by extension:", structure['by_extension'])
print("Largest files:", structure['largest_files'])
```

---

## Notes

- Expects the repository path to exist and be a directory; otherwise, it raises a `ValueError`.
- Warnings (via `print`) are emitted if files cannot be read, but scanning continues.
- Encodings are tried sequentially to maximize successful reading of source files.

---

## Summary

`code_analyzer.py` is a utility module designed to robustly scan code repositories for files to document, implementing configurable filtering, content retrieval, and structure analysis. It forms an essential component in an automated documentation or analysis pipeline for codebases.

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: f8bdbfd26916ff0c37fce9ace6f6952fd5c870503b1cb9b8474b94f4d7810839
relative_path: src\code_analyzer.py
generation_date: 2025-06-29T16:51:13.270561
```
<!-- END GENERATION METADATA -->
