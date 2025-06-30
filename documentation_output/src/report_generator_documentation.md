<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for src/report_generator.py

# `report_generator.py`

## Purpose

The `report_generator.py` file provides the main reporting logic for a documentation generation pipeline. It is responsible for saving results, generating human-readable summary reports, and reporting the status of both file-level and design-level documentation generation.

This component acts as a central place to finalize output, summarize successes and failures, and provide actionable feedback at the end of a pipeline run. It helps users, developers, and maintainers understand what has been produced, what failed, and where further attention may be needed.

---

## Functionality

The core class, `ReportGenerator`, orchestrates:
- Saving documentation results to output directories.
- Handling both incremental and non-incremental saving modes.
- Generating detailed Markdown summary reports, including stats and breakdowns.
- Detailed reporting for a "design documentation" subsystem, which may feature multiple document types and sections per type.

### Main Methods

#### `__init__(self, config)`
Initializes the report generator with a given configuration. The configuration (`config`) is expected to have at least a `.design_docs` attribute among other settings.

#### `save_results(self, state: PipelineState, file_processor) -> dict`
- Finalizes the documentation run.
- Ensures output directories exist and saves non-incremental results if required.
- Calls other methods to generate the summary report and report on design documentation status.
- Prints summary statistics.
- Returns a dictionary indicating completion.

#### `report_design_documentation_status(self, state: PipelineState)`
- Reports progress and results for all configured design document types and their sections.
- Lists successful and failed documents.
- Prints aggregate statistics.

#### `generate_summary_report(self, state: PipelineState)`
- Gathers summary data about the documentation generation (successes, skips, failures, configuration information, and existing docs context).
- Assembles a Markdown report and writes it to `documentation_report.md` in the output directory.
- Appends the design docs summary via `generate_design_docs_report_section()` if any.

#### `generate_design_docs_report_section(self, state: PipelineState) -> str`
- Returns a Markdown string summarizing the outcomes for design documentation, breaking down by doc type, sections, and error info.

---

## Key Components

### Classes

- **`ReportGenerator`**: Main orchestrator for report generation.
- **PipelineState**: Imported from `.models`. Supplies pipeline and documentation state, including results, configuration, paths, and design doc statuses.

### Methods

See above for methods in `ReportGenerator`.

### Variables

- `self.config`: Pipeline configuration object.
- `self.logger`: Logger for the report generator.
- `state`: Passed PipelineState instance holding the context of the documentation run.
- `file_processor`: External object responsible for file result persistence when incremental saving is disabled.

---

## Dependencies

### Internal

- `.models.PipelineState`: The full state of the documentation pipeline, including results, requests, design documentation state, and existing documentation context.

### External

- `logging`: For logging (mainly logger initialization; print is used for user output).
- `pathlib.Path`: For directory and file path manipulations.

### What Depends on This Module

- Components responsible for running the documentation pipeline will instantiate and use `ReportGenerator` to produce summary output and reporting at the end of execution.

---

## Usage Examples

### Example: Finalizing a Documentation Pipeline

Assume `state` is a `PipelineState` holding the results, and `file_processor` is an object with a `.save_single_result()` method:

```python
from report_generator import ReportGenerator

config = {
    # ... your config here ...
}
generator = ReportGenerator(config)
completion_info = generator.save_results(state, file_processor)

# The summary report will be written to state.request.output_path/documentation_report.md
# Console will output stats and status
```

### Example: Accessing Detailed Reporting (within the pipeline)

You can call:
```python
generator.report_design_documentation_status(state)
```
to print out status messages for only the design documentation results.

---

## Notes

- The report files and directories created are determined by `state.request.output_path` and other fields of the pipeline state/request.
- Configuration expects fields such as `design_docs`, `processing` (with keys like `save_incrementally`, `max_files`), and more.
- The file processor is only used when incremental saving is turned off (`save_incrementally=False`).

---

## Summary

The `report_generator.py` module serves as the completion and reporting engine for a documentation generation pipeline. It ensures that results are saved, users are informed of successes and failures, and that summary information is both machine- and human-readable for ongoing maintenance and improvement efforts.

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: c04fe5bc868ce4b0b7a060ff64e8c329ac722af1948b4f8c009c6b7ac57dc2ce
relative_path: src/report_generator.py
generation_date: 2025-06-30T00:12:29.339887
```
<!-- END GENERATION METADATA -->
