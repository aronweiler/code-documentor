<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for .vscode\settings.json

# `.vscode/settings.json` Documentation

## Purpose

This configuration file customizes project-level settings for [Visual Studio Code (VS Code)](https://code.visualstudio.com/) within your workspace. It streamlines Python development and seamlessly integrates the **MCP (Model Context Protocol) documentation server** into the VS Code environment. By ensuring consistent interpreter usage and defining MCP server commands, this file helps maintain a reproducible, automated workflow for code documentation and AI-powered code analysis features.

---

## Functionality

The file defines the following main settings:

### Python Interpreter Configuration

- **`python.pythonPath`**  
  Sets the full path to the Python interpreter to be used by VS Code for this project. This ensures that all Python operations (running, linting, testing, debugging) use the same interpreter, typically a virtual environment local to the project.

- **`python.defaultInterpreterPath`**  
  Newer VS Code Python extension uses this setting for the default interpreter. Here, it matches `python.pythonPath`, pointing to the `venv` virtual environment within the workspace.

### MCP Server Integration

- **`mcp.servers`**  
  Adds a custom MCP server configuration named `"documentation-server"`. This allows the MCP VS Code extension (or other compatible tools) to start and connect to an instance of the `mcp_server.py` script from within VS Code.

  - **`command`**: Specifies the interpreter to launch the MCP server (project virtual environment's Python).
  - **`args`**: Arguments to pass to the Python command.
    - `${workspaceFolder}/mcp_server.py`: The MCP server script, relative to the project root.
    - `${workspaceFolder}`: The target repository path, typically the current workspace.
  - **`cwd`**: Sets the working directory for the subprocess to the root of the workspace.

---

## Key Components

- **Variable Expansion (`${workspaceFolder}`):**
  - Ensures paths are always relative to the currently opened VS Code workspace, promoting portability and collaborative consistency.
- **Virtual Environment Usage:**  
  - Both Python interpreter settings and the MCP server command use the `venv/Scripts/python.exe` interpreter, isolating dependencies and avoiding conflicts.
- **MCP Server Automation:**  
  - The configuration under `mcp.servers` supports the VS Code MCP extension or similar tools for effortless starting, stopping, and monitoring of the documentation MCP server.

---

## Dependencies

### Depends On

- **Local Virtual Environment**:  
  - Expects a Python virtual environment at `${workspaceFolder}/venv` (usually set up with `python -m venv venv`).
- **`mcp_server.py` Script**:  
  - The documentation MCP server must exist as `${workspaceFolder}/mcp_server.py`.
- **VS Code extensions**:
  - [Python extension for VS Code](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
  - [MCP VS Code extension](https://github.com/langchain-ai/langgraph) (or compatible)

### Used By

- **VS Code itself:**  
  - Reads `settings.json` to configure the editor and extensions upon project load.
- **MCP extension:**  
  - Discovers `mcp.servers` entries for launching tools like the documentation server.

---

## Usage Examples

### 1. **Working with Python in This Project**

When you open VS Code in the repository:
- The Python interpreter will be set automatically to the virtual environment (`venv/Scripts/python.exe`).
- Python files will run, debug, and lint using this interpreter.

### 2. **Running the Documentation MCP Server**

If you have the [MCP VS Code extension](https://github.com/langchain-ai/langgraph) or a compatible client:
- You can invoke or manage the `"documentation-server"` directly from VS Code (e.g., MCP panel or commands).
- The server will launch as:
  ```bash
  venv/Scripts/python.exe mcp_server.py .
  ```
  in the root workspace directory.

### 3. **Recommended Workflow**

1. Install dependencies and set up your virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Launch VS Code with this workspace; Python interpreter will be auto-set.
3. Generate documentation for your codebase (see main README).
4. Use the MCP extension or VS Code Tasks to start the Documentation MCP Server.
5. Use features like "get relevant files" or "feature understanding" directly from your IDE.

---

## Summary Table

| Setting                              | Purpose                                            |
|---------------------------------------|----------------------------------------------------|
| `"python.pythonPath"`                 | Sets Python interpreter for VS Code                |
| `"python.defaultInterpreterPath"`     | Default Python interpreter (newer VS Code)         |
| `"mcp.servers.documentation-server"`  | Defines how to launch the documentation MCP server |

---

## See Also

- [Project README: "VS Code Integration" Section](README.md)
- [Python in VS Code Documentation](https://code.visualstudio.com/docs/python/python-tutorial)
- [LangGraph MCP Protocol](https://github.com/langchain-ai/langgraph)

---

**Note**:  
- On non-Windows systems, the interpreter path should be adjusted (typically `venv/bin/python`).  
- This settings file is for **per-project configuration**; do not commit sensitive information or machine-specific paths.

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: aa95ce127c3cdbc38cd0e1bf9e52fdc879d6280b9e12a48e3a6a5c421ddd1b54
relative_path: .vscode\settings.json
generation_date: 2025-07-01T23:03:32.097059
```
<!-- END GENERATION METADATA -->
