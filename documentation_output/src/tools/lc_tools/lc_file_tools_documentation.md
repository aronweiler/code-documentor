<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for src/tools/lc_tools/lc_file_tools.py

# lc_file_tools.py

## Purpose

This file defines a factory function for creating a set of [LangChain](https://python.langchain.com/) `Tool` objects for interacting with files in a specific repository. It exposes various file system operations—reading file contents, listing files in directories, searching by pattern, and getting file metadata—through a structured and consistent interface. The primary use case is to provide language model agents with safe, controlled access to a repository's files for tasks such as code analysis, documentation, or automation.

---

## Functionality

### Main Function

#### `create_file_tools(repo_path: Path) -> List[Tool]`

- **Description**: Factory function to instantiate a list of LangChain `Tool` objects, each implementing a different file operation bound to a specified repository root.
- **Parameters**:  
  - `repo_path` (`Path`): The root path of the repository to operate on.
- **Returns**:  
  - `List[Tool]`: A list of LangChain `Tool` objects with standardized names and descriptions.

#### Internal Wrapper Functions

All wrappers handle conversion, parameter adaptation, exception handling, and output formatting for the underlying file operations:

- **`read_file_wrapper(file_path: str) -> str`**
  - Reads and returns the contents of the specified file.
- **`list_files_wrapper(directory_path: str, extensions: str = "", recursive: str = "true") -> str`**
  - Lists files in a directory, with optional filtering by extension(s) and recursion.
- **`find_files_wrapper(pattern: str, directory: str = "") -> str`**
  - Finds files matching a glob pattern; can be scoped to a subdirectory.
- **`get_file_info_wrapper(file_path: str) -> str`**
  - Returns basic information about a file: path, size, extension, and last modification time.

Each wrapper is attached as a function (`func`) in a corresponding LangChain `Tool` entry, with an explicit `name` and `description` for user-facing agent interactions.

---

## Key Components

- **Imports**:
  - `List` from `typing`
  - `Path` from `pathlib`
  - `Tool` from `langchain.tools`
  - File utility functions from a sibling module (`..file_tools`):
    - `read_file_content`
    - `list_files_in_directory`
    - `find_files_by_pattern`
    - `get_file_info`
- **Wrapper Functions**:
  - Handle input/output normalization and exception reporting for agent robustness.
- **LangChain `Tool` Instances**:
  - Each represents a repository file operation, ready to be added to an agent or chain.

---

## Dependencies

### External

- **`langchain.tools.Tool`**: For structuring agent actions as callable, describable tools.
- **`pathlib.Path`**: For robust, cross-platform file path handling.

### Internal

- **Sibling Module `file_tools`**:
  - Core functions (`read_file_content`, `list_files_in_directory`, `find_files_by_pattern`, `get_file_info`) implement the actual file system logic. This file acts as a bridge, exposing those capabilities to LangChain agents.

### Downstream

- Any code using LangChain agents that wants to enable file reading, listing, searching, and metadata retrieval within a repo should import and call `create_file_tools`.

---

## Usage Examples

### 1. Integrating With a LangChain Agent

```python
from pathlib import Path
from langchain.agents import initialize_agent
from src.tools.lc_tools.lc_file_tools import create_file_tools

repo_path = Path("/path/to/my/code/repo")

# Create the file tools.
tools = create_file_tools(repo_path)

# Add these tools to your agent.
agent = initialize_agent(
    tools=tools,
    llm=your_llm,  # Your chosen language model
    agent_type="zero-shot-react-description"
)

# Now your agent can:
# - Read file contents
# - List files (with extension filters, recursion)
# - Find files by glob
# - Get file metadata info
```

### 2. Manual Invocation of Tools

```python
tools = create_file_tools(Path("/my/repo"))

# Call the read file tool directly
file_text = tools[0].func("src/main.py")
print(file_text)

# List all Python files in the 'utils' directory, non-recursively
py_files = tools[1].func("utils", ".py", "false")
print(py_files)
```

---

## Notes

- Relative paths in tool calls are always interpreted with respect to the given `repo_path`.
- All tool outputs are strings, formatted for easy agent consumption.
- The tools return helpful error messages on failure—no exceptions are propagated.
- For core file logic, see the sibling `file_tools` module.

---

**This file bridges file system utility functions (_file_tools_) to the LangChain agent interface, providing robust, well-described tools for controlled repository access in agent-driven workflows.**

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: 76848ce72ac62104407dd8a841684e6ab09f260c5790a2c3f20fd917cbc6ddf9
relative_path: src/tools/lc_tools/lc_file_tools.py
generation_date: 2025-06-30T00:13:49.106601
```
<!-- END GENERATION METADATA -->
