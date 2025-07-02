<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for src\guide_generator.py

# `guide_generator.py`

## Purpose

The `guide_generator.py` module provides high-level orchestration and automation for generating, summarizing, and maintaining a **Documentation Guide** for a code repository. It collects individual documentation files (typically auto-generated for source code files), organizes them into a navigable guide, and supports both **full** and **incremental** guide updates in response to source code changes. The guide helps users quickly overview and locate generated documentation for large projects.

## Functionality

The principal logic is encapsulated in the `GuideGenerator` class. Its key responsibilities are:

- **Loading Existing Documentation**: Efficiently retrieves previously generated documentation files and their summaries.
- **Generating Documentation Guide**: Aggregates documentation summaries and metadata into a central guide file.
- **Incremental Updates**: Detects file changes and regenerates only the affected guide entries, avoiding unnecessary work.
- **Saving Guide**: Outputs the compiled documentation guide as a Markdown file.
- **Metadata Extraction and Management**: Reads and updates metadata embedded in documentation files for synchronization.
- **Summarization**: Utilizes a language model (LLM) to generate concise summaries of documentation entries.

The guide generator is designed for workflows using both OpenAI and Anthropic LLMs and operates within a pluggable "pipeline" configuration.

## Key Components

### Main Class: `GuideGenerator`

#### Initialization

```python
def __init__(
    self,
    llm: Union[ChatAnthropic, ChatOpenAI],
    config: PipelineConfig,
    doc_processor: DocumentProcessor,
)
```

- `llm`: Language model instance for summarization.
- `config`: Pipeline configuration options.
- `doc_processor`: For token counting and document context preparation.

#### Core Methods

- **Full Guide Pipeline:**
    - `load_existing_documentation(state)`
        - Loads all previous documentation files and their results from the output path.
    - `load_existing_documentation_results(state)`
        - Loads and parses all `_documentation.md` files, extracting their content and original file paths.
    - `generate_documentation_guide(state)`
        - Produces a full guide from a set of results, including LLM-driven summary generation for each file.
    - `save_documentation_guide(state, guide)`
        - Writes the aggregated guide to `documentation_guide.md` as Markdown.

- **Incremental Guide Pipeline:**
    - `detect_guide_changes(state)`
        - Uses `GuideMetadataManager` to assess what guide entries need to be updated, created, or deleted based on current and previous states.
    - `generate_incremental_guide(state)`
        - Generates only the changed or new parts of the documentation guide, reusing unchanged entries, and updates the guide file.
    - `_generate_guide_entry_for_file(state, relative_path)`
        - Generates a `DocumentationGuideEntry` for any arbitrary source file.

- **Utility/Helpers:**
    - `extract_metadata_from_doc(doc_path)`
        - Extracts YAML or HTML metadata from a documentation file for tracking provenance and state.
    - `_clean_documentation_content(doc_content)`
        - Strips LLM output and generated files of metadata and code to leave only documentation text for summarization.
    - `_generate_doc_summary(doc_content, file_path)`
        - Calls the LLM to generate a concise summary of documentation for a source file.
    - `_get_metadata_manager(output_path)`
        - Instantiates or reuses the associated `GuideMetadataManager` for the output path.

### Data Models (imported from `.models`)
- `DocumentationGuide`
- `DocumentationGuideEntry`
- `PipelineConfig`
- `PipelineState`
- `DocumentationResult`
- `ChangeSet`

### Metadata Manager
- `GuideMetadataManager`
    - Manages persistent metadata for correlating source changes with documentation and guide entries.

### Prompt Templates
- Uses a pre-defined LLM system prompt `GENERATE_DOC_SUMMARY_SYSTEM_MESSAGE` defined in `prompts/generate_doc_summary_system_message.py`.

## Dependencies

**Internal:**
- `.models` – shared dataclasses/objects for documentation and pipeline state.
- `.document_processor.DocumentProcessor` – for doc loading and preprocessing.
- `.guide_metadata_manager.GuideMetadataManager` – for metadata tracking and diffing.

**Third-party:**
- `langgraph`, `langchain_openai`, `langchain_anthropic`, `langchain_core` – for LLM invocation and prompt handling.
- Standard libs: `datetime`, `hashlib`, `logging`, `re`, `typing`, `pathlib`.

**External Inputs:**
- `PipelineState` and its properties
- Files on disk: previously generated documentation, code files, and guide files.
- LLM APIs (OpenAI, Anthropic)

## Usage Examples

### 1. **Generating a Full Documentation Guide**
```python
from guide_generator import GuideGenerator

# Suppose you have set up these objects in your pipeline:
llm = ChatOpenAI()  # or ChatAnthropic()
config = PipelineConfig(...)
doc_processor = DocumentProcessor(...)
generator = GuideGenerator(llm, config, doc_processor)
state = PipelineState(...)  # Filled with documentation results

# Generate (or regenerate) the documentation guide:
guide = generator.generate_documentation_guide(state)
generator.save_documentation_guide(state, guide)
```

### 2. **Incrementally Updating the Guide After Code Changes**
```python
# Detect changes:
changeset = generator.detect_guide_changes(state)

# Incrementally update the guide:
updated_guide = generator.generate_incremental_guide(state)
generator.save_documentation_guide(state, updated_guide)
```

### 3. **Loading Existing Documentation for Further Processing**
```python
existing_docs = generator.load_existing_documentation(state)
# existing_docs['results']: list of `DocumentationResult` objects
```

### 4. **Extracting Metadata from a Documentation File**
```python
metadata = generator.extract_metadata_from_doc(Path("path/to/doc_file_documentation.md"))
```

### 5. **Generating Summaries for Documentation**
```python
summary = generator._generate_doc_summary(doc_content, "path/to/src_file.py")
```

## Notes

- The `GuideGenerator` expects documentation files with a specific naming convention (`*_documentation.md`) and embedded structured metadata.
- Summaries for documentation are generated using an LLM, for which an appropriate system prompt is imported.
- Incremental guide updates rely on robust metadata tracking; full guide regeneration is used as a fallback or when major changes are detected.
- Logging is used extensively for diagnostics.

---

**This module is essential for maintaining an up-to-date, navigable summary and index of generated documentation across evolving codebases, leveraging LLMs for human-friendly guide content.**

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: 2db4b86486144c6c05b0a8482d93b4d70560445941e5ca9ec7aeb850a3148f3a
relative_path: src\guide_generator.py
generation_date: 2025-07-01T22:14:20.052452
```
<!-- END GENERATION METADATA -->
