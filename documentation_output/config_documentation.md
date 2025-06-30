<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for config.yaml

# config.yaml Documentation

## Purpose

The `config.yaml` file serves as the central configuration file for a documentation pipeline that generates comprehensive technical documentation for codebases. This configuration allows you to tailor the documentation generation process, choose which document types are produced, set templates, define file processing rules, and tune AI model settings for the generation of structured documentation such as project overviews, user guides, architecture docs, and more.

## Functionality

This file defines how the documentation tool processes code, manages AI generation, and outputs documentation. Major configuration sections include:

- **model**: Specifies which AI provider and model is used, along with generation parameters (e.g., temperature, token limits, recursion).
- **token_limits**: Sets token budgets for context management and summarization, crucial for managing large source code bases.
- **processing**: Controls the file processing pipeline, including max files to document and whether to save incrementally.
- **file_processing**: Lists file extensions to process and patterns to exclude (such as `node_modules`, `.git`, or build artifacts).
- **output**: Configures output format (e.g., Markdown), whether to include side-by-side code, and inclusion of original code.
- **templates**: Provides base templates for documentation structure and specific templates for each doc section type (e.g., executive summary, design, user guides, etc.).
- **retry_config**: Sets retry logic for handling truncations or failures in AI documentation generation.

## Key Components

### Top-Level Sections

- **model**:  
  - `provider`: AI model provider ("openai", "anthropic", etc.)
  - `name`: Specific AI model (e.g., "gpt-4.1")
  - `temperature`: AI creativity (set to 1 for o4-mini model)
  - `max_tokens`: Max generation size per request
  - `recursion_limit`: Max recursion for advanced pipeline logic (LangGraph)

- **token_limits**:
  - `max_context_tokens`: Token limit for context when generating docs
  - `summarization_threshold`: When to summarize to fit within context
  - `chunk_size`: For splitting large documents for processing

- **processing**:
  - `max_files`: Max files to process; set to 0/null for unlimited
  - `save_incrementally`: Whether to save processed docs as files are completed

- **file_processing**:
  - `supported_extensions`: List of allowed file extensions
  - `exclude_patterns`: Files/folders/patterns to skip

- **output**:
  - `format`: E.g., "markdown"
  - `include_code`: Include code in output?
  - `side_by_side`: Present documentation/code side-by-side

- **templates**:
  - `file_documentation`: Template for individual file docs
  - `documents`: Nested section controlling which high-level documents are generated (architecture, design, user guide, etc.)
    - Each document type has `enabled` flags, section ordering, maximum tokens, and templated instructions

- **retry_config**:
  - `max_retries`: How many times to retry failed generations
  - `retry_on_truncation`: If true, will resume/continue docs if generation is cut off by token limit
  - `continuation_prompt`: Template for resuming a truncated section

### Documentation Structure Settings

- **documents**: Controls generation of large-scale project documentation, such as:
  - `project_overview`
  - `architecture`
  - `design`
  - `user_guide`
  - `developer_guide`
  - `api_documentation`
  - `module_documentation`
  - `testing_documentation`
  - `deployment_documentation`
- Each of these can be enabled/disabled, subdivided into sections, and customized by template and token count.

## Dependencies

### What This File Depends On

- **AI Documentation Generation Tool**: Requires a documentation pipeline that reads this YAML file for its configuration.
- **AI Provider Credentials**: The referenced model providers (OpenAI, Anthropic, Azure-OpenAI) require account and access keys managed elsewhere.
- **File System Access**: The pipeline will scan code files according to the patterns here.

### What Depends On This File

- **Documentation Pipeline Entry Point**: All code/documentation generation processes depend on this file for configuration.
- **Template Expansion**: The pipeline uses the templates and settings here to create structured documentation.

## Usage Examples

### Basic Usage

1. **Configure the Model**  
   - Set the provider (`openai`), the specific model (`gpt-4.1`), and adjust generation parameters as needed.

2. **Customize File Processing**  
   - Modify `supported_extensions` to add or remove filetypes.
   - Tweak `exclude_patterns` to skip build/dev directories.

3. **Select Documentation Types**  
   - Under `templates.documents`, set `enabled: true` for the document sections you want (e.g., `project_overview`, `user_guide`).
   - Adjust section templates or token limits as needed.

4. **Run the Pipeline**  
   - The documentation generation tool will read `config.yaml` to drive:
     - Which files are processed
     - Which document structures/templates are used
     - How output is formatted and saved

**Example Workflow:**
```shell
# 1. Edit config.yaml as described above
# 2. Run your documentation tool, e.g.:
docgen --config config.yaml --src ./my_project/
# 3. Resulting docs will be generated as per your config (Markdown, with/without code, side-by-side)
```

### Enabling/Disabling Documentation Types

To disable API documentation (for example):
```yaml
api_documentation:
  enabled: false
```
To enable and customize project overview:
```yaml
project_overview:
  enabled: true
  sections:
    - name: "executive_summary"
      enabled: true
      # ... etc.
```

### Adjusting Output Format

To include original code in output:
```yaml
output:
  include_code: true
```

### Setting File Processing Limits

To process only a subset of files:
```yaml
processing:
  max_files: 100
```

## Summary

- **config.yaml** is the master control file for your AI-powered documentation pipeline.
- It enables fine-tuned, template-driven, scalable, and extensible project, user, developer, and file-level documentation.
- Adjust this file to change what gets documented, how, and with what AI/model and template settings.

---

*Edit this file to shape the entire documentation output for your codebase. For additional tuning, adapt section templates and parameters as required for your project's needs.*

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: 941bba0776274de18d0f5d59e8f6158cf149c965381fb4a84bc63a5e31826ee2
relative_path: config.yaml
generation_date: 2025-06-29T16:50:14.101795
```
<!-- END GENERATION METADATA -->
