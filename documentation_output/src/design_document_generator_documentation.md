<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for src/design_document_generator.py

# design_document_generator.py

## Purpose

`design_document_generator.py` provides the core logic for automating the generation of structured, comprehensive design documents using an LLM (Large Language Model). It manages the multi-step workflow of initializing documentation, generating section-by-section content, handling content truncation, assembling final documents, and writing the output to disk, typically as Markdown files.

This component exists to support complex documentation pipelines, ensuring design documentation can be created or updated iteratively with context from existing documents, requirements, and prior outputs.

---

## Functionality

The primary functionality is implemented in the `DesignDocumentGenerator` class, which orchestrates the flow:

- **Initialization**: Sets up a plan of which documents and sections (from configuration) need to be generated.
- **Section Generation**: For each section, prepares context, generates content via the LLM, and handles retries or continuations in case of output truncation.
- **Assembly**: After all sections are generated, uses the LLM to combine them coherently or falls back to simple concatenation.
- **Persistence**: Saves the final design document to a designated path on disk in Markdown format.

---

## Key Components

### `DesignDocumentGenerator` Class

#### Constructor and Main Instance Attributes

- **`__init__(self, llm, config, doc_processor)`**
  - `llm`: The language model interface (supports tools + invocation)
  - `config`: Configuration dict/object detailing which docs/sections to generate, token limits, retry options, etc.
  - `doc_processor`: Object/utility for document processing (not directly used in this file)
  - Instantiates a `TokenCounter` for token heuristics.

#### High-Level Methods

- **`initialize_design_documents(state)`**  
  Reads the configuration and sets up the initial state for document/section planning, skipping disabled docs/sections.

- **`generate_design_section(state)`**  
  Generates a single section's content, handles context preparation, output validation, and token truncation/continuation logic. Updates state accordingly.

- **`assemble_design_document(state)`**  
  Collects all sections, invokes the LLM for a final assembly prompt, saves the result, and updates state for the next document.

#### Internal/Helper Methods

- **`_prepare_section_context(...)`**  
  Builds context string for a section using prior documentation, previous documents, and current/previous sections.

- **`_generate_section_content(...)`**  
  The LLM-invoking logic for section generation, with built-in retry and truncation detection.

- **`_create_langchain_tools(repo_path)`**  
  Sets up LangChain-based file access tools for the LLM, scoped to the repository path.

- **`_create_section_prompt(document, section, context)`**  
  Prepares a system+human message prompt for section generation.

- **`_is_content_truncated(content, max_tokens)`**  
  Heuristically determines if a generated output is truncated (by punctuation and token count).

- **`_continue_truncated_content(...)`**  
  Handles LLM prompt design for continuing a previously-truncated section.

- **`_ai_assemble_document(document, sections_content)`**  
  Invokes the LLM to combine all section texts into a single document; falls back to concatenation if the LLM fails.

- **`_save_design_document(state, document, content)`**  
  Persists the assembled document to the `design_documentation` folder in the output path, with a metadata header.

---

### Data Model Dependencies

Imports and operates on the following data classes (from `.models`):

- `PipelineState`
- `DesignDocument`
- `DesignDocumentSection`
- `DesignDocumentationState`
- `DocumentationContext`

These represent the evolving state of the documentation process and structure of documents/sections.

---

### Prompt and Tool Dependencies

- `SECTION_PROMPT_SYSTEM_MESSAGE`, `AI_ASSEMBLY_SYSTEM_MESSAGE`, `CONTINUE_TRUNCATED_CONTENT_SYSTEM_PROMPT`  
  System prompt strings/templates for use when interacting with the LLM.

- `create_file_tools`  
  Function to produce repository-scoped LangChain tool objects.

- `TokenCounter`  
  Utility for token length heuristics (used to detect truncation).

---

## Dependencies

**Direct Python Imports:**
- `datetime`, `pathlib.Path`, `typing` (Dict, Any, etc.)

**LangChain/Core AI Imports:**
- `langchain_core.messages.HumanMessage`, `SystemMessage`
- `langchain_core.prompts.ChatPromptTemplate`

**Internal (project-level) Imports:**
- Prompts from `.prompts` submodules
- Models from `.models`
- Token management from `.utilities.token_manager`
- Repository tooling from `.tools.lc_tools.lc_file_tools`

**What Depends on This:**  
This generator is intended to be invoked as part of a larger documentation or code analysis pipeline, possibly triggered by a CLI tool, web app, or batch script managing a project documentation process.

---

## Usage Examples

### Example: Minimal End-to-End Usage in a Pipeline

```python
from src.design_document_generator import DesignDocumentGenerator
from src.models import PipelineState

# Assume you have LLM, config, doc_processor, and an initialized PipelineState
generator = DesignDocumentGenerator(llm, config, doc_processor)

# Step 1: Initialize documentation plan
pipeline_state = PipelineState(...)  # needs to be populated as per project
init_result = generator.initialize_design_documents(pipeline_state)

# Step 2: Generate all sections for a document
while not all_documents_complete(init_result["design_documentation_state"]):
    section_result = generator.generate_design_section(init_result["design_documentation_state"])
    # Optionally, can check for errors or review intermediate outputs

# Step 3: Assemble final document after its sections are all generated
assembly_result = generator.assemble_design_document(section_result["design_documentation_state"])

# Generated documents are saved to disk at this point.
```

*See `PipelineState`, `DesignDocument`, etc., for details on what the `state` objects should contain/cohere to.*

---

## Notes

- Logging is done via `print()` statements; in production this may be swapped for a proper logger.
- The class assumes `llm` can be bound with tools and accepts chain-of-prompts; adjust for your LLM integration as required.
- Fails gracefully, marking sections/documents as unsuccessful when errors occur.
- Heuristics for truncation are adjustable/replaceable as needed.
- Final Markdown files include auto-generated headers with metadata.

---

**This file is the central AI-driven orchestration layer for design documentation workflows.**

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: 770baf328becc167321fc77192e8efca3739f8850b82fbd1da226ce31976dec5
relative_path: src/design_document_generator.py
generation_date: 2025-06-30T00:05:51.503897
```
<!-- END GENERATION METADATA -->
