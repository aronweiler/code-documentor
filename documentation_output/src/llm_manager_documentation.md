<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for src/llm_manager.py

# `llm_manager.py`

## Purpose

This module provides the `LLMManager` class, which is responsible for initializing and configuring Large Language Model (LLM) clients for use within an application, based on configuration parameters. It abstracts and unifies access to different LLM providers—specifically OpenAI and Anthropic—using the [LangChain](https://langchain.dev/) integrations for these services.

This abstraction allows the rest of the application to obtain a pre-configured LLM client from a supported provider without concerning itself with the details of provider selection, credential management, or low-level instantiation.

---

## Functionality

### Overview

- **LLMManager** is the main class, taking a configuration manager as its input dependency.
- It reads the LLM provider and relevant parameters (API key, model name, temperature, etc.) from the configuration manager or environment variables.
- It supports two providers:
  - OpenAI (via `langchain_openai.ChatOpenAI`)
  - Anthropic (via `langchain_anthropic.ChatAnthropic`)
- Provides logging information about which model and provider have been initialized.

### Main Methods

#### `initialize_llm(self)`

- Determines which provider to use (OpenAI or Anthropic).
- Calls the respective initialization helper (`_initialize_openai_llm` or `_initialize_anthropic_llm`).
- Returns an instance configured for the chosen provider.

#### `_initialize_openai_llm(self, model_config)`

- Acquires the OpenAI API key from the configuration or the `OPENAI_API_KEY` environment variable.
- Raises an error if the API key can't be found.
- Instantiates and returns a `ChatOpenAI` object with specified model name and temperature.
- Logs model initialization.

#### `_initialize_anthropic_llm(self, model_config)`

- Similar to OpenAI, fetches the Anthropic API key from config or `ANTHROPIC_API_KEY` environment variable.
- Raises an error if the key is missing.
- Instantiates and returns a `ChatAnthropic` object with specified parameters including timeout.
- Logs model initialization.

---

## Key Components

### Classes

- **LLMManager**
  - `__init__(config_manager)`: Stores reference to the configuration, prepares logger.
  - `initialize_llm()`: Public method to create the right LLM client.
  - `_initialize_openai_llm(model_config)`: Helper for OpenAI setup.
  - `_initialize_anthropic_llm(model_config)`: Helper for Anthropic setup.

### Dependencies

- `os`: To access environment variables for API keys.
- `logging`: To log provider/model initialization.
- `langchain_openai.ChatOpenAI`: Client for OpenAI LLMs.
- `langchain_anthropic.ChatAnthropic`: Client for Anthropic LLMs.
- `config_manager` (an external object): Must provide a `get_model_config()` method returning a dictionary with LLM configuration parameters.

### Key Variables

- **config_manager**: Externally provided configuration interface.
- **logger**: For logging initiation events and errors.

---

## Dependencies

**Required:**

- [`langchain-openai`](https://pypi.org/project/langchain-openai/) (`ChatOpenAI`)
- [`langchain-anthropic`](https://pypi.org/project/langchain-anthropic/) (`ChatAnthropic`)
- Python standard libraries: `os`, `logging`
- A configuration manager object passed to `LLMManager`, with a `get_model_config()` method.

**Used by:**

- All application components needing a configured LLM client (ChatOpenAI or ChatAnthropic) for inference or chat tasks.

---

## Usage Examples

```python
# Assume you have a config_manager object with a get_model_config() method
from src.llm_manager import LLMManager

config_manager = ...  # Your config manager implementation

llm_manager = LLMManager(config_manager)

# Initialize the proper LLM client based on configuration (OpenAI or Anthropic)
llm_client = llm_manager.initialize_llm()

# Now use the llm_client for your inference tasks (see LangChain docs for details)
response = llm_client.invoke("Hello, world!")

print(response)
```

**Example configuration (which config_manager.get_model_config() might return):**
```python
{
    "provider": "openai",
    "name": "gpt-4o",
    "temperature": 0.3,
    "api_key": "sk-...",
}
```

If API keys are not provided in configuration, be sure that
- `OPENAI_API_KEY` (for OpenAI) or
- `ANTHROPIC_API_KEY` (for Anthropic)
are set in your environment variables.

---

## Notes

- If an unsupported provider is specified, a `ValueError` will be raised.
- If the necessary API key is missing, a `ValueError` will be raised.
- Timeouts for Anthropic models can be specified in the configuration, defaulting to 60 seconds.
- This module does not perform any model inference itself—it just constructs and returns the appropriate, configured LLM backend for consumer code to use.

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: ae3dcf853c1e98944816eb7e8e33a09c27f943f416711fcb1206e933a7a8d47d
relative_path: src/llm_manager.py
generation_date: 2025-06-30T00:08:08.491228
```
<!-- END GENERATION METADATA -->
