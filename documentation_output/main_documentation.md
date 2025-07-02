<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for main.py

# main.py

## Purpose

`main.py` is the **entry point** for the documentation generation toolkit in this project. Its primary purpose is to provide a command-line interface (CLI) for generating, analyzing, and cleaning up documentation for a source code repository. It orchestrates actions such as generating comprehensive documentation, cleaning orphaned documentation files, validating the configuration, and analyzing repository structure.

This file ensures users can easily manage code documentation via simple terminal commands with flexible subcommands and arguments.

---

## Functionality

### Overview of Main Features

- **Documentation Generation**: Generate file-level, design, and/or documentation guide outputs for a repository.
- **Cleanup Routine**: Remove orphaned documentation files corresponding to deleted source files (`--cleanup` feature).
- **Repository Analysis**: Analyze the repository's source file structure (counts by extension/directory, largest files, etc.).
- **Configuration Validation**: Check that configuration files (and API keys) are valid and that the environment is set up properly.
- **Flexible CLI Interface**: Accepts both modern subcommand-style arguments and legacy direct arguments for compatibility.

### Main Function

#### `main()`

- Detects how to parse arguments (subcommand mode vs. legacy mode).
- Parses CLI arguments and dispatches to the appropriate action:
    - `generate` &rarr; `run_documentation_generation()`
    - `analyze` &rarr; `run_repository_analysis()`
    - `validate-config` &rarr; `run_config_validation()`
- Handles exceptions gracefully, including keyboard interrupts and errors with verbose traceback if requested.

### Argument Parsers

- **`create_subcommand_parser()`**:  
  Builds a parser supporting explicit subcommands (`generate`, `analyze`, `validate-config`), each with its own arguments and help text.
  
- **`create_direct_parser()`**:  
  Provides backward-compatible parsing for direct flags (shortcut for always running the `generate` command).

- **`add_generate_arguments(parser)`**:  
  Adds shared arguments for documentation generation (e.g., repo path, output path, various flags).

### Documentation Pipeline

#### `run_documentation_generation(args)`

- Verifies input paths and argument combinations are valid.
- Initializes the documentation pipeline (`DocumentationPipeline`) and triggers the documentation process as requested:
    - Individual file documentation (`--file-docs`)
    - Design documentation (`--design-docs`)
    - Documentation guide (`--guide`)
    - Cleanup orphaned documentation (`--cleanup`)
- Outputs a summary of the result: how many files were generated, skipped, or failed.

#### `run_cleanup(args)`

- Implements the `--cleanup` feature:
    - Scans source code files and maps expected documentation outputs.
    - Identifies documentation files that no longer correspond to an existing source file.
    - Removes orphaned documentation files and cleans up empty directories.
    - Updates (or removes) the documentation guide as needed to reflect removed files.

### Repository & Config Utilities

#### `run_repository_analysis(args)`

- Analyzes and outputs a summary of:
    - Total files
    - Count of files by extension and by directory
    - Largest source files
    - Whether the configured processing limit is met or exceeded

#### `run_config_validation(args)`

- Loads and validates the configuration file.
- Checks API key connectivity and displays masked API key.
- Reports on configuration items: file extensions, exclude patterns, model/provider, etc.

---

## Key Components

| Component           | Description                                                                                 |
|---------------------|--------------------------------------------------------------------------------------------|
| **DocumentationPipeline** | Orchestrates the full documentation generation workflow. Imported from `src.pipeline`.    |
| **ConfigManager**          | Loads and validates configuration files and model API keys. Imported from `src.config`.    |
| **CodeAnalyzer**           | Scans the repository and analyzes the file structure. Imported from `src.code_analyzer`. |
| **GuideGenerator, DocumentProcessor, LLMManager** | Used for documentation guide regeneration during cleanup.                       |
| **argparse**               | Standard Python module for parsing CLI arguments.                                        |

---

## Dependencies

- **`src.pipeline`**: For the main documentation generation process.
- **`src.config`**: For configuration handling and API key management.
- **`src.code_analyzer`**: For repository analysis and file discovery.
- **`src.guide_generator`, `src.document_processor`, `src.llm_manager`, `src.models`**: Used internally, especially for guide regeneration during cleanup.
- **Standard library**: `argparse`, `sys`, `pathlib`, `traceback`.

### What depends on `main.py`:

- This script is intended to be run directly (`python main.py ...`) as the command-line interface to the toolkit.
- Other scripts or launch configurations (e.g., VS Code, MCP server setups, CLI wrapper scripts) may call this file as their entry point.

---

## Usage Examples

### Documentation Generation

```bash
# Generate individual file docs only
python main.py generate -r path/to/repo -f

# Generate design docs only
python main.py generate -r path/to/repo -D

# Generate both file and design docs
python main.py generate -r path/to/repo -f -D

# Only documentation guide
python main.py generate -r path/to/repo -g

# All outputs, with explicit config and custom output location
python main.py generate -r path/to/repo -f -D -g -c alternate-config.yaml -o path/to/output
```

Short syntax for backward-compatible invocation:

```bash
python main.py -r path/to/repo -f -D -g
```

### Orphaned Documentation Cleanup

```bash
python main.py generate -r /path/to/repo --cleanup
```

Or with classic syntax:

```bash
python main.py -r /path/to/repo --cleanup
```

### Repository Analysis

```bash
python main.py analyze /path/to/repo
```

### Configuration Validation

```bash
python main.py validate-config --config my-config.yaml
```

---

## Typical Workflow

1. **Validate Config** (optional but recommended):  
   `python main.py validate-config`

2. **Analyze Repository** (optional for inspection):  
   `python main.py analyze /path/to/repo`

3. **Generate Documentation**:  
   `python main.py generate -r /path/to/repo -f -D -g`

4. **Clean Up Orphaned Docs** (as needed):  
   `python main.py -r /path/to/repo --cleanup`

---

## Additional Notes

- **Error Handling**: Displays human-friendly error messages, with stack traces if `--verbose` is enabled.
- **Incremental/Selective Generation**: Flag combinations control what gets generated.
- **Integrated Cleanup**: `--cleanup` can be run alone or combined with other generation flags.
- **Comprehensive Help**: Argument parsers provide detailed usage examples and help info.

---

## Conclusion

The `main.py` script is the command-line "front door" to the entire automated documentation solution. It unifies documentation workflows, repository introspection, robust configuration validation, and orphaned documentation maintenance—all in a user-friendly CLI package.

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: f93397c858e522b95e84b2973b7e1ca491a59b686c5aef042d1653d0d356176b
relative_path: main.py
generation_date: 2025-07-01T23:04:41.254654
```
<!-- END GENERATION METADATA -->
