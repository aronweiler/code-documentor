<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for config.yaml

# Documentation: `config.yaml`

## Purpose

This file defines the **central configuration** for the documentation generation pipeline. It specifies all operational parameters for AI model invocation, file selection and processing, documentation output formatting, documentation template management, and advanced features such as retry logic. It exists to allow maintainers and operators to easily customize, tune, and extend the documentation workflow without changing code.

---

## Functionality

`config.yaml` provides structured settings consumed by the documentation generator and server components (including AI-powered processing via code-documentor, MCP server, and related scripts). Its main functions are:

- **Model Selection and Tuning:** Configures the LLM provider (OpenAI, Anthropic, Azure), model name, temperature, token limits, and recursion settings for all AI operations.
- **Token and Context Management:** Sets global and context-specific token budgets to support long-document summarization, chunking, and context handling.
- **File Selection and Processing:** Defines which file types are included/excluded, how files are processed (incremental saving, max files), and custom glob patterns for project-specific needs.
- **Documentation Output Control:** Determines output format (e.g., Markdown), whether to include original code, and layout details like side-by-side displays.
- **Documentation Template Management:** Supplies extensive, customizable templates for all documentation artifacts—ranging from file-level prose to high-level project, architecture, and user/developer guides. This allows fine-grained control over generated document structure and content.
- **Retry Logic for Robustness:** Provides settings to auto-retry failed or truncated generations and supplies a continuation prompt template to resume incomplete sections smoothly.

---

## Key Components

### 1. **Model Configuration (`model`)**
- `provider`: Sets AI backend (`openai`, `anthropic`, or `azure_openai`).
- `name`: Model name (e.g., `"gpt-4.1"`).
- `temperature`: Model creativity (set to `1` for `o4-mini` as required).
- `max_tokens`: The total output length the LLM can generate.
- `recursion_limit`: Controls maximum call depth for advanced workflows (e.g., LangGraph).

### 2. **Token Management (`token_limits`)**
- `max_context_tokens`: Caps context window for document context during processing.
- `summarization_threshold`: Triggers summarization for very large contexts.
- `chunk_size`: Sets how large each document chunk should be broken for processing.

### 3. **Processing Control (`processing`)**
- `max_files`: Maximum number of files to process (0/null for unlimited).
- `save_incrementally`: Whether to save documentation output as each file is completed.

### 4. **File Processing (`file_processing`)**
- `supported_extensions`: File extensions eligible for documentation.
- `exclude_patterns`: Directories and files to skip (e.g., caches, build outputs, binary logs, and common metadata files).

### 5. **Output Specification (`output`)**
- `format`: Format for generated documentation (e.g., `"markdown"`).
- `include_code`: Whether to embed original code within the documentation.
- `side_by_side`: Whether to use paired code-commentary in rendered output.

### 6. **Documentation Templates (`templates`)**
- `file_documentation`: Template for per-file docs using placeholders.
- `documents`: Nested configuration for **project_overview**, **architecture**, **user_guide**, **developer_guide**, and (optionally) **design**, **API**, **module**, **testing**, and **deployment** documentation. Each allows granular `enabled` flags, tokens limits, and fully editable generation instructions.

### 7. **Retry Logic (`retry_config`)**
- `max_retries`: How many times to retry failed/truncated generations.
- `retry_on_truncation`: Retry when output is incomplete due to token limit.
- `continuation_prompt`: Custom prompt for resuming incomplete output, keeping style and format consistent.

---

## Dependencies

- **Upstream consumers:** The documentation generator (`main.py`), MCP server (`mcp_server.py`), LangGraph-based workflows, and related tools (`test_mcp_tools.py`) all load and parse this configuration at startup or runtime.
- **Downstream usage:** All AI operations, file selection, output writing, and documentation structure strictly follow the logic described here.
- **Third-party:** This file assumes you use LLM providers named here (OpenAI, Anthropic, or Azure) and that your project structure and file types align with those in `supported_extensions` and `exclude_patterns`.

---

## Usage Examples

- **Default Operation**: When running documentation generation, the system loads `config.yaml` from its working directory to know which files to include, what LLM/model to call, and how to format resulting documentation.
    ```bash
    python main.py generate --repo-path /path/to/repo
    ```
    > Uses this config file to guide everything about the run.

- **Custom Model/Scope**: To change the LLM or restrict documentation to only a subset of filetypes, edit the `model` and `file_processing` sections accordingly (e.g., to use Claude instead of GPT, or add `.md` to extensions).

- **Enable/Disable Document Types**: You can selectively turn on or off entire documentation sections (like `architecture`, `developer_guide`, etc.) by toggling the `enabled` flag.

- **Template Customization**: To reword or localize documentation, edit the YAML templates—these are injected verbatim into LLM prompts.

- **Retry and Continuation**: Failed document generations (such as incomplete large section outputs) will be retried up to `max_retries`, automatically using the `continuation_prompt` template to resume from the last good output segment.

---

## Example Configuration Edit

Enabling API documentation:
```yaml
templates:
  api_documentation:
    enabled: true
    sections:
      - name: "api_overview"
        enabled: true
        max_tokens: 4096
        template: |
          # API Overview
          ...
```

Changing output format:
```yaml
output:
  format: "markdown"
  include_code: true
  side_by_side: false
```

---

## Summary

This configuration file is the **heart of customization and workflow definition** for the documentation generation pipeline. By editing it, users control every aspect of the documentation process—from what is documented, to how summaries are written, to how robust the system is in the face of model output truncation. It supports advanced, modular, and extensible documentation generation for diverse codebases and organizational needs.

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: 718e1e11d3f4b7a8e432a80d26ef0ba94f92cca240329dd3fdefe672bbba9f14
relative_path: config.yaml
generation_date: 2025-07-01T23:04:09.754263
```
<!-- END GENERATION METADATA -->
