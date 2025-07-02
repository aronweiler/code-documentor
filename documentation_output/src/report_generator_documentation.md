<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for src\report_generator.py

# `report_generator.py`

## Purpose

This module defines the `ReportGenerator` class, which is responsible for generating documentation summary reports and reporting the status of file and design documentation generation in a documentation pipeline. It centralizes the logic for saving results, reporting processing outcomes, and assembling comprehensive Markdown summary reports. The reports are designed to aid users in quickly understanding the outcome of a documentation generation run.

---

## Functionality

### Overview

- **Saving Results:** Manages the saving of file documentation and/or design documentation files, depending on configuration.
- **Summary and Status Reporting:** Creates a human-readable Markdown report summarizing the overall process, including successes, failures, and skipped files.
- **Design Documentation Status:** Reports detailed progress on the generation of higher-level design docs and their sections.

### Main Class: `ReportGenerator`

#### `__init__(self, config)`

Initializes the report generator with a configuration object.

- **Parameters:**
  - `config`: An object containing project and reporting configuration.


#### `save_results(self, state: PipelineState, file_processor) -> dict`

Manages the saving of results at the end of the documentation pipeline.

- Outputs the documentation files into the desired directory.
- Handles both incremental and non-incremental saving (i.e., saving files as they are processed or all at once at the end).
- Triggers generation of the summary Markdown report.
- Reports both file-level and design documentation status using helper methods.
- Prints overall summary to the console.
- **Returns:** A dict indicating completion (`{"completed": True}`).


#### `report_design_documentation_status(self, state: PipelineState)`

Prints the status of the design documentation generation to the console, including per-document and per-section statistics, highlighting enabled/disabled configurations, and reporting failures with error details.


#### `generate_summary_report(self, state: PipelineState)`

Generates a detailed Markdown summary report of the documentation run and writes it to `documentation_report.md` in the output directory.

- Includes file documentation success, failures, and skips.
- Appends additional statistics—design documentation, configuration, and pre-existing docs context.


#### `generate_design_docs_report_section(self, state: PipelineState) -> str`

Returns a Markdown-formatted string containing a summary of the design documentation generation, including document and section-level statistics and lists of enabled/disabled/failing docs.

---

## Key Components

- **Class: `ReportGenerator`**  
  Main interface for report and status generation.

- **Methods:**
  - `save_results`
  - `report_design_documentation_status`
  - `generate_summary_report`
  - `generate_design_docs_report_section`
  
- **Input types and references:**
  - Uses an instance of `PipelineState` (from `.models`) as the main state object.
  - Expects a `file_processor` object responsible for saving individual file results.
  - Relies on configuration provided as a constructor argument.

- **Output:**
  - Standard output (console).
  - Markdown report file (`documentation_report.md`).

- **Data Structures:**
  - `state.results`: File documentation results (list of result objects with at least `.success`, `.documentation`, `.file_path`, `.error_message`).
  - `state.design_documentation_state`: Design documentation generation outcome.
  - `state.request`: Contains request configuration details (such as output and repo paths, enabled features, config dictionaries).
  - `state.existing_docs`: Context around existing documentation in the repository.


---

## Dependencies

### Imports

- **Standard:** `logging`, `pathlib.Path`
- **Internal:** `.models.PipelineState`

### Internal Coupling

- **Depends on:**
  - `.models.PipelineState` and its nested/requested attributes, as well as result types for both file and design documentation.
  - An external `file_processor` for saving individual file-level documentation results.

- **Is Depended on by:**
  - The documentation pipeline's main controller or entry point, which should instantiate and use `ReportGenerator` as needed.

---

## Usage Examples

### Basic Example

```python
from report_generator import ReportGenerator
from models import PipelineState

# ...setup your config, state, and file_processor somehow...

reporter = ReportGenerator(config)
result = reporter.save_results(state, file_processor)
# This will:
# - Save all documentation results as files
# - Print a summary to the console
# - Write a Markdown summary report to <state.request.output_path>/documentation_report.md
```

### Integrating into a Pipeline

Typical usage is as the last step in a processing pipeline:

```python
def main(config, state, file_processor):
    # ... after processing all files/docs
    report_generator = ReportGenerator(config)
    result = report_generator.save_results(state, file_processor)
    if result["completed"]:
        print("All reports finalized. See documentation_report.md for details.")
```

---

## Additional Notes

- All reports are written in Markdown (`documentation_report.md`) in the output path.
- The implementation supports tracking skipped files (no changes), failures (with error details), and design documentation statistics.
- Configuration-driven: respects flags like `save_incrementally`, `max_files`, and toggles for design docs and guides.
- Console output informs the user of high-level results and errors.
- The precise schema for `PipelineState` and results must align with the code's expectations (attributes such as `.success`, `.error_message`, `.file_path`, `.sections`, etc.).


---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: c04fe5bc868ce4b0b7a060ff64e8c329ac722af1948b4f8c009c6b7ac57dc2ce
relative_path: src\report_generator.py
generation_date: 2025-07-01T22:20:11.113094
```
<!-- END GENERATION METADATA -->
