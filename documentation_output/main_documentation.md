<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for main.py

# main.py Documentation

## Purpose

The `main.py` file serves as the command-line interface (CLI) entry point for the documentation generation toolkit. It provides three primary subcommands:

- **generate**: Run a full documentation generation pipeline.
- **analyze**: Inspect and report on a code repository’s structure.
- **validate-config**: Verify the configuration file and API key setup.

This file orchestrates argument parsing, dispatches to the appropriate workflows, and handles high-level error reporting.

---

## Functionality

1. **Argument Parsing**  
   - Determines whether to use _subcommand_ parsing (`generate`, `analyze`, `validate-config`) or _direct_ parsing (backward compatibility for the `generate` command).  
   - Defines and injects common and command-specific arguments using `argparse`.

2. **Command Dispatch**  
   - Based on the parsed `args.command`, invokes one of:
     - `run_documentation_generation(args)`
     - `run_repository_analysis(args)`
     - `run_config_validation(args)`

3. **Error Handling**  
   - Catches keyboard interrupts and other exceptions to print user-friendly messages.  
   - Optionally prints stack traces if the `--verbose` flag is enabled.

---

## Key Components

### 1. `main()`
- Entry point when `main.py` is executed.
- Chooses parsing mode, dispatches to subcommands, and wraps execution in exception handlers.

### 2. Argument-Builder Functions
- `create_subcommand_parser()`: Builds an `ArgumentParser` with three subcommands: `generate`, `analyze`, `validate-config`.
- `create_direct_parser()`: Builds a backward-compatible `ArgumentParser` for `generate` only.
- `add_generate_arguments(parser)`: Injects common arguments used by the `generate` subcommand.

### 3. Command Runners
- `run_documentation_generation(args)`
  - Validates that at least one doc type flag (`--file-docs`, `--design-docs`, `--guide`) is set.
  - Verifies repository and docs paths.
  - Instantiates `DocumentationPipeline(config_path)` and runs it.
  - Summarizes results: counts of generated, skipped, and failed files.
- `run_repository_analysis(args)`
  - Loads configuration via `ConfigManager`.
  - Uses `CodeAnalyzer` to scan and analyze file structure.
  - Prints metrics: total files, breakdown by extension and directory, largest files, and any configured processing limits.
- `run_config_validation(args)`
  - Loads and prints configuration details (model provider, temperature).
  - Tests the presence and validity of the API key.
  - Displays processing limits, supported extensions, exclude patterns, and design-doc settings.

---

## Dependencies

### Standard Library
- `argparse` — CLI argument parsing.
- `sys` — Access to command‐line arguments and exit.
- `pathlib.Path` — Filesystem path manipulations.

### Local Modules (in `src/`)
- `DocumentationPipeline` (in `src/pipeline.py`)  
- `ConfigManager` (in `src/config.py`)  
- `CodeAnalyzer` (in `src/code_analyzer.py`)  
- `DocumentProcessor` (in `src/document_processor.py`)  

_No other project files depend on `main.py`; it is the top‐level launcher._

---

## Usage Examples

### 1. Generate Documentation
```
# File docs only
python main.py generate -r /path/to/repo -f

# Design docs only
python main.py generate -r /path/to/repo -D

# Both file & design docs, and a guide
python main.py generate \
  -r /path/to/repo \
  -f -D -g \
  -c custom_config.yaml \
  -d /path/to/existing_docs \
  -o /path/to/output_docs \
  --verbose
```

### 2. Analyze Repository Structure
```
python main.py analyze /path/to/repo \
  --config custom_config.yaml
```

### 3. Validate Configuration
```
python main.py validate-config \
  --config custom_config.yaml
```

### 4. Backward Compatibility (Direct Parsing)
```
# Equivalent to `generate -r /path/to/repo -f`
python main.py -r /path/to/repo -f
```

---

*End of `main.py` documentation.*

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: 7e929a51da90d7040bd515957ceef0b0e69dbee8b131d4baebdee2aa84ffa05f
relative_path: main.py
generation_date: 2025-06-10T21:51:43.125410
```
<!-- END GENERATION METADATA -->
