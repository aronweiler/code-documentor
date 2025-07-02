<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for src\tools\file_tools.py

# `file_tools.py`

## Purpose

The `file_tools.py` module provides a suite of utility functions for secure and flexible file and directory handling within a repository. It is designed to assist in reading, listing, searching, and extracting metadata from files in a way that enforces repository boundaries, preventing access to files or directories outside the intended project area. This makes it specially useful for applications that automate code analysis, repository search, or for building developer tools that work within project roots.

---

## Functionality

The module consists of four main functions:

### 1. `read_file_content(file_path: str, repo_path: str) -> str`
- Reads and returns the content of a specified file.
- Ensures the file resides within the repository and attempts multiple encodings (`utf-8`, `utf-16`, `cp1252`, `iso-8859-1`).
- Raises helpful errors if the file cannot be found, accessed, or is outside the repository structure.

### 2. `list_files_in_directory(directory_path: str, repo_path: str, extensions: Optional[List[str]]=None, recursive: bool=True) -> List[str]`
- Lists all files in a given directory within the repository.
- Supports optional filtering by file extensions and recursive or non-recursive searches.
- Returns paths relative to the repository root.

### 3. `find_files_by_pattern(pattern: str, repo_path: str, directory: Optional[str]=None) -> List[str]`
- Searches for files matching a glob pattern (`*.py`, `test_*.js`, etc.) within the repository or a subdirectory.
- Returns repository-relative paths for matched files.

### 4. `get_file_info(file_path: str, repo_path: str) -> Dict[str, Any]`
- Retrieves metadata for a given file within the repository, such as name, extension, size, last modified time, and type (file or directory).
- Validates that the file is inside the repository.

---

## Key Components

- **Pathlib & OS:** Uses `pathlib.Path` for robust, cross-platform path manipulations, and `os` for compatibility.
- **Security Checks:** Each relevant function includes a check to guarantee the target path is within the provided repo root using `relative_to()`.
- **Encodings Handling in Read:** Attempts multiple file encodings when reading text files, and falls back to binary read with error-ignore if necessary.
- **Glob Patterns:** Uses `glob` and `rglob` for advanced pattern-based searching of files.
- **Sorted Output:** Lists of files are always returned in sorted order for predictable client usage.

---

## Dependencies

### External Python Modules

- `pathlib` (standard library) — advanced path handling
- `os` (standard library) — basic operating system interactions
- `typing` (standard library) — type hints for improved static analysis

### Internal dependencies

- None (standalone utility functions; does not import from other project files)

### Downstream dependencies

- Other project files or tools seeking to list, search, or analyze files within a repository will depend on this module. It's ideal for code searchers, analysis tools, or any feature that needs safe navigation of repository files.

---

## Usage Examples

### Example 1: Read a file's content

```python
from src.tools.file_tools import read_file_content

content = read_file_content('README.md', '/path/to/my_repo')
print(content)
```

### Example 2: List Python files recursively in a directory

```python
from src.tools.file_tools import list_files_in_directory

python_files = list_files_in_directory('src', '/path/to/my_repo', extensions=['.py'])
print(python_files)
# Output: ['src/app.py', 'src/utils/helpers.py', ...]
```

### Example 3: Find all test files matching a pattern

```python
from src.tools.file_tools import find_files_by_pattern

test_files = find_files_by_pattern('test_*.py', '/path/to/my_repo', directory='tests')
print(test_files)
```

### Example 4: Get metadata for a specific file

```python
from src.tools.file_tools import get_file_info

info = get_file_info('src/main.py', '/path/to/my_repo')
print(info)
# Output:
# {
#   'path': 'src/main.py',
#   'name': 'main.py',
#   'extension': '.py',
#   'size_bytes': 1421,
#   'modified_time': 1701153703.24,
#   'is_file': True,
#   'is_directory': False
# }
```

---

## Notes and Best Practices

- Always verify that the paths provided are correct and if possible, use absolute paths for the `repo_path` to avoid confusion.
- The functions defend against path traversal (attempting to access files outside the project) and will raise errors if this is detected.
- For performance, limit recursive and pattern-based searches to necessary directories.

---

**Summary:**  
This module is a must-have for any tool or backend needing to safely access, analyze, or manipulate files within a repository environment—it provides security, flexibility, and straightforward interfaces for typical file operations.

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: 57f7db3d05ce8069071ba9136d6a464d9ca70efa938b15e7bcc4d58054cc3169
relative_path: src\tools\file_tools.py
generation_date: 2025-07-01T22:21:10.904394
```
<!-- END GENERATION METADATA -->
