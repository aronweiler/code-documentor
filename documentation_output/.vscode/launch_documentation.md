<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for .vscode\launch.json

# `.vscode/launch.json` Documentation

## Purpose

The `.vscode/launch.json` file configures Visual Studio Code's debugging environment for this project. It defines multiple debug configurations for running and testing project scripts, particularly those related to generating and validating documentation, as well as analyzing repositories. This allows developers to quickly launch common project scripts with specified parameters directly from the VS Code UI without re-typing command-line arguments.

---

## Functionality

The file leverages VS Code's [Launch configuration](https://code.visualstudio.com/docs/editor/debugging#_launch-configurations) format to set up how scripts (here, Python scripts using `debugpy`) are executed for various documentation-related workflows. The functionalities encoded cover:

- Generating file-level documentation
- Generating guides (presumably higher-level documentation)
- Generating design documents
- Running a comprehensive documentation generation workflow
- Analyzing repositories
- Validating the configuration of the documentation generation system

Each configuration customizes arguments, working directories, and environment variables (notably the `PYTHONPATH`), and launches the main script (`main.py`) in the project root.

---

## Key Components

### 1. **Configurations**

Each object under the `"configurations"` array defines a launch scenario, with keys:

- **name**: Display name in VS Code's debug panel.
- **type**: Always `"debugpy"` for Python debugging.
- **request**: Always `"launch"`, indicating a launch (not an attach) type.
- **program**: Always `"${workspaceFolder}/main.py"` – runs the main Python script at the root.
- **args**: Arguments passed to `main.py` (see details below).
- **console**: The VS Code console to use (here, always `"integratedTerminal"`).
- **cwd**: Sets the current working directory (always the workspace root).
- **env**: Sets environment variables (here, ensures `PYTHONPATH` includes the workspace root).

#### Notable Configurations

- **Generate File Documentation Only**
- **Generate/All Docs for Therapy-Link** (Windows and Linux variants)
- **Generate Design Docs**
- **Generate Guide**
- **Generate File Docs + Guide**
- **Generate File Docs + Design Docs + Guide**
- **Analyze Repository**
- **Validate Configuration**

### 2. **Arguments Passed to `main.py`**

Common arguments include:

- **generate**: Command to generate documentation.
- **--repo-path**: Path to the root of the repository to document.
- **--file-docs**: Generate file-level documentation.
- **--design-docs**: Generate design documentation.
- **--guide**: Generate user or developer guides.
- **--docs-path**: Destination directory for documentation output.
- **--cleanup**: Clean up generated docs or intermediate files.
- **--verbose**: Run with verbose output (for debugging/logging).
- **analyze**: Run repository analysis.
- **validate-config**: Validate the documentation configuration.

---

## Dependencies

### **Depends On**

- **debugpy**: Python debug adapter for VS Code.
- **main.py**: The project’s main script, assumed to handle various documentation and analysis operations.
- **Python interpreter**: The system Python used to run the scripts.
- **Workspace directory structure**: Relies on the project structure (e.g., presence of `main.py`).

### **Depended On By**

- **VS Code Debugger**: Uses this file to populate the Run and Debug UI.
- **Developers**: Rely on these configurations for efficient development, troubleshooting, and documentation tasks.

---

## Usage Examples

### **Selecting and Running a Launch Configuration**

1. Open the Run and Debug sidebar in VS Code (`Ctrl+Shift+D`).
2. Choose a configuration (e.g., *"Generate File Documentation Only"*) from the dropdown menu.
3. Press the green play (`Start Debugging`) button or `F5`.
4. The selected configuration launches `main.py` with pre-specified arguments, using the integrated terminal.

### **Example Scenarios**

#### **Generate File Documentation Only**
- Runs: 
  ```
  python main.py generate --repo-path . --file-docs --verbose
  ```
- Use when you want to produce documentation for individual files in the current repository, with extra log output.

#### **Analyze Repository**
- Runs:
  ```
  python main.py analyze C:\repos\example-project
  ```
- Use to perform analysis (possibly static analysis or metrics) on a separate codebase.

#### **Generate All Docs for Therapy-Link (Linux)**
- Runs:
  ```
  python main.py generate --repo-path /mnt/h/repos/therapy-link --docs-path /mnt/h/repos/therapy-link/docs --file-docs --guide --verbose
  ```
- Use to generate all documentation for the Therapy-Link repo on a Linux filesystem.

...

### **Customizing or Adding Configurations**
- Add new objects to the `configurations` array with the desired arguments and settings to support new workflows or scripts.

---

## Summary

This `.vscode/launch.json` streamlines common documentation and analysis workflows for the project by providing one-click or one-keystroke launch profiles in Visual Studio Code, heavily relying on the underlying `main.py` script and the Python `debugpy` debugger. It is central for development, automation, and QA tasks tied to documentation in the repository.

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: 217d4d6564914c308a4d7f414baeb425b9dbef6ab488d1fabb2cea2a8ac1bd24
relative_path: .vscode\launch.json
generation_date: 2025-07-01T23:28:30.281530
```
<!-- END GENERATION METADATA -->
