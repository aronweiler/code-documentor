<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for .vscode/launch.json

# .vscode/launch.json

## Purpose

This file configures **launch and debug settings** for Visual Studio Code (VSCode) for a Python project. It defines a set of pre-configured launch configurations that streamline running or debugging common project tasks and scripts, particularly related to documentation and repository analysis.

## Functionality

The configurations in this file allow team members to easily:

- Generate various types of documentation (file-level docs, guides, design docs) for the project or external repositories.
- Validate project configuration.
- Analyze the repository structure or content.
- Switch seamlessly between these tasks with a convenient launch menu within VSCode.

Each configuration is tailored with the appropriate command-line arguments, working directories, and environment settings. All profiles use Python (specifically the [debugpy](https://github.com/microsoft/debugpy) launcher) as the runtime.

## Key Components

### Main Sections

- **version**: Specifies the version of the launch configuration schema; `"0.2.0"` is standard for VSCode.
- **configurations**: An array of configuration objects, each corresponding to a task or debug scenario.

### Important Configuration Entries

Each configuration shares some or all of the following keys:

- **name**: A unique, descriptive name for the launch task (shown in VSCode UI).
- **type**: The debugger type (here, always `"debugpy"` for Python).
- **request**: How this is run. Use `"launch"` to start the script.
- **program**: The main Python file to execute, usually `${workspaceFolder}/main.py`.
- **args**: Arguments passed to the Python script. These control the operation, e.g. `"generate"`, `"analyze"`, `"validate-config"`, and various flags like `--file-docs`, `--guide`, `--docs-path`, etc.
- **console**: Where output appears (`"integratedTerminal"`).
- **cwd**: Working directory for the process (defaults to `${workspaceFolder}`).
- **env**: Environment variables to set (`"PYTHONPATH"` ensures local imports work).

### Notable Configurations

- **Generate File Documentation Only**: Generates only file-level docs for the project.
- **Generate All Docs for Therapy-Link & Linux Variant**: Runs comprehensive documentation (files, guides) for a remote project, configurable for Windows and Linux paths.
- **Generate Design Docs**: Only generates design documentation.
- **Generate Guide / File Docs + Guide / File Docs + Design Docs + Guide**: Combinations for generating guides, file docs, and design docs.
- **Analyze Repository**: Runs the `analyze` command on a project path, presumably scanning code or structure.
- **Validate Configuration**: Runs configuration validation logic.

## Dependencies

### External Tooling & Libraries

- **VSCode**: Interprets this configuration file for debugging and task launching.
- **debugpy**: Required as the Python debugger for the configurations.
- **Python**: All commands invoke a Python script (`main.py`), which must implement the respective CLI commands (`generate`, `analyze`, `validate-config`, etc.).

### Internal Dependencies

- **main.py**: The central entry point. All the logic implied by these tasks must exist in this script.

### What Depends on This File

- VSCode only. Developers interact with these definitions in the "Run and Debug" sidebar or from the Command Palette.

## Usage Examples

These configurations are surfaced directly in the VSCode "Run and Debug" sidebar for use.

### Example: Launching a Documentation Generator

To generate both file and guide documentation for the current repository:

1. Open the Run and Debug sidebar (Ctrl+Shift+D).
2. Select **Generate File Docs + Guide** from the list.
3. Click "Run" or "Start Debugging".

This will run:

```bash
python main.py generate --repo-path . --file-docs --guide --verbose
```

### Example: Analyzing a Repository

To analyze an external repository (like `C:\repos\example-project`):

1. Select **Analyze Repository**.
2. Run or debug; VSCode will execute:

```bash
python main.py analyze C:\repos\example-project
```

### Example: Validating Configs

To check your configuration is valid:

1. Choose **Validate Configuration**.
2. Click run—executes:

```bash
python main.py validate-config
```

---

**Note:**  
To add or modify tasks, edit this `.vscode/launch.json` and reload or reopen your VSCode workspace.

---

## Summary Table of Tasks

| Name                                     | Task                        | Arguments/Flags                                                    |
| ----------------------------------------- | --------------------------- | ------------------------------------------------------------------ |
| Generate File Documentation Only          | Doc generation              | `generate --repo-path . --file-docs --verbose`                     |
| Generate All Docs for Therapy-Link        | Full doc generation         | `generate --repo-path <path> --docs-path <path> --file-docs --guide --force-full-guide --verbose` |
| Generate All Docs for Therapy-Link (Linux)| Full doc generation (Linux) | As above, Linux paths                                              |
| Generate Design Docs                     | Design doc generation       | `generate --repo-path . --design-docs --verbose`                   |
| Generate Guide                           | Guide generation            | `generate --repo-path . --docs-path documentation_output --guide --verbose` |
| Generate File Docs + Guide               | Both file docs and guide    | `generate --repo-path . --file-docs --guide --verbose`             |
| Generate File Docs + Design Docs + Guide | All doc types               | As above, plus `--design-docs`                                     |
| Analyze Repository                       | Repository analysis         | `analyze <path>`                                                   |
| Validate Configuration                   | Config validation           | `validate-config`                                                  |

---

**For further configuration options**, refer to the [VSCode launch documentation](https://code.visualstudio.com/docs/editor/debugging#_launchjson-attributes).

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: 655e8167354652f3ff27123ecc0d7d890914815788a09612e106dfaf2152a55e
relative_path: .vscode/launch.json
generation_date: 2025-06-30T02:48:55.406792
```
<!-- END GENERATION METADATA -->
