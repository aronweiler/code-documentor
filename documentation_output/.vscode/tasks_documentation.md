<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for .vscode\tasks.json

# `.vscode/tasks.json` Documentation

## Purpose

This file defines reusable **VS Code Tasks** for automating developer workflows related to the Documentation MCP Server in your project. It enables quick launching of the MCP server and installs necessary dependencies via pip, all from within the VS Code tasks interface.

By centralizing these common operations, it simplifies onboarding and daily development, ensuring that contributors are always working with a properly configured environment and minimizing manual command-line effort.

---

## Functionality

The file contains two main VS Code tasks:

1. **Start Documentation MCP Server**  
   Launches the MCP (Model Context Protocol) documentation server as a background process using the workspace's Python virtual environment.

2. **Install MCP Dependencies**  
   Installs the required Python packages as defined in `requirements.txt` using pip from the workspace's virtual environment.

Both tasks are type `"shell"` tasks, meaning they run as shell commands inside VS Code terminals.

---

## Key Components

- **`version`**:  
  Specifies the tasks configuration version (`2.0.0` is the current standard).

- **`tasks`**:  
  An array of task definitions, each describing a workflow step.

### Task: Start Documentation MCP Server

- **`type`**: `"shell"`  
  This is a shell-based task (executes given command in a shell).

- **`label`**: Unique identifier for the task as it appears in the VS Code UI.

- **`command`**:  
  Runs the MCP server using the Python interpreter from the active virtual environment:
  ```
  ${workspaceFolder}/venv/Scripts/python.exe
  ```

- **`args`**:  
  Specifies the MCP server script and passes the workspace as a parameter:
  ```
  ${workspaceFolder}/mcp_server.py
  ${workspaceFolder}
  ```

- **`group`**:  
  Designates it as a "build" task (visible in the Tasks panel's build category).

- **`presentation`**:  
  Customizes the terminal behavior (always reveals output, uses a new terminal panel, etc.).

- **`options.cwd`**:  
  Ensures command executes from the workspace root.

- **`problemMatcher`**:  
  Empty array; means no output parsing for errors/warnings.

### Task: Install MCP Dependencies

- **`type`**: `"shell"`  
  Runs the pip package installer.

- **`label`**:  
  Describes the task (shows as "Install MCP Dependencies").

- **`command`**:  
  Uses pip from the project’s virtual environment:
  ```
  ${workspaceFolder}/venv/Scripts/pip.exe
  ```

- **`args`**:  
  Installs dependencies from `requirements.txt`:
  ```
  install -r requirements.txt
  ```

- **Other fields**:  
  `group`, `presentation`, and `options.cwd` are configured similarly to the server start task.

---

## Dependencies

### Required by This File

- This tasks file depends on:
  - Existence of a valid Python virtual environment at `venv/`
  - The MCP server script: `mcp_server.py` in the workspace root
  - A `requirements.txt` file listing all Python dependencies

### What Depends on It

- Developers using VS Code who wish to reliably start the MCP server or install dependencies using the Command Palette (Ctrl/Cmd + Shift + P → "Tasks: Run Task") or via the Tasks sidebar.

---

## Usage Examples

### Running the Documentation MCP Server

1. Press `Ctrl/Cmd + Shift + P` in VS Code
2. Type `Tasks: Run Task`
3. Select `Start Documentation MCP Server`

This will initialize the server for your repository, enabling MCP-based documentation tools (such as Claude Code or VS Code MCP integrations).

### Installing Dependencies

1. Press `Ctrl/Cmd + Shift + P`
2. Select `Tasks: Run Task`
3. Choose `Install MCP Dependencies`

This will install or update all required Python packages in your virtual environment, ensuring the server and related tools can run.

---

## Additional Notes

- **Platform-Specific Paths**:  
  The paths in this configuration (`venv/Scripts/python.exe`, `venv/Scripts/pip.exe`) are **Windows-style**.  
  - On **Linux/macOS**, you would use:
    - `venv/bin/python` and `venv/bin/pip`
  - If your project is cross-platform, consider a different configuration for non-Windows users.

- **Customization**:  
  You can add more tasks or tweak existing ones (such as adding test runners or linting) to suit your workflow as needed.

- **Integration**:  
  Tasks work hand-in-hand with launch configurations (`.vscode/launch.json`) for a seamless coding and debugging experience.

---

## File Format Reference

- VS Code tasks documentation: [https://code.visualstudio.com/docs/editor/tasks](https://code.visualstudio.com/docs/editor/tasks)
- For more details on how to further customize tasks, see the official documentation.

---

**In summary:**  
`.vscode/tasks.json` automates the development environment for the Documentation MCP Server in VS Code by providing ready-to-use tasks for server startup and dependency installation, promoting consistency and developer convenience.

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: 77d3ef6245c73831e7167561620aacd943862d4815d97bdb5082fa58ca15bf0a
relative_path: .vscode\tasks.json
generation_date: 2025-07-01T23:03:49.718735
```
<!-- END GENERATION METADATA -->
