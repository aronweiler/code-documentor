<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for documentation_output/.documentation_state/guide_metadata.json

# `guide_metadata.json` Documentation

## Purpose

The `guide_metadata.json` file serves as the central metadata registry for documentation generation within the project. It records tracking information for each source file that is documented, capturing details about their state, corresponding documentation, and various hash/timestamp values to facilitate incremental and consistent doc generation. This enables the documentation system to detect when files have changed and require regeneration, and to manage the relationship between source files and their documentation outputs.

## Functionality

This file is a JSON-encoded object containing:

- Global metadata for the documentation generation process (e.g., timestamps, versioning).
- A comprehensive mapping (`tracked_files`) of each tracked source file to metadata about its documentation state.

It is meant to be machine-generated and maintained exclusively by the documentation tools/processes, which read and update it during doc generation cycles.

## Key Components

### Top-Level Fields

- **guide_last_generated**:  
  A Unix timestamp (float) indicating when the guide/documentation set was most recently generated.

- **guide_version**:  
  An integer specifying the version of the documentation guide format/schema.

- **guide_structure_hash**:  
  Currently an empty string, intended to store a hash representing the structure or significant content of the overall documentation guide. Used for change detection/integrity in advanced scenarios.

- **tracked_files**:  
  An object mapping source file paths to their corresponding documentation metadata.

### tracked_files (Object)

Each key is a relative path to a source file. The value is an object with these properties:

- **source_file_path**:  
  The relative path to the source file being documented.

- **source_file_modified**:  
  Last modification time of the source file (Unix timestamp, float).

- **doc_file_path**:  
  The path where documentation for this file is/will be generated.

- **doc_generated**:  
  A Unix timestamp (float) indicating when the documentation for this file was last generated.

- **doc_file_hash**:  
  A hash of the most recently generated documentation file (for change tracking).

- **guide_entry_generated**:  
  A Unix timestamp (float) of when the guide metadata entry for this file was last updated/generated.

- **guide_entry_hash**:  
  A hash identifying the state/content of this guide metadata entry (for change detection or cache validation).

## Dependencies

### This file depends on:
- The documentation generation system or tool, which updates this file.
- Source files and their associated documentation outputs within the project.

### This file is used by:
- The documentation generator itself, to determine which files need updating, track history, and connect source code to documentation.
- Any automated processes related to documentation integrity, incremental generation, or CI/CD documentation pipelines.

## Usage Examples

### For Documentation Tooling (Automated)

When you run the documentation generator or an update script:

1. **Load `guide_metadata.json`** to get the current state of all tracked files and documentation.
2. For each file in the codebase:
    - Compare `source_file_modified` to the current modification time on disk.
    - If newer, (re-)generate documentation, update `doc_file_path`, `doc_generated`, `doc_file_hash`, etc.
3. Update `guide_last_generated` after the run.

#### Pseudocode Example

```python
with open("documentation_output/.documentation_state/guide_metadata.json") as f:
    metadata = json.load(f)

for file, info in metadata["tracked_files"].items():
    current_mtime = os.path.getmtime(file)
    if current_mtime > info["source_file_modified"]:
        # Source changed, re-generate docs!
        doc_path = info["doc_file_path"]
        generate_docs_for_file(file, doc_path)
        # Update the info dict fields accordingly

metadata["guide_last_generated"] = time.time()
# Write back the updated metadata
```

### For Manual Inspection

If a user wishes to confirm which files have up-to-date docs:
- Review the `tracked_files` section for each relevant file.
- Compare `source_file_modified` and `doc_generated` to see if documentation may be out of date.

## Summary Table of Key Fields

| Field                       | Description                                                                               |
|-----------------------------|-------------------------------------------------------------------------------------------|
| guide_last_generated        | Last full documentation generation timestamp                                              |
| guide_version               | Version of the guide metadata schema                                                     |
| guide_structure_hash        | Hash of the overall documentation structure (for integrity/change detection)              |
| tracked_files               | Map of each source file to its documentation metadata                                    |
| └─ source_file_path         | Relative path to the tracked source file                                                 |
| └─ source_file_modified     | Last modification time of the source file                                                |
| └─ doc_file_path            | Path to the generated documentation for the source file                                  |
| └─ doc_generated            | Timestamp of last documentation generation for that file                                 |
| └─ doc_file_hash            | Hash of the documentation file (for cache and integrity)                                 |
| └─ guide_entry_generated    | Timestamp when the guide entry for this file was last generated/updated                  |
| └─ guide_entry_hash         | Hash of this guide metadata entry (for content/incremental update validation)            |

---

**NOTE:**  
Users should not edit this file directly. All changes are made programmatically by the documentation tooling to ensure consistency and correctness throughout the documentation update process.

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: a05cdfb86025b16cc515a871098a4a1846733feffab350fbe93fdcf7bc3a67ba
relative_path: documentation_output/.documentation_state/guide_metadata.json
generation_date: 2025-06-30T02:49:11.729447
```
<!-- END GENERATION METADATA -->
