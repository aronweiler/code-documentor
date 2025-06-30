<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for src\config.py

# config.py

## Purpose

The `config.py` file provides configuration management for your application. It enables the loading and parsing of configuration data from a YAML file and environment variables, particularly for API keys and model-related settings. This centralizes configuration handling for consistent access across the project and enforces best practices for managing sensitive credentials.

## Functionality

The core logic is encapsulated in the `ConfigManager` class, which handles:

- Loading persistent configuration from a YAML file (default: `config.yaml`).
- Loading environment variables (from a `.env` file using `python-dotenv`).
- Providing convenient access to API keys for supported providers (OpenAI, Anthropic, Azure OpenAI).
- Assembling a comprehensive model configuration dictionary, optionally including additional provider-specific values.

## Key Components

### Classes

#### `ConfigManager`

Manages all aspects of application configuration, including YAML loading and environment variable access.

**Methods:**

- `__init__(self, config_path: str = "config.yaml")`
  - Initializes the manager, sets the config file path, and loads `.env` vars.
- `load_config(self) -> PipelineConfig`
  - Loads and parses the main configuration file into a `PipelineConfig` dataclass (from `.models`).
  - Caches the result for subsequent calls.
- `get_api_key(self, provider: str) -> str`
  - Retrieves the correct API key from environment variables based on the provider (`openai`, `anthropic`, or `azure_openai`).
  - Raises an error if the provider or key is missing.
- `get_model_config(self) -> Dict[str, Any]`
  - Returns a dict suitable for model instantiation or API calls, including embedded API keys and, if needed, Azure-specific values.

### Variables

- `config_path`: Path to the YAML configuration file (default: `config.yaml`).
- `_config`: Cached loaded config object.

### External References

- `PipelineConfig` (imported from `.models`): Expected to be a dataclass or object modeling your pipeline configuration.

## Dependencies

### External Packages

- [`os`](https://docs.python.org/3/library/os.html): For accessing environment variables.
- [`yaml`](https://pyyaml.org/): For loading YAML configuration files.
- [`dotenv`](https://pypi.org/project/python-dotenv/): For loading environment variables from a `.env` file.
- [`pathlib`](https://docs.python.org/3/library/pathlib.html): For robust filesystem path handling.
- `PipelineConfig` from your local `.models` module.

### Internal

- This file depends on a `PipelineConfig` class (from `.models`) that matches the expected config schema (must accept dict-unpacking).
- Typical usage assumes a `config.yaml` exists and that relevant API keys are present in a `.env` file.

### Downstream

- Any component that needs access to unified configuration (e.g., model initialization, service clients, etc.) should instantiate and use the `ConfigManager`.

## Usage Examples

### Example 1: Basic Configuration Loading

```python
from src.config import ConfigManager

config_mgr = ConfigManager()
pipeline_config = config_mgr.load_config()
print(pipeline_config.some_setting)
```

### Example 2: Get Model Configuration with API Key

```python
from src.config import ConfigManager

config_mgr = ConfigManager()
model_config = config_mgr.get_model_config()
print(model_config)
# Output includes: provider, api_key, and (if Azure) azure-specific keys
```

### Example 3: Fetch Specific API Key

```python
from src.config import ConfigManager

config_mgr = ConfigManager()
openai_key = config_mgr.get_api_key("openai")
print("OpenAI key:", openai_key)
```

## Notes

- You **must** provide a `.env` file with the necessary API keys (e.g., `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, etc.).
- The required YAML config structure must match what `PipelineConfig` expects.
- Azure-specific fields are only added if `provider` is set to `'azure_openai'` in your config.

---

**Recommendation:** Place this file at the root of your `src` package and ensure that all services or scripts consistently use this configuration manager. This makes configuration changes, credential rotation, and environment switching much easier to manage.

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: b4886e508ee52a8b9582d55ece0dac4825215397b92b4735587e1a36e2e2edd2
relative_path: src\config.py
generation_date: 2025-06-30T14:14:21.042391
```
<!-- END GENERATION METADATA -->
