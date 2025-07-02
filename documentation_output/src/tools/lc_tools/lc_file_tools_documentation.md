<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for src\tools\lc_tools\lc_file_tools.py

# lc_file_tools.py

## Purpose

This file defines utilities to generate a collection of file operation tools (as `Tool` objects) for use with LangChain. These tools enable reading file contents, listing files, searching for files by pattern, and retrieving file metadata within a given repository. The intent is to provide a language-model-friendly interface for common file system operations scoped to a specific repository path.

---

## Functionality

The core function in this module is:

### `create_file_tools(repo_path: Path) -> List[Tool]`

- Returns a list of LangChain `Tool` objects, each exposing repository-specific file system functions.
- The tool functions wrap lower-level implementations (e.g., `read_file_content`) and inject exception handling and LangChain integration.
- The following tools are exposed:
  - `read_file_content` — Read content of a specified file.
  - `list_files_in_directory` — List files in a directory, with filtering and recursion options.
  - `find_files_by_pattern` — Find files by glob pattern, optionally within a subdirectory.
  - `get_file_info` — Get file metadata (size, extension, modification time).

---

## Key Components

### Inner Wrappers (Functions):

Each tool exposes a wrapper function to adapt low-level I/O for LangChain usage:

- **`read_file_wrapper(file_path: str) -> str`**
  - Calls `read_file_content` and returns the file's contents or an error string.

- **`list_files_wrapper(directory_path: str, extensions: str = "", recursive: str = "true") -> str`**
  - Calls `list_files_in_directory` with optional extension and recursion control.
  - Formats results as newline-separated list or a message if empty.

- **`find_files_wrapper(pattern: str, directory: str = "") -> str`**
  - Searches for files matching a `pattern` in an optional directory using `find_files_by_pattern`.
  - Returns a newline-separated list or a not-found message.

- **`get_file_info_wrapper(file_path: str) -> str`**
  - Gets size, extension, and modification time of a file using `get_file_info`.
  - Formats the information as a readable string.

### File Tool List

- **`file_tools`**  
  A list of four `Tool`-type objects, each encapsulating a file system operation for repo-scoped usage (as described above).

---

## Dependencies

### Internal Dependencies

- **`read_file_content`**
- **`list_files_in_directory`**
- **`find_files_by_pattern`**
- **`get_file_info`**

  — All imported from the sibling module `..file_tools` (must be present/implemented).

### External Dependencies

- **`Path`** from `pathlib`
- **`List`** from `typing`
- **`Tool`** from `langchain.tools`

### What Depends on This

- Any code wishing to expose repo-scoped file operations as LangChain Tools.
- Typically imported and called within a LangChain agent or custom chain to provide file I/O for LLM-driven workflows.

---

## Usage Examples

### Example 1: Generating Tools for an Agent

```python
from pathlib import Path
from src.tools.lc_tools.lc_file_tools import create_file_tools

repo_root = Path("/path/to/my/repo")
tools = create_file_tools(repo_root)

# Now `tools` can be added to a LangChain agent/toolchain
for tool in tools:
    print(tool.name)
```

### Example 2: Use a Tool Directly

```python
tools = create_file_tools(Path("./my_repo"))
read_tool = [t for t in tools if t.name == "read_file_content"][0]

file_contents = read_tool.run("README.md")
print(file_contents)
```

---

## Notes

- All file paths are interpreted as relative to the `repo_path` provided.
- Wrappers ensure any operating system errors are returned as readable messages, not exceptions.  
- These tools are **not** intended for direct command-line use, but for integration with LangChain's Tool abstraction or similar AI orchestration frameworks.

---

## Summary

This file defines a convenient factory (`create_file_tools`) to produce LangChain Tools for repository-scoped file system operations, wrapping common tasks like reading files, listing/searching files, and metadata retrieval into AI-accessible functions. It serves as a bridge between lower-level file manipulation and higher-level language model agent workflows.

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: 76848ce72ac62104407dd8a841684e6ab09f260c5790a2c3f20fd917cbc6ddf9
relative_path: src\tools\lc_tools\lc_file_tools.py
generation_date: 2025-07-01T22:21:24.474393
```
<!-- END GENERATION METADATA -->
