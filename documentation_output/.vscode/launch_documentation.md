<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for .vscode\launch.json

# `.vscode/launch.json` – VS Code Launch Configurations for Documentation Toolkit

## Purpose

This file configures **Visual Studio Code (VS Code) debugging and run profiles** for automating tasks in the documentation generation toolkit (`main.py`). It enables one-click running and debugging of various documentation workflows—such as generating file-level docs, guides, design docs, performing cleanup, and validating configuration—directly within the VS Code IDE.

This improves developer productivity by standardizing commands, eliminating the need for custom terminal commands, and ensuring consistent environments for different documentation scenarios.

---

## Functionality

### What This File Does

- **Defines Launch Profiles:** Each entry in the `configurations` array is a named profile for running or debugging `main.py` with a specific set of arguments and environment variables.
- **Supports Multiple Workflows:** Profiles are tailored for file documentation, design documentation, guide generation, repository cleanup, repository analysis, and configuration validation.
- **Handles Platform-Specific Paths:** Some configurations (e.g., "for Therapy-Link") are set up for Windows and Linux environments.
- **Ensures PYTHONPATH Set:** All profiles configure the environment variable `PYTHONPATH` to the workspace root to ensure Python module resolution.

---

## Key Components

- **`version`**: `"0.2.0"` — The VS Code launch configuration schema version.
- **`configurations`**:  
  An array of profiles, each including:
  - `name`: Display name in the VS Code "Run and Debug" menu.
  - `type`: Always `debugpy` (Python debugger).
  - `request`: Always `launch` (start a new process).
  - `program`: Main Python entry point—always `${workspaceFolder}/main.py`.
  - `args`: Arguments passed to `main.py`, customized per task.
  - `console`: Where output appears (`integratedTerminal` for standard terminal tab).
  - `cwd`: Working directory (always `${workspaceFolder}`).
  - `env`: Environment variables (`PYTHONPATH` set to workspace root).

#### Notable Configurations

- **Generate File Documentation Only**:
  - Runs `main.py generate --repo-path . --file-docs --verbose`
- **Generate All Docs for Therapy-Link (Windows/Linux)**:
  - Runs doc generation targeting the external repository at `H:\repos\therapy-link` (Windows) or `/mnt/h/repos/therapy-link` (Linux), including guides.
- **Generate Design Docs**:
  - Runs `main.py generate --repo-path . --design-docs --verbose`
- **Generate Guide**:
  - Runs `main.py generate --repo-path . --docs-path documentation_output --guide --verbose`
- **Generate File Docs + Guide**:
  - Runs file docs and guide generation together.
- **Generate File Docs + Design Docs + Guide + Cleanup**:
  - Runs all documentation tasks with `--cleanup` to remove orphaned files.
- **Analyze Repository**:
  - Runs analysis on a specified repository (`analyze` command).
- **Validate Configuration**:
  - Runs `validate-config` command to check project setup.

---

## Dependencies

### Depends On

- **Python** with the [debugpy](https://github.com/microsoft/debugpy) extension (used by VS Code).
- **`main.py`**: The toolkit's main command-line file, which must accept all the listed arguments.
- Documentation generator's Python environment and project structure.

### Depended On By

- VS Code developers working in this repository who want convenient F5 (Run/Debug) tasks for documentation generation.
- Any team process that standardizes or automates documentation tasks via VS Code integration.

---

## Usage Examples

### Running a Launch Profile

1. Open VS Code in your project folder.
2. Go to the **Run and Debug** sidebar (`Ctrl+Shift+D`).
3. Select a configuration (e.g., "Generate File Documentation Only") from the dropdown.
4. Click the green "Run/Debug" button or press `F5`.
5. Output and logs appear in the integrated terminal.

### Customizing for Your Repo

Edit `--repo-path` or `--docs-path` as needed for your project's location, or duplicate and modify configurations for new workflows.

---

## Typical Workflow Calls

- **Generate file documentation for current project:**
  - `main.py generate --repo-path . --file-docs --verbose`
- **Generate design docs:**
  - `main.py generate --repo-path . --design-docs --verbose`
- **Full guide generation:**
  - `main.py generate --repo-path . --guide --docs-path documentation_output --verbose`
- **Generate and cleanup docs:**
  - `main.py generate --repo-path . --cleanup --docs-path docs --file-docs --design-docs --guide --verbose`
- **Analyze another repository:**
  - `main.py analyze C:\repos\example-project`
- **Validate project configuration:**
  - `main.py validate-config`

---

## Related Files & Extensions

- `.vscode/tasks.json`: For shell-based commands (see project documentation).
- VS Code Python extension (required for debugpy integration).

---

## Summary Table

| Name                                      | Main Purpose                          | Typical Arguments                                               |
|--------------------------------------------|---------------------------------------|----------------------------------------------------------------|
| Generate File Documentation Only           | File-level docs (source code)         | `generate --repo-path . --file-docs --verbose`                 |
| Generate All Docs for Therapy-Link         | All docs for Windows repo             | Uses full paths with `--file-docs --guide`                     |
| Generate All Docs for Therapy-Link (Linux) | All docs for Linux repo               | Uses Linux paths                                               |
| Generate Design Docs                      | Design documentation only             | `generate --repo-path . --design-docs --verbose`               |
| Generate Guide                            | Documentation guide                   | `generate --repo-path . --docs-path documentation_output --guide --verbose` |
| Generate File Docs + Guide                 | File docs AND guide                   | `--file-docs --guide --verbose`                                |
| Generate File Docs + Design Docs + Guide   | All, with cleanup and most options    | `--cleanup --file-docs --design-docs --guide --verbose`        |
| Analyze Repository                        | Analyze (not generate) on target repo | `analyze C:\repos\example-project`                             |
| Validate Configuration                    | Validate toolkit setup                | `validate-config`                                              |

---

## Notes

- If you add or change options in `main.py`'s CLI, update these configs!
- Paths may need adjustment for different users/OSes.
- For team use, ensure all developers use compatible VS Code plugins and `debugpy` environments.

---

**For further workflow integration or batch scripting, see the `README.md` and project documentation for `.vscode/tasks.json` and CI/CD guidance.**

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: 7117bfdfb50d2ad5faf785207235d93b45bd9fe6667d9c8dc5511213f838d4f3
relative_path: .vscode\launch.json
generation_date: 2025-07-01T23:03:09.623754
```
<!-- END GENERATION METADATA -->
