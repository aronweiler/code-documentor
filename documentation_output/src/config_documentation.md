<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for src\config.py

# ConfigManager Module Documentation

## Purpose

The `ConfigManager` module is designed to handle the loading and management of configuration settings for an application. It primarily deals with reading configuration data from a YAML file and environment variables, specifically focusing on API keys and model configurations. This module is essential for applications that require dynamic configuration management, especially those interacting with external APIs.

## Functionality

### Class: `ConfigManager`

The `ConfigManager` class is the core component of this module. It provides methods to load configuration data and retrieve API keys from environment variables.

#### `__init__(self, config_path: str = "config.yaml")`

- **Description**: Initializes the `ConfigManager` instance. It sets the path to the configuration file and loads environment variables from a `.env` file.
- **Parameters**:
  - `config_path` (str): The path to the YAML configuration file. Defaults to `"config.yaml"`.

#### `load_config(self) -> PipelineConfig`

- **Description**: Loads configuration data from a YAML file and returns it as a `PipelineConfig` object. This method ensures that the configuration is loaded only once and cached for future use.
- **Returns**: An instance of `PipelineConfig` containing the configuration data.

#### `get_api_key(self, provider: str) -> str`

- **Description**: Retrieves the API key for a specified provider from environment variables.
- **Parameters**:
  - `provider` (str): The name of the provider for which the API key is required. Supported providers include "openai", "anthropic", and "azure_openai".
- **Returns**: The API key as a string.
- **Raises**: 
  - `ValueError` if the provider is unknown or if the API key is not found in the environment variables.

#### `get_model_config(self) -> Dict[str, Any]`

- **Description**: Retrieves the model configuration, including the necessary API keys. It also adds Azure-specific configuration details if the provider is "azure_openai".
- **Returns**: A dictionary containing the model configuration.

## Key Components

- **Classes**: 
  - `ConfigManager`: Manages configuration loading and API key retrieval.
- **Methods**:
  - `load_config()`: Loads and caches configuration data.
  - `get_api_key()`: Retrieves API keys from environment variables.
  - `get_model_config()`: Combines model configuration with API keys.
- **External Dependencies**:
  - `yaml`: For parsing YAML configuration files.
  - `os`: For accessing environment variables.
  - `dotenv`: For loading environment variables from a `.env` file.
  - `PipelineConfig`: A model class presumably defined in the `models` module for handling configuration data.

## Dependencies

- **Imports**:
  - `os`: Standard library module for environment variable access.
  - `yaml`: Third-party library for YAML file parsing.
  - `dotenv`: Third-party library for loading environment variables from a `.env` file.
  - `PipelineConfig`: A class from the local `models` module, used to structure the configuration data.
- **Environment Variables**: Requires a `.env` file with API keys and possibly other configuration details.

## Usage Examples

```python
from src.config import ConfigManager

# Initialize the ConfigManager
config_manager = ConfigManager()

# Load the configuration
pipeline_config = config_manager.load_config()

# Retrieve an API key for a specific provider
api_key = config_manager.get_api_key("openai")

# Get the complete model configuration
model_config = config_manager.get_model_config()
```

This module is typically used in applications that require structured configuration management and secure handling of API keys, especially in environments where different API providers are used.

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: b4886e508ee52a8b9582d55ece0dac4825215397b92b4735587e1a36e2e2edd2
relative_path: src\config.py
generation_date: 2025-06-10T20:41:37.684278
```
<!-- END GENERATION METADATA -->
