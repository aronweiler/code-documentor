<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for src\context_manager.py

# src/context_manager.py

## Purpose
`ContextManager` centralizes the logic for assembling, summarizing, and enhancing documentation context within a pipeline. It enables:
- Loading an existing documentation guide (if any) into the current documentation context.
- Summarizing large documentation blobs via an LLM, with chunking and error-fallback.
- Formatting and merging a generated documentation guide (`DocumentationGuide`) into existing docs.
- Providing a unified interface for downstream steps that generate design documents or further process docs.

---

## Functionality

### `__init__(self, config, doc_processor, llm)`
Constructor.  
- **config**: global or pipeline-level settings.  
- **doc_processor**: component with methods  
  - `create_chunks(text: str) -> List[str]`  
  - `count_tokens(text: str) -> int`  
- **llm**: language-model client exposing an `invoke(messages)` method.  
- **logger**: module-level logger for info/debug/error messages.

### `load_documentation_guide(self, state: PipelineState) -> Dict[str, Any]`
Checks whether a documentation guide exists on disk and, if found, reads it and appends it to the `state.existing_docs` context.  
- If `state.request.guide` is `False` but `design_docs` are requested, it still attempts to load a guide from `output_path/documentation_guide.md`.  
- On success, returns `{"existing_docs": DocumentationContext(...)}` with updated content, token count, and original docs list.  
- On failure or absence, returns an empty dict.

### `summarize_docs(self, state: PipelineState) -> Dict[str, Any]`
Breaks `state.existing_docs.content` into chunks, submits each chunk to the LLM for summarization using a predefined `ChatPromptTemplate`, and stitches the chunk‐summaries back together.  
- Preserves terminology, architecture decisions, implementation details, and dependencies.  
- Implements per-chunk error handling: on exception, logs the error, falls back to truncated chunk text, and counts failures.  
- Returns `{"existing_docs": DocumentationContext(...)}` with `summarized=True` and updated token counts.

### `format_guide_for_context(self, guide: DocumentationGuide) -> str`
Transforms a populated `DocumentationGuide` object into a markdown string block suitable for appending to existing contexts.  
- Includes metadata (`generation_date`, `total_files`) and iterates each `guide.entries` to list file paths and their summaries.

### `enhance_context_with_guide(self, state: PipelineState, guide: DocumentationGuide) -> DocumentationContext`
If the provided `guide` has entries, merges the formatted guide content into `state.existing_docs.content` and returns a new `DocumentationContext`. Otherwise, returns the unmodified `state.existing_docs`.

### `load_existing_guide_from_file(self, state: PipelineState) -> str`
Reads the file `output_path/documentation_guide.md` (if it exists) and returns its content as a string. On error or absence, returns an empty string.

---

## Key Components

- **ContextManager**  
  Orchestrates reading, summarizing, and enriching documentation contexts.
- **PipelineState** (`.models`)  
  Carries request parameters, existing docs, and other pipeline metadata.
- **DocumentationContext** (`.models`)  
  Data class encapsulating:
  - `content: str`  
  - `token_count: int`  
  - `summarized: bool`  
  - `original_docs: List[str]`
- **DocumentationGuide** (`.models`)  
  Represents a generated guide, with fields:
  - `generation_date: str`  
  - `total_files: int`  
  - `entries: List[Entry]` (each with `original_file_path`, `doc_file_path`, `summary`)
- **doc_processor**  
  - `count_tokens(text: str) -> int`  
  - `create_chunks(text: str) -> List[str]`
- **llm**  
  Language-model client with `invoke(messages: List[Message]) -> Response`.

---

## Dependencies

External:
- `logging` (std lib)
- `typing`: `Dict`, `Any`, `List`
- `langchain_core.messages`: `HumanMessage`, `SystemMessage`
- `langchain_core.prompts`: `ChatPromptTemplate`

Internal:
- `.models`: `PipelineState`, `DocumentationContext`, `DocumentationGuide`

Downstream:
- Pipeline orchestrators that generate design docs or final outputs rely on `ContextManager` to prepare `existing_docs` for next steps.

---

## Usage Examples

```python
from pathlib import Path
import logging

from src.context_manager import ContextManager
from src.models import PipelineState, DocumentationContext, DocumentationGuide
from my_project.doc_processor import DocProcessor
from my_project.llm_client import LLMClient

# 1. Initialize components
config = {"max_tokens": 2000}
doc_processor = DocProcessor()
llm = LLMClient(model="gpt-4")
ctx_manager = ContextManager(config, doc_processor, llm)

# 2. Prepare pipeline state
state = PipelineState(
    request=SomeRequest(
        output_path=Path("./output"),
        guide=False,
        design_docs=True
    ),
    existing_docs=DocumentationContext(
        content="Long existing documentation...",
        token_count=15000,
        summarized=False,
        original_docs=["initial docs..."]
    )
)

# 3. Load an existing guide if present
result = ctx_manager.load_documentation_guide(state)
if "existing_docs" in result:
    state.existing_docs = result["existing_docs"]

# 4. Summarize if too large
if state.existing_docs.token_count > config["max_tokens"]:
    result = ctx_manager.summarize_docs(state)
    state.existing_docs = result["existing_docs"]

# 5. At design-doc generation time, merge a freshly generated guide
generated_guide = DocumentationGuide(
    generation_date="2024-07-01",
    total_files=5,
    entries=[
        Entry("/src/a.py", "/docs/a.md", "Summary of a.py"),
        # ...
    ]
)
state.existing_docs = ctx_manager.enhance_context_with_guide(
    state, generated_guide
)

# 6. Now pass state.existing_docs.content to your design doc generator
print("Final context:", state.existing_docs.content)
```

This workflow ensures that your documentation pipeline can incrementally load, summarize, and enrich context for downstream processing without manual file I/O.

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: db8eada057d6b2cab8857bad6b8b10b4ca7f7d6403bb3983e178a4f9f6b263eb
relative_path: src\context_manager.py
generation_date: 2025-06-10T22:37:46.905782
```
<!-- END GENERATION METADATA -->
