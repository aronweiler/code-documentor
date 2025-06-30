<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for .vscode/tasks.json

# .vscode/tasks.json

## Purpose

This file defines reusable build and utility tasks for Visual Studio Code in the context of a Python project using a virtual environment (venv).  
It automates commands for starting the documentation MCP server and installing project Python dependencies, making development workflows faster and more consistent across environments.

## Functionality

The file specifies VS Code tasks that can be executed directly from the editor. Each task is a shell command with configuration for how it runs, how output is displayed, and task grouping for easy invocation.

### Main Tasks

1. **Start Documentation MCP Server**:
    - Launches a Python script (`mcp_server.py`) using the project's Python interpreter from the venv.
    - Passes the project directory as an argument.
    - Useful for starting local servers related to documentation or code review.

2. **Install MCP Dependencies**:
    - Installs project dependencies from `requirements.txt` using the pip executable from the venv.
    - Ensures the development environment has all required libraries installed.

## Key Components

- **Tasks Array**: Contains all the task entries to be recognized by VS Code.
- **Task Properties**:
    - `type`: Type of task (`shell` for shell commands).
    - `label`: Display name in VS Code task picker.
    - `command`: Executable path (Python interpreter or pip).
    - `args`: Arguments to the command.
    - `group`: Grouping for easy invocation (`build` in both cases).
    - `presentation`: Control of how and where command output is shown.
    - `options.cwd`: Working directory for the command.
    - `problemMatcher`: Empty array means no output parsing for errors/warnings.

## Dependencies

### This File Depends On

- The existence of a Python virtual environment in `venv/` within the workspace.
- The scripts:
    - `mcp_server.py` in the workspace root.
    - `requirements.txt` in the workspace root.
- Python and pip executables located at `${workspaceFolder}/venv/Scripts/python.exe` and `${workspaceFolder}/venv/Scripts/pip.exe` (Windows paths).

### Depended On By

- Visual Studio Code: reads and presents these tasks to the user.
- Developers: can run these tasks via the VS Code command palette, status bar, or as part of workspace-level automation.

## Usage Examples

### 1. Start Documentation MCP Server

**How to Run:**
- Open the command palette (`Ctrl+Shift+P`), select "Run Task", then pick **Start Documentation MCP Server**.
- Or configure as a preLaunchTask for debugging configurations.

**What It Does:**
```sh
venv\Scripts\python.exe mcp_server.py <workspaceFolder>
```

### 2. Install MCP Dependencies

**How to Run:**
- Open the command palette (`Ctrl+Shift+P`), select "Run Task", then pick **Install MCP Dependencies**.

**What It Does:**
```sh
venv\Scripts\pip.exe install -r requirements.txt
```

**Typical Workflow:**
1. Run "Install MCP Dependencies" to set up all Python requirements.
2. Run "Start Documentation MCP Server" to launch the local server for documentation.

---

**Note:**  
These tasks are primarily configured for Windows environments due to the explicit use of the `Scripts` directory for the virtual environment's executables.  
For use on macOS or Linux, adjust executable paths to `venv/bin/python` and `venv/bin/pip` as needed.

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: f0c5c284d4b06ba0a92b9d542ab0d6a0f413edf3f2fb6d9f02595eb156185ca2
relative_path: .vscode/tasks.json
generation_date: 2025-06-30T00:02:02.441420
```
<!-- END GENERATION METADATA -->
