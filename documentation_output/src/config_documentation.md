<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for src/config.py

# src/config.py

## Purpose

This module provides configuration management for the project, including:

- Loading configuration settings from a YAML file (`config.yaml` by default).
- Managing sensitive environment variables, such as API keys, using `.env` files.
- Supplying model and provider-specific configuration settings to the application.

It improves the separation of configuration from code, centralizing environment-sensitive values and pipeline settings for easier development, deployment, and maintenance.

---

## Functionality

The key functionality is encapsulated in the `ConfigManager` class, which:

1. Loads and parses the main configuration YAML file according to a structured `PipelineConfig` model.
2. Loads environment variables from the `.env` file on initialization using `python-dotenv`.
3. Provides methods to:
    - Safely retrieve API keys for different providers (OpenAI, Anthropic, Azure OpenAI, etc.).
    - Combine static YAML configuration with dynamic, secure API keys and optional Azure-specific environment settings.

---

## Key Components

### Classes

#### `ConfigManager`

**Description:**  
Manages the lifecycle of application configuration, including loading YAML config files and injecting API keys from environment variables. Can be extended to support other providers or configuration sources.

**Constructor:**

- `__init__(self, config_path: str = "config.yaml")`:  
  Initializes `ConfigManager` and loads environment variables from `.env`.  
  - `config_path`: Path to the configuration YAML file. Defaults to `config.yaml`.

**Methods:**

- `load_config(self) -> PipelineConfig`:  
  Loads and parses the YAML configuration using `PipelineConfig` (imported from `.models`). Caches the result for subsequent calls.

- `get_api_key(self, provider: str) -> str`:  
  Retrieves the relevant API key for the given provider from environment variables. Provider must be one of `"openai"`, `"anthropic"`, or `"azure_openai"`.

- `get_model_config(self) -> Dict[str, Any]`:  
  Returns an augmented model configuration dictionary by merging base YAML config with the correct API key and, in the case of Azure OpenAI, additional settings (endpoint, deployment name, API version) from environment.

### External Dependencies

- **os**: To access environment variables.
- **yaml**: For parsing the YAML configuration file.
- **pathlib.Path**: For robust path manipulation.
- **dotenv.load_dotenv**: To load environment variables from a `.env` file.
- **.models.PipelineConfig**: Data model for the YAML configuration structure (assumed to be a Pydantic or similar data class).

### Configuration Files

- `.env`: Loaded automatically for environment variable management.
- `config.yaml`: Main configuration file for pipeline settings.

---

## Dependencies

### This file depends on:

- `os` (standard library)
- `yaml` (PyYAML)
- `pathlib.Path` (standard library)
- `dotenv.load_dotenv` (`python-dotenv` package)
- Local import: `.models.PipelineConfig` data model (must be defined elsewhere in your project).

### Code that depends on this file:

- Any code that requires structured, secure access to model configuration, API keys, or other project-level settings should utilize the `ConfigManager` class.

---

## Usage Examples

### Load and Access Full Config

```python
from src.config import ConfigManager

# Initialize (loads .env automatically)
cfg_mgr = ConfigManager('config.yaml')

# Load parsed PipelineConfig model from YAML
cfg = cfg_mgr.load_config()

# Access specific config sections
print(cfg.model)
```

### Get API Key for Provider

```python
api_key = cfg_mgr.get_api_key("openai")
print(api_key)
```

### Get Model Configuration (includes merged-in API key and Azure info)

```python
model_cfg = cfg_mgr.get_model_config()
print(model_cfg)
```

### Expected Environment

You should define the necessary variables in your `.env` file:

```env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_ENDPOINT=https://<your-azure-openai-endpoint>
AZURE_OPENAI_DEPLOYMENT_NAME=my-deployment
AZURE_OPENAI_API_VERSION=2023-12-01-preview
```

---

## Notes & Best Practices

- **Sensitive keys/credentials should never be committed to version control.** Keep `.env` in your `.gitignore`.
- Extendable for future providers by modifying `key_mapping` and the Azure-specific logic as needed.
- The `PipelineConfig` class structure should align with the format and fields expected in `config.yaml`.
- This file should be considered the single source of truth for all runtime configuration and credential needs.

---

## Related Files

- `src/models.py`: Must provide the `PipelineConfig` class.
- `.env`: For secret management.
- `config.yaml`: Project configuration settings.

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: b4886e508ee52a8b9582d55ece0dac4825215397b92b4735587e1a36e2e2edd2
relative_path: src/config.py
generation_date: 2025-06-30T00:04:43.290726
```
<!-- END GENERATION METADATA -->
