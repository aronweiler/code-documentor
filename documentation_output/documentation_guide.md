# Documentation Guide

<!-- AUTO-GENERATED DOCUMENTATION GUIDE -->
<!-- This file was automatically generated and should not be manually edited -->

This guide provides an overview of all generated documentation files in this repository.
Use this guide to quickly locate relevant documentation when working on specific features or components.

**Generated on:** 2025-06-10T23:27:16.810044  
**Total documented files:** 19

## Documentation Files

### main.py

**Documentation:** `main_documentation.md`

**Summary:** main.py serves as the command-line entry point for a documentation toolkit, exposing three subcommands—generate (to run the full documentation pipeline), analyze (to inspect repository structure), and validate-config (to verify config and API key setup). It sets up both subcommand and backward-compatible direct argument parsing, then dispatches to the appropriate runner functions (run_documentation_generation, run_repository_analysis, run_config_validation) while handling errors and optional verbose stack traces. Core components include the main() entry point, parser-builder helpers, and integrations with local modules like DocumentationPipeline, ConfigManager, and CodeAnalyzer.

---

### src\code_analyzer.py

**Documentation:** `src\code_analyzer_documentation.md`

**Summary:** The `src/code_analyzer.py` module defines a `CodeAnalyzer` class that scans a code repository using configurable file‐extension and exclusion patterns, reads each qualifying file’s contents (with multi‐encoding fallbacks), and wraps them into `CodeFile` objects. Its key methods—`scan_repository`, `_should_include_file`, and `_read_code_file`—handle file discovery, filtering, and content loading, while `analyze_file_structure` compiles metrics such as total file count, breakdowns by extension and directory, and the largest files by size. This functionality underpins automated extraction and structural analysis of codebases for downstream documentation generation.

---

### src\config.py

**Documentation:** `src\config_documentation.md`

**Summary:** The `ConfigManager` module provides a centralized way to load, cache, and manage application settings from a YAML file (defaulting to `config.yaml`) and environment variables (via a `.env` file), with a focus on API keys and model parameters. Its core class, `ConfigManager`, offers `load_config()` to parse and return a `PipelineConfig` object, `get_api_key(provider)` to fetch provider-specific API keys from the environment, and `get_model_config()` to assemble a complete model configuration (including Azure-specific details). By leveraging `yaml`, `dotenv`, and `os`, it ensures secure, dynamic configuration management for multiple API providers such as OpenAI, Anthropic, and Azure OpenAI.

---

### src\context_manager.py

**Documentation:** `src\context_manager_documentation.md`

