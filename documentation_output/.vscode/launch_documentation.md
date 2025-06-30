<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for .vscode\launch.json

# .vscode/launch.json

## Purpose

This file provides **debugging and run configurations** for Visual Studio Code (VS Code), specifically for running and debugging various documentation generation tasks on a Python project. These configurations let developers quickly launch specific functions in `main.py` with tailored command-line arguments and environment variables.

## Functionality

- **Defines launch configurations for common documentation-related tasks** including generating file documentation, design documentation, guides, and running repository analyses.
- **Supports multiple environments** (e.g., Windows and Linux paths).
- **Automates repetitive command line arguments and environment setup** for working with the project's documentation tooling.

## Key Components

### Top-level Properties

- **version**: Specifies the schema version for the launch configuration format (required by VS Code).
- **configurations**: An array containing individual launch/debug configurations.

### Configuration Objects

Each object in `configurations` provides a specific launch/debug scenario. Key fields include:

- **name**: Descriptive label in the VS Code "Run & Debug" menu.
- **type**: Debugger type (`debugpy` indicates Python debugging).
- **request**: The type of action; `"launch"` to start a new process.
- **program**: The Python file to run (`${workspaceFolder}/main.py`).
- **args**: Arguments to pass to the script (`main.py`). These differ based on the specific documentation task.
- **console**: Where to show output (`integratedTerminal`).
- **cwd**: Working directory for the process (usually `${workspaceFolder}`).
- **env**: Environment variables—for now, always sets `PYTHONPATH` to the workspace root.

### Notable Configurations

Each configuration launches `main.py` with arguments suitable for different tasks:

- **Generate File Documentation Only**: Generates only per-file documentation for the current repo.
- **Generate All Docs for Therapy-Link**: Generates all docs (files, guides) into a specified location (Windows path variant).
- **Generate All Docs for Therapy-Link (Linux)**: Similar, but uses Linux path conventions.
- **Generate Design Docs**: Generates only design documentation.
- **Generate Guide**: Generates a user guide in a specified output directory.
- **Generate File Docs + Guide**: Runs both file docs and guides.
- **Generate File Docs + Design Docs + Guide**: Runs all major documentation generators for an example repo.
- **Analyze Repository**: Runs analysis mode on a specified project path.
- **Validate Configuration**: Validates the project's configuration.

## Dependencies

- **Direct Dependencies**:
  - VS Code (the file is only relevant inside a VS Code workspace).
  - [`debugpy`](https://github.com/microsoft/debugpy) Python debugger extension.

- **Indirect/project-specific dependencies**:
  - `main.py`: Must exist in your workspace folder, as all configurations launch this script.
  - The Python project should be structured so that setting `PYTHONPATH=${workspaceFolder}` suffices for correct imports.

- **Consumers**:
  - Other files, scripts, or team members do not usually “depend on” `launch.json`, but it is used by the VS Code Run & Debug UI.

## Usage Examples

These scenarios are visible in the VS Code "Run & Debug" panel once you open the workspace:

### Example 1: Generate Only File Documentation

1. Open VS Code in the project directory.
2. Go to Run & Debug (`Ctrl+Shift+D`).
3. Choose **Generate File Documentation Only** and click the green play button.
4. VS Code will launch `python main.py generate --repo-path . --file-docs --verbose` in the workspace root.

### Example 2: Generate All Docs for Therapy-Link (Windows)

1. Select **Generate All Docs for Therapy-Link**.
2. Click run. The following command is executed:
   ```
   python main.py generate --repo-path H:\repos\therapy-link --docs-path H:\repos\therapy-link\docs --file-docs --guide --verbose
   ```

### Example 3: Analyze Repository

1. Choose **Analyze Repository**.
2. Initiates:
   ```
   python main.py analyze C:\repos\example-project
   ```

### Customization

You can duplicate any configuration to run additional or custom documentation commands by modifying the `args` array as needed.

---

**Tip:** Always check that the referenced paths and files exist in your environment, and that the required Python dependencies are installed and available to the interpreter specified by VS Code.

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: a4b59cff3bb79991b2a484f0bd5e1b841ec85a1578863490580fe8d13616329d
relative_path: .vscode\launch.json
generation_date: 2025-06-30T14:13:21.581822
```
<!-- END GENERATION METADATA -->
