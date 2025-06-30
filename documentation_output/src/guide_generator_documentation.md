<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for src\guide_generator.py

# guide_generator.py

## Purpose

The `guide_generator.py` file is responsible for creating, updating, and managing a comprehensive documentation guide for a codebase. It automates the aggregation of documentation files into a single navigable guide, facilitates incremental guide regeneration when code changes occur, and ensures that up-to-date summaries and references to detailed documentation files are available. This is primarily intended to assist developers in easily discovering relevant documentation throughout a repository.

---

## Functionality

The main class in this file is `GuideGenerator`, which offers methods to:

- **Load existing documentation files**
- **Generate documentation summaries using LLMs (Large Language Models)**
- **Create a top-level documentation guide** (mapping code files to their documentation and a summary)
- **Detect file/documentation changes for incremental guide updates**
- **Save and load guides and associated metadata**

The generator ensures both full-guide regeneration and efficient, incremental updates when only a subset of files or documentation requires modification.

---

## Key Components

### Main Class: `GuideGenerator`

#### Initialization

```python
GuideGenerator(
    llm: Union[ChatAnthropic, ChatOpenAI],
    config: PipelineConfig,
    doc_processor: DocumentProcessor,
)
```
- **llm:** An instantiated ChatOpenAI or ChatAnthropic LLM for summarization
- **config:** Pipeline configuration with runtime settings
- **doc_processor:** Tool for loading and contextualizing documentation/code

#### Principal Methods

- **load_existing_documentation(state)**
  - Loads already-generated documentation files for a project.
  - Returns a structured result containing loaded docs and their metadata.

- **load_existing_documentation_results(state)**
  - Scans for existing generated documentation markdown files, parsing their metadata and content into `DocumentationResult` objects.

- **generate_documentation_guide(state)**
  - Processes all documentation results to create `DocumentationGuideEntry` objects.
  - Uses the LLM to generate concise summaries for each file's doc.
  - Returns a `DocumentationGuide` aggregating all entries and metadata.

- **_generate_doc_summary(doc_content, file_path)**
  - Uses the LLM to produce a concise summary based on generated documentation content.

- **save_documentation_guide(state, guide)**
  - Writes the `DocumentationGuide` (as Markdown) to disk in the documentation output directory.

- **extract_metadata_from_doc(doc_path)**
  - Extracts metadata (YAML or HTML-style) from a documentation file for traceability and mapping.

##### Incremental Guide Support

- **detect_guide_changes(state)**
  - Detects which documentation files have changed or need guide updates using `GuideMetadataManager`.
  - Stores a `ChangeSet` in state for later incremental guide regeneration.

- **generate_incremental_guide(state)**
  - Uses a `ChangeSet` to only update the parts of the guide corresponding to modified/new/deleted files.
  - Merges updates into the existing guide.
  - Backs off to a full regeneration if major structure changes are detected.

- **_load_existing_guide(state)**
  - Attempts to load and parse an existing guide from disk.

- **_parse_guide_entries(guide_content)**
  - Parses previously generated entries from the Markdown guide.

- **_generate_single_guide_entry(state, result)**
  - Generates a guide entry for a single result (including reprocessing summary via LLM).

- **_clean_documentation_content(doc_content)**
  - Utility to remove code blocks and metadata from documentation for better summarization.

- **_generate_guide_entry_for_file(state, relative_path)**
  - Generates a guide entry given a file path (for cases not tracked by results).

---

## Key Dependencies

- **langchain_openai, langchain_anthropic:** For invoking LLMs to summarize documentation
- **langgraph.graph:** For orchestration (imported but not directly used in this file)
- **DocumentProcessor, GuideMetadataManager:** Utility classes/modules internal to the project
- **models.py:** Provides classes such as `DocumentationGuide`, `DocumentationGuideEntry`, `PipelineState`, `DocumentationResult`, `ChangeSet`
- **prompts.generate_doc_summary_system_message:** Provides the prompt system message for summaries

**Standard library:** Uses typical modules for I/O, path management, logging, datetime, regex, and typing.

**This file is depended upon by:** Other modules in the project that orchestrate pipeline execution, documentation aggregation routines, and developer-facing reporting tools.

---

## Usage Examples

### Full Documentation Guide Generation

```python
# Assume 'llm', 'config', and 'doc_processor' are properly instantiated.
generator = GuideGenerator(llm, config, doc_processor)
pipeline_state = ...  # Prepared PipelineState, including output and repo paths

# Generate a guide from all documentation results
guide = generator.generate_documentation_guide(pipeline_state)

# Save it for team consumption
generator.save_documentation_guide(pipeline_state, guide)
```

### Incremental Guide Updates After Code Change

```python
# Detect which files have changed or need guide updates
changeset = generator.detect_guide_changes(pipeline_state)

# Generate only the updated guide entries
incremental_guide = generator.generate_incremental_guide(pipeline_state)

# Save the updated guide
generator.save_documentation_guide(pipeline_state, incremental_guide)
```

### Loading Existing Documentation and Guides

```python
existing_docs_info = generator.load_existing_documentation(pipeline_state)
existing_guide = generator._load_existing_guide(pipeline_state)
```

### Extracting Metadata from a Documentation File

```python
meta = generator.extract_metadata_from_doc(Path("docs/my_code_documentation.md"))
```

---

## Additional Notes

- The class assumes markdown-based documentation files generated for individual code files, each containing a machine-readable metadata block.
- Summaries for the guide are generated via LLM invocation for consistency and accuracy.
- Incremental guide functions optimize regeneration, avoiding expensive recomputation when code/docs churn is localized.
- Errors and warnings are robustly logged.
- The design is modular and extensible, supporting different LLM backends for summary generation.

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: ec5dfa87f9aa4c4ff3249b5f513731f813db8e794537d1ae40be596f34ba2baf
relative_path: src\guide_generator.py
generation_date: 2025-06-29T16:52:05.643507
```
<!-- END GENERATION METADATA -->
