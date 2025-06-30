<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for .vscode\tasks.json

# .vscode/tasks.json

## Purpose

This file defines custom task configurations for [Visual Studio Code](https://code.visualstudio.com/) specific to your project workspace. It automates development workflows such as starting the "MCP Server" and installing required dependencies using Task Runner within VS Code. This ensures consistency and convenience when managing the environment and project-specific scripts.

---

## Functionality

The file specifies two main tasks:

### 1. **Start Documentation MCP Server**

- **Objective:** Launches the `mcp_server.py` script using the project's dedicated Python virtual environment. This task is intended to run a server (presumably to serve or generate documentation, as implied by its label).
- **How it Works:**
  - Executes `python.exe` from the `venv/Scripts` directory.
  - Passes `mcp_server.py` and the workspace directory as arguments.
  - Opens output in a new panel and always reveals it for user visibility.

### 2. **Install MCP Dependencies**

- **Objective:** Installs all required Python packages listed in `requirements.txt` into the virtual environment.
- **How it Works:**
  - Executes `pip.exe` from the `venv/Scripts` directory using the `install -r requirements.txt` command.
  - Ensures the project's dependencies are set up consistently in your environment.
  - Output and task presentation mirror the server start task (new panel, always revealed).

---

## Key Components

### Top-Level Fields

- **version:** Specifies the version of the VS Code tasks schema (`2.0.0`).
- **tasks:** An array of task objects, each representing a command that can be run from the VS Code interface.

### Task Fields

- **type:** Always `shell`, indicating commands will be run in the terminal.
- **label:** User-friendly task name displayed in the VS Code command palette.
- **command:** The executable to run—either Python or pip within the virtual environment.
- **args:** Arguments to provide to the executable. For Python, that's the server script and workspace path; for pip, it's the install command and requirements file.
- **group:** Categorizes the task under "build" for easy grouping/filtering.
- **presentation:** Controls how task output appears (e.g., always opens in a new panel).
- **options.cwd:** Ensures commands are run within the project’s workspace directory.
- **problemMatcher:** Not used here, but available for integrating tool output with VS Code’s problems panel.

---

## Dependencies

### Direct Dependencies

- **Python virtual environment**: Assumes `venv` is created and contains Python and pip executables in the standard locations.
- **mcp_server.py**: Present in the project’s root directory; must be executable as a main script.
- **requirements.txt**: Must exist in the workspace root for dependency installation.

### What Depends on This File

- The VS Code editor uses this file to offer automated tasks in its Run Task menu.
- Developers working in this project rely on these configurations for consistent commands and environment setup.

---

## Usage Examples

After opening your project in Visual Studio Code:

### 1. Start the Documentation MCP Server

- Open the Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P`).
- Run: **Tasks: Run Task**.
- Choose **Start Documentation MCP Server** from the list.
- The server will start, and you’ll see the output in a new terminal panel.

### 2. Install MCP Dependencies

- Open the Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P`).
- Run: **Tasks: Run Task**.
- Choose **Install MCP Dependencies**.
- All dependencies from `requirements.txt` will be installed using the project's virtual environment.

---

## Additional Notes

- If you change the layout of your virtual environment or rename key files (`mcp_server.py`, `requirements.txt`), update the `tasks.json` paths accordingly.
- You may add new tasks for other scripts or workflows by expanding this file following the existing structure.

---

**Do not edit `.vscode/tasks.json` unless you are configuring, adding, or removing automated project tasks in VS Code.**

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: 77d3ef6245c73831e7167561620aacd943862d4815d97bdb5082fa58ca15bf0a
relative_path: .vscode\tasks.json
generation_date: 2025-06-30T14:13:47.950412
```
<!-- END GENERATION METADATA -->
