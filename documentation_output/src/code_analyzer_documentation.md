<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for src/code_analyzer.py

# code_analyzer.py

## Purpose

`code_analyzer.py` provides core functionality for analyzing the structure of code repositories. Its main job is to identify, read, and prepare code files for further processes such as automated documentation generation. It discovers which files should be included based on configuration (supported extensions and patterns to exclude), reads file contents robustly (handling encoding issues), and summarizes codebase structure to support downstream documentation or analysis tasks.

---

## Functionality

### Main Class: `CodeAnalyzer`

This class is responsible for:

- Scanning a repository directory, identifying files that meet configuration criteria,
- Reading and encapsulating code files for further processing,
- Analyzing and summarizing the codebase's structure for reporting or documentation augmentation.

#### `__init__(self, config: PipelineConfig)`
- Initializes the analyzer with a `PipelineConfig` instance, which determines what kinds of files to include or exclude (by extension and pattern).

#### `scan_repository(self, repo_path: Path) -> List[CodeFile]`
- Scans the target repository path recursively.
- Collects file paths matching criteria defined in configuration:
  - Supported file extensions (e.g., `.py`, `.js`)
  - Exclude patterns (strings to omit specific files or directories)
  - Non-empty and accessible files only
- Reads content robustly from each included file.
- Returns a sorted list of `CodeFile` objects with standardized relative paths.

#### `_should_include_file(self, file_path: Path, supported_extensions: List[str], exclude_patterns: List[str]) -> bool`
- Checks whether each file is:
  - Accessible and a regular file (not directory, not symlink)
  - Has an allowed extension
  - Does not match any of the excluded patterns
  - Is not empty
- Returns `True` if all checks pass.

#### `_read_code_file(self, file_path: Path) -> str`
- Reads file contents using a prioritized list of encodings. Attempts:
  1. `'utf-8'`
  2. `'utf-16'`
  3. `'cp1252'`
  4. `'iso-8859-1'`
- If all fail, reads as binary and decodes with utf-8, ignoring undecodable bytes.
- Ensures robust reading even if encoding isn't standard.

#### `analyze_file_structure(self, code_files: List[CodeFile]) -> dict`
- Receives a list of `CodeFile` objects.
- Produces a summary including:
  - Total number of files,
  - Count of files by extension,
  - Count of files by (relative) directory,
  - The 10 largest files (by content length).
- Returns the summary as a nested Python `dict`.

---

## Key Components

- **Class `CodeAnalyzer`**: Main utility for scanning, filtering, reading, and summarizing files.
- **Type `CodeFile` (imported)**: Data structure (likely a data class) holding path, content, extension, and relative path of code files.
- **Type `PipelineConfig` (imported)**: Holds configuration options, notably:
    - `file_processing["supported_extensions"]`
    - `file_processing["exclude_patterns"]`

#### Important Methods
- `scan_repository()`: Entry point for scanning codebase.
- `analyze_file_structure()`: Entry point for generating file summary statistics.

---

## Dependencies

### Direct Imports
- **Python Standard Library**:  
  - `os`: Possibly used out of habit, but not directly referenced—could be omitted.
  - `typing`: For type hints.
  - `pathlib`: For path and filesystem manipulation.
- **Local module**:  
  - `.models`: Provides `CodeFile` and `PipelineConfig`.

### External Dependencies
- This file depends on the correct definition of `CodeFile` and `PipelineConfig` in `.models`.

### Used By
- Any pipeline or tool that needs to analyze source repositories for documentation (or gather statistics for reporting).

---

## Usage Examples

### 1. Scanning a Code Repository

```python
from pathlib import Path
from src.code_analyzer import CodeAnalyzer
from src.models import PipelineConfig  # Make sure to provide correct config and paths

# Example config setup
config = PipelineConfig(
    file_processing={
        "supported_extensions": [".py", ".js"],
        "exclude_patterns": ["test", "__pycache__"]
    }
)

analyzer = CodeAnalyzer(config)
repo_path = Path("/path/to/repository")
code_files = analyzer.scan_repository(repo_path)

for cf in code_files:
    print(cf.relative_path, len(cf.content))
```

### 2. Analyzing File Structure

```python
structure_summary = analyzer.analyze_file_structure(code_files)
print("Total files:", structure_summary["total_files"])
print("Files by extension:", structure_summary["by_extension"])
print("Largest files:", structure_summary["largest_files"])
```

---

## Notes

- Printed warnings are generated for files that cannot be read (e.g., permission errors, decoding issues). These do not halt the scanning process.
- Encodings are attempted in a failover manner for robust file reading, making this tool suitable for codebases with mixed encoding.
- Files are reported by relative path (to the scanned root), allowing for intuitive linking in documentation outputs.

---

## Summary

`code_analyzer.py` encapsulates the core logic for discovering, reading, and analyzing the structure of code files in a repository. With configuration-driven inclusion/exclusion, robust file reading, and analytical summaries, it is suited for automated documentation pipelines or repository analytics tools.

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: f8bdbfd26916ff0c37fce9ace6f6952fd5c870503b1cb9b8474b94f4d7810839
relative_path: src/code_analyzer.py
generation_date: 2025-06-30T00:04:24.761468
```
<!-- END GENERATION METADATA -->
