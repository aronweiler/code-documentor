<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for config.yaml

# config.yaml Documentation

## Purpose

The `config.yaml` file serves as the central configuration for the documentation pipeline. It defines operational, processing, and output behaviors for generating, organizing, and formatting documentation across a codebase. This configuration file ensures the pipeline is both flexible and reproducible, supporting varied codebases and documentation requirements.

## Functionality

This configuration file primarily:

- Specifies AI model parameters and how large language models (LLMs) are used for code/documentation generation.
- Sets limits for processing, chunking, and summarizing large codebases for efficient memory and performance management.
- Defines which file types and directory patterns should be included or excluded from processing.
- Sets output options, including formatting (e.g. Markdown), contents of the documentation, and organization.
- Includes comprehensive templates for multiple documentation types, including project overview, architecture, detailed design, user and developer guides, and more.
- Contains retry logic for resilient handling of LLM generation errors or truncations.

The configuration is declarative and does not execute code itself, but is referenced by components of the documentation pipeline to guide their behavior.

## Key Components

### 1. AI Model Configuration (`model`)
- **provider**: Selects the LLM provider (`openai`, `anthropic`, `azure_openai`).
- **name**: LLM model name (e.g., `"gpt-4.1"`).
- **temperature**: Controls model creativity.
- **max_tokens**: Limits LLM output length.
- **recursion_limit**: Controls recursion depth in document analysis (useful for deep scans).

### 2. Token Management (`token_limits`)
- **max_context_tokens**: Max tokens for context fed to the LLM.
- **summarization_threshold**: Triggers summarization for large contexts.
- **chunk_size**: Size of chunks to split large documents.

### 3. Processing Controls (`processing`)
- **max_files**: Caps number of files processed per run.
- **save_incrementally**: If true, saves intermediate files to prevent data loss.

### 4. File Processing Settings (`file_processing`)
- **supported_extensions**: Lists allowable code/document file types.
- **exclude_patterns**: Glob patterns and directories to skip.

### 5. Output Options (`output`)
- **format**: Output format, typically `"markdown"`.
- **include_code**: Whether to include original code snippets.
- **side_by_side**: Whether to generate side-by-side (code and docs) output.

### 6. Documentation Templates (`templates`)
- **file_documentation**: Top-level template for each code file's docs.
- **documents**: Hierarchical, modular templates for:
    - Project overview
    - Architecture
    - Design
    - User guide
    - Developer guide
    - API and module documentation (can be toggled on/off)
    - Testing and deployment docs
- Each section has enablement settings, token limits, and rich instructions.

### 7. Retry Configuration (`retry_config`)
- **max_retries**: How often to retry failed LLM generations.
- **retry_on_truncation**: Whether to retry when responses are truncated.
- **continuation_prompt**: Prompt template for seamless continuations if output is cut off.

## Dependencies

### What this file depends on
- The documentation pipeline's core code, which must read, parse, and obey this YAML structure.
- LLM providers (OpenAI, Anthropic, etc.) referenced in the `model` block.

### What depends on this file
- All documentation generation scripts or services: they use this configuration to determine processing logic, file inclusion/exclusion, output format, and document structure.
- Any CI/CD pipeline stages responsible for automated documentation.

## Usage Examples

### Example 1: Using the Configuration in a Documentation Pipeline
```python
import yaml

# Load config.yaml at the start of the documentation pipeline
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Example usage:
model_provider = config['model']['provider']
file_exts = config['file_processing']['supported_extensions']
if config['output']['side_by_side']:
    # generate side-by-side docs
    ...
```

### Example 2: Setting up for Incremental Runs
- A large codebase sets `processing.max_files: 1000` and `save_incrementally: true` to allow pausing/resuming documentation.
- The CLI entrypoint references this file:
    ```sh
    docgen --config config.yaml --src ./myrepo
    ```
    The generator respects all inclusion/exclusion patterns and output formats specified herein.

### Example 3: Advanced Template Customization
- A team wants to disable API docs and enable only user/developer guides:  
    Set `templates.api_documentation.enabled: false`,  
    Ensure `templates.user_guide` and `templates.developer_guide` have `enabled: true`.

---

> **Note**: Changes to this file take effect the next time the documentation pipeline is run. When evolving your project structure or documentation goals, update the templates or processing rules accordingly for best results.

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: 4995b6941949c37e41789f28227d1128e85f4f48cc99be5a18400f0288abf324
relative_path: config.yaml
generation_date: 2025-06-30T14:13:59.229293
```
<!-- END GENERATION METADATA -->