**Summary:** The src/context_manager.py module provides a ContextManager class that orchestrates loading an existing documentation guide, summarizing large documentation blobs via chunking and an LLM client (with error fallback), and formatting plus merging newly generated guides into the current documentation context. Its key methods include load_documentation_guide (to read and append on-disk guides), summarize_docs (to chunk and synthesize summaries), format_guide_for_context (to render a DocumentationGuide as markdown), and enhance_context_with_guide (to merge guide content into a DocumentationContext. It relies on a PipelineState carrying request parameters, a doc_processor for token counting/chunking, and an LLM client to produce a unified DocumentationContext for downstream design-doc generation.

---

### src\design_document_generator.py

**Documentation:** `src\design_document_generator_documentation.md`

**Summary:** The `DesignDocumentGenerator` class automates end-to-end creation of software design documents by reading user configuration, iteratively generating each section via an LLM (with retry‐on‐truncation logic), assembling sections into a coherent Markdown file, and saving it with metadata. Key components include pipeline state management (tracking documents, sections, and accumulated context), LangChain‐based prompt construction and file tools for LLM interactions, token‐based truncation detection/continuation, and utilities for assembling and persisting the final documents.

---

### src\document_processor.py

**Documentation:** `src\document_processor_documentation.md`

**Summary:** The `DocumentProcessor` module loads and processes documentation files—reading their content, counting tokens with GPT-4 encoding, checking against configurable summarization thresholds, splitting oversized text into chunks, and assembling a final context string for downstream pipelines. Its main class, `DocumentProcessor` (configured via `PipelineConfig`), provides methods like `load_existing_docs`, `count_tokens`, `needs_summarization`, `create_chunks`, and `prepare_context`, leveraging `tiktoken` and LangChain text-splitting utilities.

---

### src\file_processor.py

**Documentation:** `src\file_processor_documentation.md`

**Summary:** The `FileProcessor` class automates a documentation pipeline by detecting changed source files (via SHA-256 hashing and existing metadata) and generating or skipping documentation accordingly. It also manages output directories and writes LLM-generated Markdown files—complete with auto-generated headers, optional code snippets, and a YAML metadata footer—using its core methods: `should_generate_documentation`, `save_single_result`, `calculate_file_hash`, and `create_output_directory_structure`.

---

### src\guide_generator.py

**Documentation:** `src\guide_generator_documentation.md`

**Summary:** The GuideGenerator class automates the final step of a documentation pipeline by loading existing markdown docs (with embedded metadata), cleaning and parsing their content, invoking an LLM (Anthropic or OpenAI) to produce concise per‐file summaries, and assembling everything into a single navigable “Documentation Guide.” It provides methods to scan an output directory for `*_documentation.md` files, extract and strip metadata and code blocks, call `_generate_doc_summary` via a chat LLM, and wrap results in `DocumentationGuideEntry` objects. Once summaries are generated, `save_documentation_guide` renders a `documentation_guide.md` with overall metadata (generation date, file count) and indexed entries. Key collaborators include `DocumentProcessor` for context handling, LLM interfaces (`ChatAnthropic`/`ChatOpenAI`), and data models like `DocumentationResult`, `DocumentationGuideEntry`, and `DocumentationGuide`.

---

### src\llm_manager.py

**Documentation:** `src\llm_manager_documentation.md`

**Summary:** LLMManager centralizes the setup of OpenAI or Anthropic chat models by selecting the provider, resolving API keys (from a config object or environment variables), and applying common parameters like model name, temperature, and timeout. It exposes a single `initialize_llm()` method that returns a configured `ChatOpenAI` or `ChatAnthropic` instance or raises an error for unsupported providers or missing keys. All settings are driven by an injected `config_manager` supplying a simple model_config dictionary.

---

### src\models.py

**Documentation:** `src\models_documentation.md`

**Summary:** This module defines core Pydantic models for a documentation‐generation pipeline, providing structured validation and serialization for pipeline configuration (PipelineConfig), user requests (DocumentationRequest), source files (CodeFile), existing docs context, and generated outputs. It includes models for file‐level documentation results (DocumentationResult), guide assembly (DocumentationGuide and its entries), design‐document sections and documents (DesignDocumentSection, DesignDocument, DesignDocumentationState), and the overall pipeline state (PipelineState) to track progress, status flags, and aggregated content. Together, these models ensure consistent data handling across code ingestion, documentation generation, guide creation, and design‐doc assembly stages.

---

### src\pipeline.py

**Documentation:** `src\pipeline_documentation.md`

**Summary:** The `DocumentationPipeline` class orchestrates an end-to-end documentation workflow: it scans a code repository, loads or summarizes existing documentation, invokes a large language model to produce per-file markdown and optional high-level design docs or style guides, and persists all outputs with progress reporting. Internally it builds a state-graph of modular steps (load, summarize, scan, generate, assemble, save) whose branching logic is managed by a `StateManager`. Core components include `ConfigManager` for settings, `CodeAnalyzer`, `DocumentProcessor`, `LLMManager`, and dedicated generators for files, design documents, guides, and reports, all wired together and executed via the pipeline’s `run()` method.

---

### src\report_generator.py

**Documentation:** `src\report_generator_documentation.md`

**Summary:** The `ReportGenerator` class centralizes all post-processing and reporting for a documentation-generation pipeline by creating output directories, saving individual file documentation (when incremental saving is off), printing CLI status updates, and producing a human-readable Markdown summary report. Its `save_results` method drives the overall flow—folder setup, optional per-file saves via a provided `file_processor`, summary report generation, and design-doc status output—returning `{"completed": True}` on success. Additional methods like `generate_summary_report` and `generate_design_docs_report_section` build detailed sections of `documentation_report.md`, including counts of processed, skipped, and failed files plus design-doc breakdowns. It operates on a `PipelineState` object (containing request/output paths, results, and optional design or existing docs) and a global `config` dict.

---

### src\state_manager.py

**Documentation:** `src\state_manager_documentation.md`

**Summary:** The `StateManager` class drives a multi‐step documentation generation pipeline by inspecting a shared `PipelineState` and configuration flags, then returning string directives (e.g. "continue", "summarize", "generate", "assemble", "finish") that tell the orchestration engine which action to take next. Its methods cover whether to load or summarize existing docs, generate file‐level or design documents, and loop over files, sections, and documents, updating indices and payloads as needed. Key entry points include `should_summarize`, `should_generate_files`, `should_generate_design_docs`, `has_more_files`, `has_more_sections`, and `has_more_documents`.

---

### src\prompts\continue_truncated_content_system_prompt.py

**Documentation:** `src\prompts\continue_truncated_content_system_prompt_documentation.md`

**Summary:** This file defines a single string constant, CONTINUE_TRUNCATED_CONTENT_SYSTEM_PROMPT, which serves as a parameterized template for generating prompts that guide an AI or automated system to continue incomplete documentation sections. The template includes placeholders for document name, section name, existing context, section instructions, and a continuation prompt to ensure coherence and relevance. It also references repository file-reading utilities (e.g., read_file_content, list_files_in_directory) to pull in additional context as needed.

---

### src\prompts\generate_doc_summary_system_message.py

**Documentation:** `src\prompts\generate_doc_summary_system_message_documentation.md`

**Summary:** This module defines a single constant, GENERATE_DOC_SUMMARY_SYSTEM_MESSAGE, which holds a standardized system‐level prompt guiding an LLM to produce concise 2–4 sentence summaries of code documentation. It centralizes instructions to focus on each piece of code’s primary purpose/function and key components. The constant has no external dependencies and is intended for import by any prompt‐builder or LLM client responsible for documentation summarization.

---

### src\prompts\section_prompt_system_message.py

**Documentation:** `src\prompts\section_prompt_system_message_documentation.md`

**Summary:** This file defines a single multi-line string, SECTION_PROMPT_SYSTEM_MESSAGE, which serves as a system-message template for a documentation generator. It embeds placeholders (e.g., document_name, section_name, context, section_template) and instructs the generator to use file-exploration tools to gather project details. By filling in these placeholders, the generator produces coherent, context-aware sections of a design document.

---

### src\tools\file_tools.py

**Documentation:** `src\tools\file_tools_documentation.md`

**Summary:** The `file_tools.py` module provides four core utilities—read_file_content, list_files_in_directory, find_files_by_pattern, and get_file_info—for safely reading files, listing directory contents (with optional extension filters and recursion), performing glob-style searches, and retrieving file metadata (size, modification time, etc.) within a specified repository. Each function enforces repository-bound checks and handles common errors (e.g., missing files, permission issues). It relies solely on Python’s standard libraries (`pathlib`, `os`) and uses type hints for clear interfaces.

---

### src\utilities\token_manager.py

**Documentation:** `src\utilities\token_manager_documentation.md`

**Summary:** The `token_manager.py` module supplies a `TokenCounter` class that loads and caches model‐specific `tiktoken` encoders, normalizes arbitrary model names, counts exact or fallback (word-based) tokens in free-form text, and estimates token usage for structured chat messages by adding fixed per-message and conversation overhead. This abstraction streamlines token‐usage tracking and budget enforcement when calling OpenAI LLM APIs, ensuring requests stay within model limits. It also logs warnings whenever encoder loading or tokenization fails.

---

### src\tools\lc_tools\lc_file_tools.py

**Documentation:** `src\tools\lc_tools\lc_file_tools_documentation.md`

**Summary:** The `lc_file_tools.py` module provides a `create_file_tools(repo_path: Path)` function that generates a suite of LangChain `Tool` objects for common file operations—reading file contents, listing directory contents (with optional extension filtering and recursion), finding files by glob pattern, and retrieving metadata like size and modification time. Each tool wraps a corresponding core file operation (e.g. `read_file_content`, `list_files_in_directory`, etc.) with error handling and a standardized interface, enabling easy integration of repository file management tasks into LangChain workflows.

---

