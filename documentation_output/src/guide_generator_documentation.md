<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for src/guide_generator.py

# guide_generator.py

## Purpose

The `guide_generator.py` module manages the creation, updating, and summarization of a **project-level documentation guide**. It compiles per-file documentation into a unified guide, computes documentation summaries using Large Language Models (LLMs), and supports both full and incremental updates in response to codebase changes. This guide provides an index and overview of the generated file documentation across a code repository.

---

## Functionality

The main responsibilities covered by this module are:

- **Loading Existing Documentation**: Reads already-generated documentation files, extracting their content and metadata.
- **Guide Generation**: Creates a guide by summarizing documentation for each source file using an LLM, then compiles these into a Markdown file.
- **Guide Updating**: Detects changes in the codebase and updates only the relevant entries in the documentation guide, supporting incremental updates.
- **Metadata Management**: Works with a metadata manager to track the status and coverage of documentation.
- **Error Handling**: Provides robust logging and error handling for loading, summarizing, and parsing documentation.

---

## Key Components

### 1. **GuideGenerator Class**

This is the central class of the module, orchestrating all guide-related operations.

#### Initialization

```python
def __init__(self, llm, config, doc_processor)
```
- `llm`: LLM instance for summarization (ChatOpenAI or ChatAnthropic)
- `config`: Pipeline configuration object
- `doc_processor`: A `DocumentProcessor` that helps with doc context

#### Loading Documentation

- `load_existing_documentation(state)`: Loads all existing documentation results and contexts from disk for use in guide generation.
- `load_existing_documentation_results(state)`: Loads the content and metadata of all documentation files found under the output directory.

#### Guide Generation

- `generate_documentation_guide(state)`: Generates the full documentation guide by summarizing all documentation files.
- `save_documentation_guide(state, guide)`: Saves the guide to a Markdown file in the documentation output directory.

#### Incremental Updates

- `detect_guide_changes(state)`: Uses `GuideMetadataManager` to detect which docs have been added/changed/removed since last guide build.
- `generate_incremental_guide(state)`: Efficiently updates only those parts of the guide affected by recent changes.

#### Entry/Summary Helpers

- `_generate_doc_summary(doc_content, file_path)`: Uses the LLM to generate a summary of a documentation content blob.
- `_generate_single_guide_entry(state, result)`: Creates a guide entry for a single documentation result.
- `_generate_guide_entry_for_file(state, relative_path)`: Generates a guide entry for an arbitrary file (not just those in pipeline results).
- `_clean_documentation_content(doc_content)`: Strips headers, code, and metadata to prepare content for summarization.

#### Miscellaneous

- `extract_metadata_from_doc(doc_path)`: Loads and parses YAML (or fallback HTML) metadata from a documentation file.
- `_parse_guide_entries(guide_content)`: Extracts entries from an existing guide file.
- `_get_metadata_manager(output_path)`: Helper for cached metadata manager.

---

### 2. **Supporting Classes/Types**

These are imported from nearby modules and used as models or processors:

- `PipelineConfig`, `PipelineState`, `DocumentationResult`, `DocumentationGuide`, `DocumentationGuideEntry`, `ChangeSet`: Typed data models.
- `DocumentProcessor`: Utility class for handling the documentation content.
- `GuideMetadataManager`: Handles incremental guide generation and metadata storage.

### 3. **Key Variables and Constants**

- `GENERATE_DOC_SUMMARY_SYSTEM_MESSAGE`: Injected prompt for LLM summarization, imported from a prompt template module.
- Logging is performed throughout via the standard Python `logging` module.

---

## Dependencies

### Required Imports and Their Uses

- **Standard Library**: `datetime`, `hashlib`, `logging`, `re`, `os`, `pathlib.Path`
- **Third-Party**:
  - `langchain_openai`, `langchain_anthropic`: For LLM chat instances.
  - `langchain_core.messages`, `langchain_core.prompts`: For prompt and message construction.
- **Local Modules**:
  - `.models`, `.document_processor`, `.guide_metadata_manager`, `.prompts.generate_doc_summary_system_message`: Project-specific models/utilities.

### Module Integration

- **Upstream/Dependent modules**: Other parts of the codebase will instantiate `GuideGenerator` and use its functions to manage or update the documentation guide.
- **Downstream use**: This module writes new files to disk (guide files) and may be called as part of a larger document generation pipeline.

---

## Usage Examples

```python
from guide_generator import GuideGenerator
from my_project.models import PipelineConfig, PipelineState
from my_project.document_processor import DocumentProcessor

# Set up your LLM and config
llm = ChatOpenAI(...)                         # or ChatAnthropic(...)
config = PipelineConfig(...)
doc_processor = DocumentProcessor(...)

# Suppose you have a PipelineState from your orchestration
state = PipelineState(...)

# Create the guide generator
guide_gen = GuideGenerator(llm, config, doc_processor)

# Full documentation guide generation
doc_guide = guide_gen.generate_documentation_guide(state)
guide_gen.save_documentation_guide(state, doc_guide)

# Detect what needs updating for incremental guides
changeset = guide_gen.detect_guide_changes(state)

# Incrementally update the documentation guide
incremental_guide = guide_gen.generate_incremental_guide(state)
guide_gen.save_documentation_guide(state, incremental_guide)

# To load an existing documentation guide
existing_guide = guide_gen._load_existing_guide(state)
```

---

## Notes

- **Extensibility**: The module is designed to work with different LLM backends and can flexibly support new documentation types and guide formats.
- **Error Handling**: Critical steps (file IO, LLM operations) include robust error handling with logging and fallback strategies.
- **Incremental Mode**: Designed for performance and responsiveness, especially in large repositories, by avoiding unnecessary regeneration of unchanged documentation guide entries.

---

## See Also

- [`.document_processor`](./document_processor.py): Utilities for loading and cleaning documentation content.
- [`.guide_metadata_manager`](./guide_metadata_manager.py): Incremental update and change detection logic.
- [`.models`](./models.py): Definitions for all data models used in documentation generation.
- [`.prompts/generate_doc_summary_system_message.py`]: Contains LLM prompt for producing doc summaries.


---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: 2db4b86486144c6c05b0a8482d93b4d70560445941e5ca9ec7aeb850a3148f3a
relative_path: src/guide_generator.py
generation_date: 2025-06-30T02:26:20.998499
```
<!-- END GENERATION METADATA -->
