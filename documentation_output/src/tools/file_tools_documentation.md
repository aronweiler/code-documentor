<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for src\tools\file_tools.py

# File Tools Documentation

## Purpose

The `file_tools.py` module provides utility functions for handling file operations within a specified repository. It is designed to facilitate reading file contents, listing files in directories, finding files by patterns, and retrieving file information, all while ensuring that operations are performed within the bounds of a given repository.

## Functionality

### `read_file_content(file_path: str, repo_path: str) -> str`

Reads the content of a specified file within the repository.

- **Args:**
  - `file_path`: The relative or absolute path to the file.
  - `repo_path`: The root path of the repository.

- **Returns:** The content of the file as a string.

- **Raises:**
  - `FileNotFoundError`: If the file does not exist.
  - `PermissionError`: If the file cannot be read.
  - `ValueError`: If the file is outside the repository bounds.

### `list_files_in_directory(directory_path: str, repo_path: str, extensions: Optional[List[str]] = None, recursive: bool = True) -> List[str]`

Lists files in a specified directory within the repository.

- **Args:**
  - `directory_path`: The relative path to the directory from the repository root.
  - `repo_path`: The root path of the repository.
  - `extensions`: An optional list of file extensions to filter by (e.g., `['.py', '.js']`).
  - `recursive`: A boolean indicating whether to search subdirectories.

- **Returns:** A list of relative file paths.

### `find_files_by_pattern(pattern: str, repo_path: str, directory: Optional[str] = None) -> List[str]`

Finds files matching a specified pattern within the repository.

- **Args:**
  - `pattern`: A glob pattern to match (e.g., `"*.py"`, `"test_*.py"`).
  - `repo_path`: The root path of the repository.
  - `directory`: An optional subdirectory to search within.

- **Returns:** A list of relative file paths matching the pattern.

### `get_file_info(file_path: str, repo_path: str) -> Dict[str, Any]`

Retrieves information about a specified file.

- **Args:**
  - `file_path`: The relative path to the file from the repository root.
  - `repo_path`: The root path of the repository.

- **Returns:** A dictionary containing file information such as path, name, extension, size in bytes, modified time, and whether it is a file or directory.

## Key Components

- **Functions**: The module consists of four main functions: `read_file_content`, `list_files_in_directory`, `find_files_by_pattern`, and `get_file_info`.
- **Error Handling**: Each function includes error handling to ensure operations are performed within the repository bounds and to handle common file-related errors.

## Dependencies

- **Python Standard Library**: The module relies on `pathlib` for path manipulations and `os` for file operations.
- **Type Hints**: Utilizes `List`, `Optional`, `Dict`, and `Any` from the `typing` module for type annotations.

## Usage Examples

### Example 1: Reading File Content

```python
repo_path = "/path/to/repo"
file_path = "docs/readme.md"
content = read_file_content(file_path, repo_path)
print(content)
```

### Example 2: Listing Files in a Directory

```python
repo_path = "/path/to/repo"
directory_path = "src"
files = list_files_in_directory(directory_path, repo_path, extensions=['.py'])
print(files)
```

### Example 3: Finding Files by Pattern

```python
repo_path = "/path/to/repo"
pattern = "*.py"
files = find_files_by_pattern(pattern, repo_path)
print(files)
```

### Example 4: Getting File Information

```python
repo_path = "/path/to/repo"
file_path = "src/tools/file_tools.py"
info = get_file_info(file_path, repo_path)
print(info)
```

This module is essential for managing file operations within a repository, ensuring security and ease of use through its comprehensive set of utility functions.

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: 57f7db3d05ce8069071ba9136d6a464d9ca70efa938b15e7bcc4d58054cc3169
relative_path: src\tools\file_tools.py
generation_date: 2025-06-10T20:43:17.225690
```
<!-- END GENERATION METADATA -->
