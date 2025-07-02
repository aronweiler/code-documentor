<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for src\context_manager.py

# context_manager.py

## Purpose

This file defines the `ContextManager` class, which is responsible for handling and managing the documentation context within a documentation generation pipeline. Its responsibilities include loading existing documentation guides, summarizing large documentation sources for efficient context usage, and enhancing documentation context with summarization and guide data. It acts as a critical layer facilitating the interaction between previously generated documentation, the summarization language model, and new artifact creation (such as design documents).

---

## Functionality

The main framework provided is the `ContextManager` class, which includes the following key functionalities:

- **Loading Documentation Guides:** Loads an existing documentation guide if available, and integrates its contents into the current documentation context.
- **Summarization:** Summarizes the existing documentation using a language model if content size is too large for downstream processing, chunking large content as needed, with robust error handling and fallback strategies.
- **Guides Formatting:** Formats detailed guides about the documentation so that they can be injected into other contexts (e.g., for generating design documents).
- **Context Enhancement:** Combines the current documentation with structured guides, managing token counts and original document tracking.
- **Utility Guide Loader:** Loads documentation guides from well-known filesystem locations for easy integration.

---

## Key Components

### 1. `ContextManager` Class

#### Initialization

```python
def __init__(self, config, doc_processor, llm)
```
- `config`: Configuration object with model and pipeline settings.
- `doc_processor`: Utility class for processing documents—chunking and token calculation.
- `llm`: Language model instance that provides summarization or other completions.
- Internal logger for status and diagnostics.

#### Methods

- **load_documentation_guide(state: PipelineState) -> Dict[str, Any]**

    Loads an existing documentation guide from a known location (`documentation_guide.md`) if requested or appropriate, and enhances the context with its content. Handles error and fallback situations.

- **summarize_docs(state: PipelineState) -> Dict[str, Any]**

    Chunks the current documentation using `doc_processor`, iteratively summarizes each chunk with the LLM, and collects the results into a single summarized context. Falls back to truncating text for chunks that fail summarization.

- **format_guide_for_context(guide: DocumentationGuide) -> str**

    Serializes a `DocumentationGuide` into a string (Markdown-friendly), including summary statistics and per-file details.

- **enhance_context_with_guide(state: PipelineState, guide: DocumentationGuide) -> DocumentationContext**

    Concatenates currently loaded documentation with a formatted documentation guide, updating token counts and provenance.

- **load_existing_guide_from_file(state: PipelineState) -> str**

    Loads the documentation guide from the filesystem if it exists and returns its string content.

### 2. Supporting Types (from `.models`)

- **PipelineConfig, PipelineState, DocumentationContext, DocumentationGuide**  
  Data structures for capturing configuration, current state, documentation context, and guide details.

### 3. External/Internal Dependencies

- **Logging**: Uses the standard `logging` library for diagnostics.
- **Language Model & Prompts:**  
  - `langchain_core.messages.{HumanMessage, SystemMessage}`
  - `langchain_core.prompts.ChatPromptTemplate`
  - System message content from `.prompts.summarize_docs_system_message.SUMMARIZE_DOCS_SYSTEM_MESSAGE`.

---

## Dependencies

### Direct Imports

- **langchain_core:** For chat-style prompting and LLM interaction.
- **.prompts.summarize_docs_system_message:** For system prompt template used during summarization.
- **.models:** Provides data types used throughout the pipeline (`PipelineConfig`, `PipelineState`, `DocumentationContext`, `DocumentationGuide`).

### Indirect (Expectation)

- Expects `doc_processor` with `count_tokens()` and `create_chunks()` methods.
- Expects `llm` providing an `.invoke()` method compatible with LangChain chat message format.

### Consumed By

- Dependent upon by pipeline orchestrators responsible for documentation generation, summarization, and context preparation.
- Used for injecting context into downstream language model calls (e.g., design doc synthesis).

---

## Usage Examples

### Instantiate `ContextManager`

```python
config = PipelineConfig(...)  # Your configuration object
doc_processor = ...           # Your document processor instance
llm = ...                     # Your LLM interface

ctx_manager = ContextManager(config, doc_processor, llm)
```

### Summarize Documentation If Too Large

```python
updated_state = ctx_manager.summarize_docs(pipeline_state)
# Now, updated_state["existing_docs"] contains the summarized docs
```

### Load and Inject Existing Documentation Guide

```python
guide_update = ctx_manager.load_documentation_guide(pipeline_state)
if "existing_docs" in guide_update:
    # Use the enhanced docs in subsequent processing
    pipeline_state.existing_docs = guide_update["existing_docs"]
```

### Enhance Context with Explicit Guide

```python
guide_str = ctx_manager.load_existing_guide_from_file(pipeline_state)
print(guide_str)  # Prints the config/guide if present
```

---

## Summary

**`context_manager.py`** provides centralized, robust functionality for managing, summarizing, and enriching the documentation context in an LLM-driven documentation pipeline. By consolidating summarization, context guide integration, and file-system-based guide management, it enables downstream tasks to leverage up-to-date, right-sized, and contextually rich documentation input.

---

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: 4c19721cb3c8d42684c1eaf60adb67b60b8a1394be95b2fa5f58d6f2fecd8baa
relative_path: src\context_manager.py
generation_date: 2025-07-01T22:13:19.342235
```
<!-- END GENERATION METADATA -->
