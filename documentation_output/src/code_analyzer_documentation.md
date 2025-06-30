<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for src\code_analyzer.py

# code_analyzer.py

## Purpose

The `code_analyzer.py` module provides core logic for scanning, analyzing, and filtering code files within a repository. Its primary goal is to automate the identification and extraction of source code files that should be included in documentation workflows. This file is typically used as part of a documentation or code analysis pipeline to build an overview of a codebase's structure and contents.

---

## Functionality

### Main Class: `CodeAnalyzer`

The `CodeAnalyzer` class encapsulates all the logic needed to:

- **Recursively scan repositories:** Identify and select code files based on configurable criteria (such as allowed file extensions and exclude patterns).
- **Read file contents:** Load file contents using various fallbacks for character encoding.
- **Analyze file sets:** Generate structural data about the codebase (file counts per extension or directory, largest files, etc.) to inform documentation or analytics.

---

## Key Components

### Dependencies

- **Standard Library:**
  - `os`
  - `pathlib.Path`
  - `typing.List`
- **Project Dependencies:**
  - `.models`:
    - `CodeFile` – Represents a code file with metadata (path, content, extension, relative path).
    - `PipelineConfig` – Configuration object containing at least `file_processing` attribute for file filtering.

### Important Elements

#### Class: `CodeAnalyzer`

- **`__init__(self, config: PipelineConfig)`**
  
  Initializes the analyzer with a user-supplied configuration object (`PipelineConfig`), which controls file scanning and filtering behavior (extensions, exclusion patterns).

- **`scan_repository(self, repo_path: Path) -> List[CodeFile]`**
  
  Recursively scans a repository directory for code files, applying include/exclude rules, and returns a sorted list of `CodeFile` objects. Handles unreadable files gracefully by logging warnings.

- **`_should_include_file(self, file_path: Path, supported_extensions: List[str], exclude_patterns: List[str]) -> bool`**
  
  Determines if a file should be processed for documentation:
  
  - Checks if the path exists and is a file.
  - Verifies that the file extension is allowed.
  - Skips files matching any of the exclude patterns.
  - Ignores empty files.

- **`_read_code_file(self, file_path: Path) -> str`**
  
  Attempts to read the contents of a file using multiple common encodings (`utf-8`, `utf-16`, `cp1252`, `iso-8859-1`). If those fail, it reads in binary mode with error-tolerant decoding.

- **`analyze_file_structure(self, code_files: List[CodeFile]) -> dict`**
  
  Generates and returns an analysis of the codebase, containing:
  
  - `total_files`: Number of code files detected.
  - `by_extension`: Counts grouped by file extension.
  - `by_directory`: Counts grouped by directory.
  - `largest_files`: List of up to 10 largest files by content length.

---

## Dependencies

### Required by This File

- **`.models` module**:
  - `CodeFile`
  - `PipelineConfig`
  
  These are critical for storing code file metadata and for passing configuration about what files to process.

### Depends On

This file depends on:

- Configuration objects (`PipelineConfig`) to control its behavior.
- The models (`CodeFile`) for passing code file data downstream in the documentation or analysis pipeline.

No other specific details on what depends on this file are given, but it is intended to be used as part of a larger code documentation or analysis pipeline.

---

## Usage Examples

```python
from pathlib import Path
from src.code_analyzer import CodeAnalyzer
from src.models import PipelineConfig

# Sample configuration
config = PipelineConfig(
    file_processing={
        "supported_extensions": [".py", ".js", ".ts"],
        "exclude_patterns": ["test", "migrations"]
    }
)

analyzer = CodeAnalyzer(config=config)

# Scan repository for code files
repo_path = Path("/path/to/your/repository")
code_files = analyzer.scan_repository(repo_path)

# Print summary of analyzed file structure
structure = analyzer.analyze_file_structure(code_files)
print("File structure summary:")
print(structure)

# Example: Print all Python file relative paths
for cf in code_files:
    if cf.extension == ".py":
        print(cf.relative_path)
```

---

## Summary

This module is designed to locate, retrieve, and analyze code files within a repository for documentation purposes. Its flexible configuration and robust scanning logic make it useful as a foundational component in automated documentation systems or codebase analytics pipelines.

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: f8bdbfd26916ff0c37fce9ace6f6952fd5c870503b1cb9b8474b94f4d7810839
relative_path: src\code_analyzer.py
generation_date: 2025-06-30T14:14:10.342335
```
<!-- END GENERATION METADATA -->
