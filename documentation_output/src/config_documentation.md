<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for src\config.py

# `src/config.py`

## Purpose

This file provides a centralized configuration manager for the documentation toolkit and MCP server ecosystem. It is responsible for:

- Loading and validating configuration settings from a YAML file (`config.yaml`)
- Managing environment variables (including API keys) loaded via `.env` files
- Providing an interface to access configuration values and sensitive credentials in a secure and consistent way across the project

This abstraction helps keep configuration logic separate from tool/app logic and ensures all secrets are loaded in one place.

---

## Functionality

### The `ConfigManager` Class

The `ConfigManager` class is the core of this module. Its responsibilities include:

- **Initialization**: Loads environment variables using `python-dotenv` upon instantiation and stores the config file path.
- **YAML Config Loading**: Loads static configuration values from a specified YAML file (defaults to `config.yaml`).
- **API Key Management**: Retrieves API keys for different LLM providers (OpenAI, Anthropic, Azure OpenAI) from the environment.
- **Model Configuration**: Provides a dictionary for the currently selected LLM provider, with all necessary API keys and endpoints embedded for easy downstream use.

Methods:

#### `__init__(config_path: str = "config.yaml")`
- Loads `.env` environment variables at import time.
- Stores the config file path for later use.

#### `load_config() -> PipelineConfig`
- Loads configuration details from a YAML file only once and caches the result.
- Constructs a `PipelineConfig` object (imported from `src/models.py`) with these settings.

#### `get_api_key(provider: str) -> str`
- Maps provider names (`openai`, `anthropic`, `azure_openai`) to corresponding environment variable names.
- Looks up the API key for the provider from the loaded environment.
- Raises errors if the provider is unknown or the required key is missing.

#### `get_model_config() -> Dict[str, Any]`
- Fetches the model configuration dictionary from the loaded YAML.
- Adds the appropriate API key to the config, invoking `get_api_key`.
- If using Azure OpenAI, pulls in further Azure-specific settings from environment variables.
- Returns a dictionary suitable for initializing LLM interfaces.

---

## Key Components

- **Class:** `ConfigManager` – Main configuration handler.
- **Method:** `load_config` – Loads and parses the YAML config, returning a `PipelineConfig` object.
- **Method:** `get_api_key` – Secure lookup of API keys by provider.
- **Method:** `get_model_config` – Aggregates API credentials into the model's runtime configuration.
- **Variable:** `self._config` – Cached object to avoid repeated disk reads.
- **Dependency:** `PipelineConfig` – Typed configuration object loaded from YAML.
- **Dependencies on environment:** Reads `.env` via `dotenv` for secrets.

---

## Dependencies

### Imports

- `os` – Accesses system environment variables.
- `yaml` – Parses the YAML configuration file.
- `dotenv.load_dotenv` – Loads secrets from a `.env` file in root or project folder.
- `pathlib.Path` – Filesystem-safe path handling.
- `typing.Dict, Any` – For type annotations.
- `.models.PipelineConfig` – Project's structured configuration class (must be present in `src/models.py`).

### Consumed By

- This config manager is imported by the MCP server, the documentation generation toolkit (main.py), and potentially any tool needing unified access to configuration and secrets.

---

## Usage Examples

**Typical configuration loading pattern:**

```python
from src.config import ConfigManager

# Instantiate config manager (uses default config.yaml)
config_manager = ConfigManager()

# Load and access YAML configuration as an object
config = config_manager.load_config()
print('Repository root:', config.repo_path)
print('LLM settings:', config.model)

# Retrieve API key for current provider
api_key = config_manager.get_api_key(config.model['provider'])

# Get full model configuration for initializing an LLM interface
model_config = config_manager.get_model_config()
llm = SomeLLMClass(**model_config)
```

**Environment Variable Setup:**

- Place your secret keys in the project root `.env` file:

  ```
  OPENAI_API_KEY=sk-...
  ANTHROPIC_API_KEY=...
  AZURE_OPENAI_API_KEY=...
  AZURE_OPENAI_ENDPOINT=...
  AZURE_OPENAI_DEPLOYMENT_NAME=...
  AZURE_OPENAI_API_VERSION=2023-12-01-preview
  ```

**Config YAML Example** (`config.yaml`):
```yaml
repo_path: /path/to/target/repo
model:
  provider: openai
  model_name: gpt-4-turbo
  temperature: 0.7
  # ... other LLM params
```

---

## Notes & Best Practices

- Always ensure your `.env` file is present and up to date; API key retrieval will fail loudly if not.
- Do not check sensitive keys into version control.
- Extend `get_api_key` if your project supports additional LLM providers.

---

## Summary Table

| Component         | Purpose                                      |
|-------------------|----------------------------------------------|
| ConfigManager     | Unified config and secret loader             |
| load_config()     | Loads and caches YAML config as PipelineConfig|
| get_api_key()     | Secure, provider-based API key lookup        |
| get_model_config()| Returns all provider settings for LLM use    |
| PipelineConfig    | Typed schema for config (imported)           |

---

**This config manager is the single source of truth for parameters and sensitive credentials in your documentation and MCP ecosystem.**

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: b4886e508ee52a8b9582d55ece0dac4825215397b92b4735587e1a36e2e2edd2
relative_path: src\config.py
generation_date: 2025-07-01T23:05:25.118973
```
<!-- END GENERATION METADATA -->
