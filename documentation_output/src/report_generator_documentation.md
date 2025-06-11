<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for src\report_generator.py

# src/report_generator.py Documentation

## Purpose
The `ReportGenerator` class encapsulates all logic for finalizing and reporting the results of a documentation‐generation pipeline. It handles:
- Creating output directories
- Saving individual file documentation (if incremental saving is disabled)
- Generating a human‐readable summary report (`documentation_report.md`)
- Printing CLI status updates
- Reporting on design documentation (if enabled)

This module exists to centralize post‐processing and reporting responsibilities so that the pipeline core can remain focused on content generation.

---

## Functionality

### Class: ReportGenerator
#### `__init__(self, config)`
- **Purpose**: Initialize the report generator.
- **Parameters**:
  - `config` (any): Global configuration object providing sections such as `design_docs` and `processing`.

Sets up:
- `self.config`: Reference to the configuration.
- `self.logger`: A `logging.Logger` for debug/info messages.

#### `save_results(self, state: PipelineState, file_processor) -> dict`
- **Purpose**: Finalize the documentation run by:
  1. Creating the output folder structure.
  2. Optionally saving each file’s documentation if incremental saving is off.
  3. Generating the summary report file.
  4. Printing a summary of successes and failures.
  5. Reporting on design documentation (if present).
- **Parameters**:
  - `state` (`PipelineState`): Holds `results`, `request`, and optional `design_documentation_state`.
  - `file_processor` (object): Must implement `save_single_result(state, result)` to save individual docs.
- **Returns**: `{"completed": True}` upon completion.

#### `report_design_documentation_status(self, state: PipelineState)`
- **Purpose**: Print a breakdown of design‐doc generation status to the console.
- **Parameters**:
  - `state` (`PipelineState`): Must include `design_documentation_state` with a list of generated docs and sections.
- **Behavior**:
  - Prints configured vs. enabled/disabled document types.
  - Summarizes successes/failures at both document and section levels.
  - Lists individual errors for failed docs.

#### `generate_summary_report(self, state: PipelineState)`
- **Purpose**: Create a Markdown report (`documentation_report.md`) summarizing:
  - Total files processed
  - Successfully documented files
  - Skipped files (no changes)
  - Failed files and their error messages
  - Design‐doc summary (delegates to `generate_design_docs_report_section`)
  - Existing documentation context (if any)
  - Processing configuration details
- **Parameters**:
  - `state` (`PipelineState`): Must include `results`, `request`, optional `existing_docs`, optional `design_documentation_state`.
- **Behavior**:
  - Builds a multi‐section Markdown string.
  - Writes it to `state.request.output_path / "documentation_report.md"`.
  - Prints confirmation to console.

#### `generate_design_docs_report_section(self, state: PipelineState) -> str`
- **Purpose**: Produce the "Design Documentation" subsection for the summary report.
- **Parameters**:
  - `state` (`PipelineState`): Includes `design_documentation_state`.
- **Returns**: A Markdown‐formatted string reporting:
  - Configured/enabled/disabled doc types
  - Counts of successes/failures
  - Lists of disabled types, successful docs (with section counts and file paths), and failed docs (with errors and section‐level errors)
  - Aggregate section statistics

---

## Key Components

- **ReportGenerator**: Central class orchestrating final reporting.
- **PipelineState** (imported from `.models`):  
  - `request`: Contains `output_path` (Path), `repo_path`, `config`, `design_docs`, `file_docs`, `guide`.
  - `results`: List of file‐level result objects with attributes `file_path`, `success`, `documentation`, and `error_message`.
  - `design_documentation_state` (optional): Holds `documents`, each having `name`, `success`, `error_message`, `sections`, and optional `file_path`.
  - `existing_docs` (optional): Contains `content`, `token_count`, `summarized`, and `original_docs`.
- **file_processor**: External component expected to provide `save_single_result(state, result)`.

---

## Dependencies

- Python Standard Library:
  - `logging`: For internal logging (though currently print statements are used).
  - `pathlib.Path`: For filesystem path operations.
- Internal Modules:
  - `.models.PipelineState`: Defines the data structures passed into report methods.
- External Runtime:
  - The pipeline orchestrator that provides the `PipelineState` and `file_processor`.
  - A well‐formed `config` object with keys:
    - `design_docs` → `{"documents": {...}}`
    - `processing` → e.g. `{"save_incrementally": bool, "max_files": int}`

**What depends on this file?**  
Typically, the pipeline’s finalization step. Any upstream code that completes documentation generation will call `ReportGenerator.save_results(...)` to persist and report outcomes.

---

## Usage Example

```python
from pathlib import Path
from src.report_generator import ReportGenerator
from src.models import PipelineState
from src.file_processor import FileProcessor  # hypothetical

# 1. Load or build your global config
config = {
    "processing": {"save_incrementally": False, "max_files": None},
    "design_docs": {
        "documents": {
            "architecture": {"enabled": True},
            "api_reference": {"enabled": False},
        }
    },
}

# 2. Instantiate the report generator
reporter = ReportGenerator(config)

# 3. After running the pipeline, assemble a PipelineState
state = PipelineState(
    request=your_request_object,       # must include output_path, repo_path, etc.
    results=your_file_results_list,    # list of file‐level result objects
    design_documentation_state=your_design_state,  # optional
    existing_docs=your_existing_docs   # optional
)

# 4. Optionally create a file_processor with save_single_result()
file_processor = FileProcessor()

# 5. Finalize and write reports
result = reporter.save_results(state, file_processor)
assert result["completed"] is True
```

---

_End of Documentation_

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: c04fe5bc868ce4b0b7a060ff64e8c329ac722af1948b4f8c009c6b7ac57dc2ce
relative_path: src\report_generator.py
generation_date: 2025-06-10T22:39:31.544247
```
<!-- END GENERATION METADATA -->
