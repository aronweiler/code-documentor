<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for main.py

# main.py

## Purpose

This file is the **command-line entry point** for the documentation generation toolkit. It orchestrates the overall process of generating, cleaning, and managing technical documentation for code repositories. It handles argument parsing, command dispatch, and connects the appropriate pipeline components depending on user input.

---

## Functionality

`main.py` provides the following core command-line functionality:

- **Documentation Generation** (`generate`): Invokes the main pipeline to create and update documentation for the target code repository, including file-level docs, design docs, and a documentation guide.
- **Repository Analysis** (`analyze`): Analyzes the structure of a code repository (file counts, directories, extensions, largest files), optionally enforcing config-defined processing limits.
- **Configuration Validation** (`validate-config`): Checks the documentation tool's configuration file and API key validity, ensuring dependencies and model access are correctly specified.
- **Cleanup Orphaned Docs** (`--cleanup`): Deletes documentation files that have no corresponding source files, cleans empty directories, and updates or removes the documentation guide as appropriate.

The CLI supports both **subcommand-style** (`main.py generate ...`) and **direct-argument** (`main.py -r ...`) invocations for backward compatibility.

---

## Key Components

### Functions

- **main**  
  Main entry point. Dispatches control to a command based on parsed arguments.

- **add_generate_arguments(parser)**  
  Adds arguments relevant to documentation generation to the provided `argparse` parser.

- **create_subcommand_parser()**  
  Builds an `argparse` parser supporting structured subcommands (`generate`, `analyze`, `validate-config`).  
  *Provides*:  
    - Examples in help/epilog  
    - User-friendly argument structure  
    - Consistent help output

- **create_direct_parser()**  
  Builds a parser for the older, direct-argument CLI (i.e., without subcommands), just for the `generate` workflow.

- **run_documentation_generation(args)**  
  Core function that manages and invokes the documentation pipeline via `DocumentationPipeline`. Handles cleanup operations and validates sufficient argument combinations.

- **run_cleanup(args)**  
  Implements the `--cleanup` operation:
    - Scans source files in the repo to determine required docs
    - Compares to current documentation output
    - Removes orphaned docs and empty directories
    - Regenerates or removes the documentation guide accordingly

- **run_repository_analysis(args)**  
  Analyzes a repository using `CodeAnalyzer`. Prints stats about file types, sizes, and organization. Highlights files that would be processed based on config.

- **run_config_validation(args)**  
  Loads and checks configuration for validity, printing key model/provider settings and credentials. Catches missing API keys and flags configuration errors.

---

### Imported Modules/Classes

- **argparse, sys, Path**: Standard Python utility modules for CLI and path handling.
- **src.pipeline.DocumentationPipeline**: Main class to orchestrate documentation generation workflows.
- **src.config.ConfigManager**: Handles config file loading and validation.
- **src.code_analyzer.CodeAnalyzer**: Scans and analyzes the codebase structure.

- **Dynamically imported for guide generation (within `run_cleanup`)**:
  - `src.guide_generator.GuideGenerator`
  - `src.document_processor.DocumentProcessor`
  - `src.llm_manager.LLMManager`
  - `src.models` (for `DocumentationResult`, `PipelineState`, etc.)

---

## Dependencies

This file depends on:

- Internal modules:
  - `src.pipeline`
  - `src.config`
  - `src.code_analyzer`
  - (During cleanup: `src.guide_generator`, `src.document_processor`, `src.llm_manager`, `src.models`)
- Configuration file (default: `config.yaml`) for pipeline options and credentials.
- A directory structure with code and, optionally, preexisting documentation.

Other files and scripts (e.g., `mcp_server.py`, test scaffolding) and downstream documentation browsers/tools depend on this entry point for generating and updating the docs.

---

## Usage Examples

### Generating Documentation

**Subcommand Style:**
```bash
# Generate docs for all files and the guide
python main.py generate -r /path/to/repo -f -D -g

# Generate only file-level docs
python main.py generate -r /path/to/repo -f

# Generate only design docs
python main.py generate -r /path/to/repo -D

# Generate the documentation guide
python main.py generate -r /path/to/repo -g
```

**Legacy/Direct Style:**
```bash
python main.py -r /path/to/repo -f -g
```

### Cleanup Orphaned Documentation

```bash
# Remove documentation for source files that no longer exist, update guide
python main.py generate -r /path/to/repo --cleanup

# Or, using the direct/legacy syntax:
python main.py -r /path/to/repo --cleanup
```

### Analyze a Repository

```bash
python main.py analyze /path/to/repo
```

### Validate Configuration

```bash
python main.py validate-config
```
You can specify a non-default config:

```bash
python main.py validate-config --config myconfig.yaml
```

---

## Design Notes

- **Backward Compatibility**: Supports both subcommands and the direct-argument CLI for users upgrading from earlier versions.
- **Graceful Exception Handling**: Handles keyboard interrupts (`Ctrl+C`) and prints full tracebacks in verbose mode for easier troubleshooting.
- **User Guidance**: All major actions echo the current operation, show status, and use emojis for accessibility.
- **Separation of Concerns**: Argument parsing and command dispatching are handled separately, while business logic is delegated to pipeline/utility modules.

---

## Typical Workflow

1. **User runs** `python main.py generate ...` to generate/update docs
2. **Pipeline** scans the repository, runs LLM analysis, produces documentation files and (optionally) a guide
3. **If files were deleted**: `--cleanup` will remove orphaned docs, clean output directories, and update the guide
4. **Analysis/validation** commands help inspect repository structure and configuration health
5. **Results**: Individual `*_documentation.md` files, updated design docs, and a `documentation_guide.md` are created/updated

---

## See Also

- [Documentation Cleanup Feature Test](#) – for specific details on cleanup feature
- Project's detailed README and guide for info on MCP server usage, configuration, and scripting

---

**Entrypoint:**  
```python
if __name__ == "__main__":
    main()
```

---

This file forms the essential **interface between user intent and the documentation system** for large codebases. All major operations—generation, cleanup, validation, and analysis—are available from this script, making it central to repository documentation management in this project.

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: c6d3298884b8df33fa6a86c1b56e7b5bd14ac995527955e73f64c536761d9909
relative_path: main.py
generation_date: 2025-07-01T23:19:54.443664
```
<!-- END GENERATION METADATA -->
