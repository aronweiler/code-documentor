<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for config.yaml

# config.yaml

## Purpose

`config.yaml` serves as the **central configuration file** for a documentation pipeline that uses AI models to generate, process, and manage documentation for a software project. It defines operational parameters, model settings, file processing rules, output formats, template structures for various document types, and retry policies. The goal is to provide a single source of truth for all aspects of automated documentation generation, ensuring consistency, scalability, and clear customization.

---

## Functionality

This configuration file governs how the documentation pipeline operates:

- **AI Model Settings**: Specifies which AI provider/model to use, as well as generation parameters like temperature, token limits, and recursion boundaries.
- **Token Management**: Controls how much context the model receives, when summarizations occur, and chunk sizes for large documents.
- **File Processing**: Sets limits and filter rules for files to include or exclude, based on name patterns and file extensions.
- **Output Formatting**: Describes how generated documentation is formatted (e.g., Markdown), and whether code should be included or shown alongside documentation.
- **Documentation Templates**: Supplies rich, structured templates for various document types, including architecture guides, design docs, user/dev guides, and more.
- **Retry Policy**: Outlines how to handle failed or truncated output from the AI, providing continuity and automating error handling.

---

## Key Components

### 1. Model Configuration (`model`)
- **provider**: Selects the AI backend (e.g., `openai`, `anthropic`, `azure_openai`).
- **name**: Chooses the AI model (e.g., `gpt-4.1`).
- **temperature**: Controls creativity/variance of model output.
- **max_tokens**: Maximum output size.
- **recursion_limit**: Limits recursion for graph-based workflows (e.g., LangGraph).

### 2. Token Limits (`token_limits`)
- **max_context_tokens**: Maximum tokens in the context window.
- **summarization_threshold**: When to trigger a context summarization.
- **chunk_size**: Document splitting size for large files.

### 3. Processing (`processing`)
- **max_files**: Maximum files to process in a run (0 or null = unlimited).
- **save_incrementally**: Whether to autosave documentation after each file.

### 4. File Processing (`file_processing`)
- **supported_extensions**: File types that are processed for documentation.
- **exclude_patterns**: Directory and file patterns to ignore during processing.

### 5. Output (`output`)
- **format**: Output document format (e.g., `markdown`).
- **include_code**: Option to include source code in output.
- **side_by_side**: Whether to generate code and docs side-by-side.

### 6. Documentation Templates (`templates`)
- **file_documentation**: Template for generated per-file docs.
- **documents**: Definitions and templates for higher-level docs; supports:
    - `project_overview`
    - `architecture`
    - `design`
    - `user_guide`
    - `developer_guide`
    - *(API, module, testing, and deployment documentation can be enabled as needed)*

Each section can be individually enabled/disabled, uses token limits, and supports custom instructions.

### 7. Retry Configuration (`retry_config`)
- **max_retries**: How many times to retry a failed or truncated generation.
- **retry_on_truncation**: Whether to retry if output is cut off.
- **continuation_prompt**: Prompt text to continue drafting from truncated content.

---

## Dependencies

**Internal dependencies:**
- This file is referenced by the documentation pipeline application (code not shown).
- Controls the behavior of document generators, file processors, and output renderers within the pipeline.

**External dependencies:**
- Depends on access to AI model APIs (e.g., OpenAI, Anthropic).
- Excludes/filters file system content according to patterns/rules specified herein.

**Reverse dependencies:**
- Documentation scripts, CLI utilities, or CI jobs responsible for generating or updating documentation rely on this config.

---

## Usage Examples

### 1. Initializing the Documentation Pipeline

When running your documentation pipeline, simply reference this file:

```sh
docgen --config config.yaml
```

Most pipelines will read this config automatically if it resides in the project root.

### 2. Customizing Documentation Output

- **To add your own docs section (e.g., 'FAQ')**: Add a new section under `templates.documents` and provide a template.
- **To enable API docs**: Set `api_documentation.enabled: true` and fill out section templates.
- **To process additional file types (e.g., `.md` files)**: Add `.md` under `supported_extensions`.

### 3. Controlling File Processing

To only run documentation on a subset of files:
```yaml
processing:
  max_files: 100
file_processing:
  exclude_patterns:
    - "legacy"
    - "tests"
```

### 4. Using Side-by-side Output

If your documentation viewer supports it, set:
```yaml
output:
  side_by_side: true
```
This visually pairs documentation with code for each file.

### 5. Handling Model Truncations

When the model gets cut off mid-generation, the pipeline will prompt the AI to **continue from where it left off** using the built-in `continuation_prompt`.

---

## Summary

`config.yaml` is a robust, modular configuration file at the core of your AI-powered documentation workflow. By editing this file, you control the documentation coverage, level of detail, output style, documentation templates, and operational resilience of the documentation pipeline. This makes auto-generating and maintaining high-quality developer, user, design, and architectural documentation streamlined and customizable.

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: 1d26d0b52f77306489f02c6d9be267bf34e1ea48463126b63b5a8e98677e309f
relative_path: config.yaml
generation_date: 2025-06-30T00:02:37.030795
```
<!-- END GENERATION METADATA -->
