<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for src/tools/file_tools.py

# file_tools.py

## Purpose

This module provides safe and convenient functions for performing common file and directory operations within a specified repository. Its primary focus is to ensure that all file accesses are contained within the repository boundaries to prevent unauthorized or accidental access to files outside the project scope. It includes utilities for reading file contents, listing files, searching with patterns, and gathering file metadata.

---

## Functionality

The module offers several key functions:

### 1. `read_file_content(file_path: str, repo_path: str) -> str`
- **Description**: Reads and returns the textual content of a file within the repository, handling both relative and absolute paths and trying multiple encodings for robustness.
- **Security**: Ensures the target file resides within `repo_path`.
- **Raises**: 
    - `FileNotFoundError` if the file doesn't exist,
    - `PermissionError` if the file can't be read,
    - `ValueError` if the file is outside the repo or not a file.

### 2. `list_files_in_directory(directory_path: str, repo_path: str, extensions: Optional[List[str]] = None, recursive: bool = True) -> List[str]`
- **Description**: Lists all files in the given directory (and optionally subdirectories) within the repository. Supports filtering results by file extension.
- **Security**: Ensures the directory queried is within the repo and is a valid directory.
- **Returns**: Relative paths of matching files as a sorted list.

### 3. `find_files_by_pattern(pattern: str, repo_path: str, directory: Optional[str] = None) -> List[str]`
- **Description**: Searches for files matching a glob pattern within the repository or a subdirectory, returning relative paths.
- **Security**: Ensures the search is confined within the repo.
- **Returns**: Sorted list of matching file paths.

### 4. `get_file_info(file_path: str, repo_path: str) -> Dict[str, Any]`
- **Description**: Retrieves metadata about a file, such as size, name, extension, modified time, and type.
- **Security**: Ensures the file is inside the repository.
- **Returns**: Dictionary with file information.

---

## Key Components

- **`Path` (from `pathlib`)**: Used extensively for path manipulations and checks, ensuring reliability across platforms.
- **Security Checks**: Each function verifies that paths remain inside the specified repository root via `relative_to`.
- **Extension and Pattern Filtering**: File listing and searching functions support flexible filtering.
- **Encoding Handling**: File reading tries several encodings for robust reading of various file types.

---

## Dependencies

### External Modules
- **pathlib**: For path operations in an object-oriented way.
- **os**: Some minor filesystem operations (not critically used here).
- **typing**: For type annotations (`List`, `Optional`, `Dict`, `Any`).

### Internal Project Structure
- This file is **self-contained** and does not depend on other internal modules.
- **Other components can import this module** to safely handle file operations restricted within a repository boundary (for command-line tools, web apps, services, etc).

---

## Usage Examples

**Reading a file's content:**
```python
from src.tools.file_tools import read_file_content

file_content = read_file_content("src/main.py", "/Users/alice/my_repo")
print(file_content)
```

**Listing all Python files recursively in a subdirectory:**
```python
from src.tools.file_tools import list_files_in_directory

python_files = list_files_in_directory(
    "src",
    "/Users/alice/my_repo",
    extensions=[".py"],
    recursive=True
)
print(python_files)
```

**Finding test files with a pattern:**
```python
from src.tools.file_tools import find_files_by_pattern

test_files = find_files_by_pattern("test_*.py", "/Users/alice/my_repo", directory="tests")
print(test_files)
```

**Fetching detailed file metadata:**
```python
from src.tools.file_tools import get_file_info

file_info = get_file_info("src/main.py", "/Users/alice/my_repo")
print(file_info)
# {
#     "path": "src/main.py",
#     "name": "main.py",
#     "extension": ".py",
#     "size_bytes": ...,
#     "modified_time": ...,
#     "is_file": True,
#     "is_directory": False,
# }
```

---

## Notes

- **Security**: All file and directory accesses are restricted to within `repo_path`. A `ValueError` is raised if an attempt is made to access files or directories outside of this boundary.
- **Encodings**: When reading files, several encodings are tried to maximize compatibility; binary mode is used as a last resort with error suppression for undecodable bytes.
- **Extensions**: When filtering by extension, extensions are matched in a case-insensitive manner and should include the leading dot (e.g., `['.py', '.txt']`).

---

**This file is intended for use by any features, tools, or scripts that need controlled access to file system data within a project or repository.**

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: 57f7db3d05ce8069071ba9136d6a464d9ca70efa938b15e7bcc4d58054cc3169
relative_path: src/tools/file_tools.py
generation_date: 2025-06-30T00:13:22.733590
```
<!-- END GENERATION METADATA -->
