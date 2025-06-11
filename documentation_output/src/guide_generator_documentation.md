<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for src\guide_generator.py

# GuideGenerator (src/guide_generator.py) Documentation

## Purpose

The `GuideGenerator` class automates the creation of a high‐level documentation guide for a codebase’s generated documentation files. It can:

- Load existing documentation results (markdown files) with metadata.
- Clean and parse the LLM‐generated content.
- Summarize each documentation file via a language model (Anthropic or OpenAI).
- Assemble and save a single “Documentation Guide” that indexes and summarizes all docs.

This file exists to streamline the final step of a documentation pipeline: producing a human‐friendly guide that points developers to the right markdown file for each source code component.

---

## Functionality

1. **Initialization**
   - `__init__(llm, config, doc_processor)`: Store references to:
     - `llm`: A chat LLM instance (either `ChatAnthropic` or `ChatOpenAI`).
     - `config`: Pipeline configuration (`PipelineConfig`).
     - `doc_processor`: Utility for token counting & context prep (`DocumentProcessor`).
   - Sets up a module‐level logger.

2. **Loading Existing Documentation**
   - `load_existing_documentation(state) → Dict[str,Any]`  
     Entry point for re‐using already‐generated docs.  
     - Calls `load_existing_documentation_results` to gather `DocumentationResult` objects.
     - Reads raw markdown files (via `doc_processor.load_existing_docs`) for context if needed.
     - Returns a dict with keys:  
       - `existing_docs`: raw docs content  
       - `results`: list of `DocumentationResult`  
       - `code_files`: empty list (since not processing source)  
       - `current_file_index`: index offset  
       - `completed`: flag

   - `load_existing_documentation_results(state) → List[DocumentationResult]`  
     Scans `state.request.output_path` for `*_documentation.md` files and for each:
     - Extracts YAML or HTML metadata (`extract_metadata_from_doc`).
     - Reads and “cleans” the markdown by stripping original code blocks and metadata.
     - Wraps content into `DocumentationResult(file_path, documentation, success, error_message)`.
     - Logs successes and failures.

3. **Generating the Documentation Guide**
   - `generate_documentation_guide(state) → DocumentationGuide`  
     - Filters successful docs from `state.results`.
     - For each doc:
       - Locates the corresponding markdown file under `output_path`.
       - Reads & cleans it (removing headers, code blocks, metadata).
       - Calls `_generate_doc_summary(clean_content, relative_source_path)` to produce a concise summary.
       - Constructs a `DocumentationGuideEntry(doc_file_path, summary, original_file_path)`.
     - Aggregates entries into a `DocumentationGuide(entries, total_files, generation_date)`.

4. **LLM‐Powered Document Summarization**
   - `_generate_doc_summary(doc_content, file_path) → str`  
     - Builds a chat prompt using a system message (`GENERATE_DOC_SUMMARY_SYSTEM_MESSAGE`) and the cleaned doc content.
     - Invokes the LLM via `llm.invoke(messages)`.
     - Parses the response to extract `summary`; falls back to a generic message on failure.

5. **Saving the Guide to Disk**
   - `save_documentation_guide(state, guide) → None`  
     - Renders a `documentation_guide.md` file under `state.request.output_path`.
     - Includes metadata (generation date, total files) and per‐entry summaries.
     - Overwrites or creates the guide file automatically.

6. **Metadata Extraction**
   - `extract_metadata_from_doc(doc_path) → Optional[Dict[str,str]]`  
     - Reads a markdown file and uses regex to find either:
       - A YAML block inside HTML comments:  
         ```yaml
         <!-- GENERATION METADATA -->
         ```yaml
         key: value
         ```
         <!-- END GENERATION METADATA -->
         ```
       - A simpler HTML comment block:  
         ```html
         <!-- GENERATION_METADATA
         key: value
         -->
         ```
     - Returns a dict of metadata fields (e.g., `relative_path`).

---

## Key Components

- **Classes & Data Models**
  - `GuideGenerator`  
  - **Models Imported**  
    - `DocumentationGuide` (holds guide entries, total count, timestamp)  
    - `DocumentationGuideEntry` (per‐file summary + paths)  
    - `DocumentationResult` (raw load results + success flag)  
    - `PipelineConfig`, `PipelineState` (pipeline orchestration)

- **External Utilities**
  - `DocumentProcessor` (pre‐existing class for token counting & context loading)
  - `ChatAnthropic` / `ChatOpenAI` (LLM interfaces)
  - `ChatPromptTemplate`, `SystemMessage`, `HumanMessage` (prompt construction)
  - `GENERATE_DOC_SUMMARY_SYSTEM_MESSAGE` (system prompt text for summary LLM calls)

- **Logging & Error Handling**
  - Uses Python’s `logging` module
  - Prints warnings & errors to console and logger

---

## Dependencies

- Standard Library: `datetime`, `hashlib` (unused), `logging`, `re`, `pathlib.Path`, `typing`
- Third‐Party:
  - `langgraph.graph` (imports `StateGraph`, `END` but not used directly here)
  - `langchain_openai.ChatOpenAI`
  - `langchain_anthropic.ChatAnthropic`
  - `langchain_core.messages.{HumanMessage,SystemMessage}`
  - `langchain_core.prompts.ChatPromptTemplate`
- Local Modules:
  - `./prompts/generate_doc_summary_system_message.GENERATE_DOC_SUMMARY_SYSTEM_MESSAGE`
  - `./models` (pipeline & documentation data models)
  - `./document_processor.DocumentProcessor`

**Downstream Dependents**:  
This class is intended to be invoked by a higher‐level pipeline orchestrator (not shown) that manages `PipelineState` transitions.

---

## Usage Examples

```python
from pathlib import Path
from langchain_openai import ChatOpenAI
from myproject.document_processor import DocumentProcessor
from myproject.models import PipelineConfig, PipelineState

# 1. Initialize dependencies
llm = ChatOpenAI(model_name="gpt-4", temperature=0.2)
config = PipelineConfig(...)        # your pipeline settings
doc_processor = DocumentProcessor(config)

# 2. Build pipeline state (e.g., after individual docs generation)
state = PipelineState(
    request=PipelineRequest(
        repo_path=Path("/path/to/repo"),
        output_path=Path("/path/to/repo/docs"),
        docs_path=Path("/path/to/repo/old_docs"),
        ...
    ),
    results=[ ... ],  # list of DocumentationResult from prior step
)

# 3. Create GuideGenerator
guide_gen = GuideGenerator(llm, config, doc_processor)

# 4a. Optionally re-load existing docs
load_context = guide_gen.load_existing_documentation(state)

# 4b. Generate fresh documentation guide
docs_guide = guide_gen.generate_documentation_guide(state)

# 5. Persist to disk
guide_gen.save_documentation_guide(state, docs_guide)
```

---

By leveraging `GuideGenerator`, teams can automate the final assembly of their auto‐generated documentation, ensuring every component has an indexed summary in a single, navigable markdown guide.

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: 51db568e62bf13cd69f9b5f356f3d27fee0ba6b155752894b3f1504ab87b9fe6
relative_path: src\guide_generator.py
generation_date: 2025-06-10T22:38:23.633587
```
<!-- END GENERATION METADATA -->
