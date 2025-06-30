<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for .vscode\launch.json

# `.vscode/launch.json`

## Purpose

The `.vscode/launch.json` file defines a set of Visual Studio Code debugging configurations for this repository. It specifies how to launch the Python scripts in different modes, allowing developers to streamline running and debugging various command-line tasks (such as generating documentation, validating configuration, or analyzing the repository) directly from the IDE.

This file is essential for maintaining reproducible, consistent development workflows across contributors and environments.

---

## Functionality

The file uses Visual Studio Code’s [debug configuration schema](https://code.visualstudio.com/docs/editor/debugging#_launchjson-attributes) (version `0.2.0`) to define how the IDE should launch the Python debugger (`debugpy`) with specific arguments, working directories, environment variables, and in some cases, different projects or documentation options.

Each entry in the `configurations` array is a separate named launch profile you can select in VS Code’s Debug sidebar.

---

## Key Components

### Top-level Structure

- **version**: The schema version for this file.
- **configurations**: An array of individual debug configuration objects.

### Configuration Properties

Each configuration typically includes:

- `name`: Display name in VS Code’s debug launch menu.
- `type`: The debugger type (always `debugpy` for Python).
- `request`: Always `"launch"` to start a program.
- `program`: The Python script to execute (always `${workspaceFolder}/main.py`).
- `args`: Arguments to pass to the script; these define what operation to run (e.g., `"generate"`, `"analyze"`, `"validate-config"`) and with which flags and paths.
- `console`: Launches in the integrated terminal.
- `cwd`: Working directory for the process (always `${workspaceFolder}`).
- `env`: Sets `PYTHONPATH` to the workspace folder, ensuring correct import resolution.

### Notable Launch Configurations

1. **Generate File Documentation Only**
   - Generates only file-level documentation for the current repository.

2. **Generate All Docs for Therapy-Link**
   - Generates file docs and guide for another repo (`therapy-link`) at a specific path.

3. **Generate Design Docs**
   - Generates only design documentation for the current repository.

4. **Generate Guide**
   - Generates only the documentation guide for the workspace.

5. **Generate File Docs + Guide**
   - Simultaneously generates file-level documentation and guide for the workspace.

6. **Generate File Docs + Design Docs + Guide**
   - Generates file-level docs, design docs, and guide for an external example project.

7. **Analyze Repository**
   - Runs a repository analysis operation on an example project.

8. **Validate Configuration**
   - Performs configuration validation for the project.

---

## Dependencies

### Internal

- **main.py**: All configurations reference `${workspaceFolder}/main.py` as the entrypoint. This script must support the CLI commands described in `args`.

### External

- **VS Code**: The file is specifically for VS Code’s debugging features.
- **debugpy**: Python debugger backend required for these launch configs.
- **Python Environment**: Presumed to be correctly set up and able to import modules via `PYTHONPATH=${workspaceFolder}`.

### Downstream

- Other parts of the repository do not import or depend directly on this file, but VS Code uses it to launch and debug `main.py` tasks.

---

## Usage Examples

### Launch in Visual Studio Code

1. Open the VS Code "Run and Debug" panel.
2. Select the desired configuration by name, for example, `Generate File Documentation Only`.
3. Click the green "Start Debugging" button (or press `F5`).

This will:

- Set the working directory.
- Set the required environment variable.
- Launch `${workspaceFolder}/main.py` with the specified arguments in an integrated terminal with the VS Code Python debugger attached.

### Example: Generating File Docs + Guide

This configuration (`Generate File Docs + Guide`) runs:

```bash
python main.py generate --repo-path . --file-docs --guide --verbose
```
...from the root of your current workspace, under the VS Code debugger.

### Example: Analyzing an External Repository

Configuration (`Analyze Repository`) runs:

```bash
python main.py analyze C:\repos\example-project
```
...ready for step-by-step debugging and inspection.

---

## Summary Table

| Name                                   | Main Purpose                                   | Target Repo/Folder      |
|-----------------------------------------|------------------------------------------------|------------------------|
| Generate File Documentation Only        | File-level docs only                           | Workspace              |
| Generate All Docs for Therapy-Link      | File docs + guide for external repository      | `therapy-link`         |
| Generate Design Docs                    | Design docs only                               | Workspace              |
| Generate Guide                          | Documentation guide only                       | Workspace              |
| Generate File Docs + Guide              | Both file docs and guide                       | Workspace              |
| Generate File Docs + Design Docs + Guide| All docs for external example project          | `example-project`      |
| Analyze Repository                      | Runs repo analysis                             | `example-project`      |
| Validate Configuration                  | Checks/validates current configuration         | Workspace              |

---

## Maintenance Notes

- Update this file when new script entrypoints or documentation modes are added to the `main.py` program.
- Paths are some-times absolute and may need modification on new systems/environments.
- If new contributors use different virtual environment structures, ensure `PYTHONPATH` is set appropriately.

---

## See Also

- [Visual Studio Code Debugging Documentation](https://code.visualstudio.com/docs/editor/debugging)
- [Python debugpy Documentation](https://github.com/microsoft/debugpy)
- [`main.py` CLI/argument documentation](./main.py) (if available)

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: 7f8a4fe81e67a0e9f1721907958748ea66bc5f9fbf5af624c5853d3456048e70
relative_path: .vscode\launch.json
generation_date: 2025-06-29T16:49:57.377575
```
<!-- END GENERATION METADATA -->
