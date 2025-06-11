<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for config.yaml

# config.yaml Documentation

## Purpose

This file serves as the central configuration for a code and documentation pipeline, controlling how source code is processed, which AI models are used for documentation generation, how outputs are formatted, and how design and user documentation are structured. It centralizes all configurable aspects for consistent and reproducible documentation workflows.

## Functionality

The configuration covers all stages of the documentation pipeline:
- **Model Selection**: Specifies the AI model provider and parameters.
- **Token Management**: Sets limits for context and document chunking to manage resource usage.
- **Processing Settings**: Controls batch size and incremental output saving.
- **File Handling**: Defines what file extensions to process or ignore and folder/file exclusion rules.
- **Output Settings**: Sets documentation format options and whether to include source code or side-by-side views.
- **Documentation Templates**: Customizes the structure and placeholders for generated documentation.
- **Design Documentation**: Structures sections for project, architecture, design, user, developer, API, module, testing, and deployment documentation with granular control over what is generated.
- **Retry Strategy**: Sets parameters for retrying failed documentation generations, especially due to truncation.

## Key Components

### 1. model
- **Purpose**: AI model settings (provider, name, temperature, etc.).
- **Fields**: `provider`, `name`, `temperature`, `max_tokens`, `recursion_limit`.

### 2. token_limits
- **Purpose**: Manages token and chunk limits for both context and summarization operations.
- **Fields**: `max_context_tokens`, `summarization_threshold`, `chunk_size`.

### 3. processing
- **Purpose**: Controls high-level file batch processing behavior.
- **Fields**: `max_files`, `save_incrementally`.

### 4. file_processing
- **Purpose**: Manages which file types are supported and which patterns to exclude.
- **Fields**:
  - `supported_extensions`: List of relevant source/document files.
  - `exclude_patterns`: Folders and files to skip.

### 5. output
- **Purpose**: Output formatting and documentation presentation.
- **Fields**: `format`, `include_code`, `side_by_side`.

### 6. templates
- **Purpose**: YAML string templates for the generated documentation.
- **Fields**: `file_documentation` (template for file-level docs).

### 7. design_docs
- **Purpose**: High-level design documentation organization.
- **Structure**: Hierarchical. Categories include `project_overview`, `architecture`, `design`, `user_guide`, `developer_guide`, and other types, each with enabled sections and detailed templates.

### 8. retry_config
- **Purpose**: Retry and continuation policy for handling generation failures or truncations.
- **Fields**: `max_retries`, `retry_on_truncation`, `continuation_prompt`.

## Dependencies

- **Depends on**: 
  - The codebase and tooling that implements this pipeline must be able to read, parse, and apply YAML configuration.
  - AI model APIs (OpenAI, Anthropic, etc.) for generation.
  - File system access for processing source and saving outputs.
- **Depended on by**:
  - The main documentation pipeline or orchestration script.
  - Scripts/utilities that automate or refine documentation output.

## Usage Examples

### Example: Using the Configuration in a Pipeline Script

```python
import yaml

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Example: choosing model parameters
model_provider = config['model']['provider']
model_name = config['model']['name']

# Example: filtering files to process
supported_extensions = config['file_processing']['supported_extensions']
exclude_patterns = config['file_processing']['exclude_patterns']

# Example: applying output formatting options
output_format = config['output']['format']

# Example: iterating through design docs sections
if config['design_docs']['enabled']:
    for doc_name, doc_cfg in config['design_docs']['documents'].items():
        if doc_cfg['enabled']:
            for section in doc_cfg['sections']:
                if section['enabled']:
                    # Use section['name'], section['template'], etc.
                    pass
```

### Example: Customizing for a New AI Model

Change the `model` section:
```yaml
model:
  provider: "anthropic"
  name: "claude-3"
  temperature: 0.8
  max_tokens: 40000
  recursion_limit: 700
```

---

This file should be edited by those responsible for documentation automation, code analysis, or DevOps, and versioned alongside the rest of your project configuration.

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: 51b1c2fe919bcbc109ccc937fd69d5d951eb976886ec037da25ecde4867710e5
relative_path: config.yaml
generation_date: 2025-06-11T11:17:42.382648
```
<!-- END GENERATION METADATA -->
