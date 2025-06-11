<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for src\llm_manager.py

# LLMManager (src/llm_manager.py)

## Purpose
`LLMManager` centralizes the initialization and configuration of large language models (LLMs) from different providers (OpenAI or Anthropic). It abstracts away:
- Model selection (by provider name).
- API‐key retrieval (from config or environment).
- Provider‐specific initialization parameters (e.g., timeouts, default model names).

This enables downstream code to request a ready‐to‐use LLM instance without handling low‐level setup logic.

---

## Functionality

### Class: LLMManager
```python
class LLMManager:
    """Handles LLM initialization and configuration."""
```

#### `__init__(self, config_manager)`
- **Parameters**  
  - `config_manager`: An object with method `get_model_config()` returning a `dict` of model settings.
- **Behavior**  
  Stores the `config_manager` and configures a `logging.Logger` for internal status messages.

#### `initialize_llm(self) -> Union[ChatOpenAI, ChatAnthropic]`
- **Purpose**  
  Entry point to create and return a configured LLM instance.
- **Behavior**  
  1. Calls `config_manager.get_model_config()`.
  2. Reads the `"provider"` key (`"openai"` by default).
  3. Delegates to either `_initialize_openai_llm` or `_initialize_anthropic_llm`.
  4. Raises `ValueError` if the provider is unsupported.

#### `_initialize_openai_llm(self, model_config: dict) -> ChatOpenAI`
- **Purpose**  
  Instantiate an OpenAI‐backed LLM client.
- **Parameters**  
  - `model_config`:  
    - `"api_key"` (optional): Overrides `OPENAI_API_KEY` env var.  
    - `"name"` (optional, default `"gpt-4o"`): Model identifier.  
    - `"temperature"` (optional, default `0.2`): Sampling temperature.
- **Behavior**  
  1. Resolves `api_key` from config or `os.getenv("OPENAI_API_KEY")`.  
  2. Raises `ValueError` if no key is found.  
  3. Constructs `ChatOpenAI(...)` and logs an info message.

#### `_initialize_anthropic_llm(self, model_config: dict) -> ChatAnthropic`
- **Purpose**  
  Instantiate an Anthropic‐backed LLM client.
- **Parameters**  
  - `model_config`:  
    - `"api_key"` (optional): Overrides `ANTHROPIC_API_KEY` env var.  
    - `"name"` (optional, default `"claude-3.5-sonnet-latest"`): Model identifier.  
    - `"temperature"` (optional, default `0.2`): Sampling temperature.  
    - `"timeout"` (optional, default `60.0`): Request timeout in seconds.
- **Behavior**  
  1. Resolves `api_key` from config or `os.getenv("ANTHROPIC_API_KEY")`.  
  2. Raises `ValueError` if no key is found.  
  3. Constructs `ChatAnthropic(...)` and logs an info message.

---

## Key Components

- **LLMManager**  
  Orchestrates model‐provider selection and client instantiation.
- **config_manager**  
  External object (injected) responsible for supplying user/config‐file settings.
- **model_config** (`dict`)  
  Dictionary with keys:
  - `provider`: `"openai"` | `"anthropic"`
  - `api_key` (optional)
  - `name` (optional)
  - `temperature` (optional)
  - `timeout` (Anthropic only, optional)
- **ChatOpenAI**  
  Class from `langchain_openai` used to interact with OpenAI models.
- **ChatAnthropic**  
  Class from `langchain_anthropic` used to interact with Anthropic models.
- **Logger**  
  Standard `logging` logger for info and error reporting.

---

## Dependencies

### Python Packages
- `langchain_openai.ChatOpenAI`
- `langchain_anthropic.ChatAnthropic`
- Standard library: `os`, `logging`, `typing.Union`

### Environment Variables
- `OPENAI_API_KEY` (fallback for OpenAI)
- `ANTHROPIC_API_KEY` (fallback for Anthropic)

### Config Manager Contract
Any object passed as `config_manager` must implement:
```python
def get_model_config() -> dict:
    """
    Returns a dictionary containing at least the key 'provider'
    and optionally 'api_key', 'name', 'temperature', 'timeout'.
    """
```

### Downstream Usage
Components that require an LLM instance rely on:
```python
llm = LLMManager(config_manager).initialize_llm()
```
and then use the returned `llm` for chat/completion calls.

---

## Usage Examples

### 1. Simple OpenAI Initialization
```python
# Mock config manager
class SimpleConfig:
    def get_model_config(self):
        return {
            "provider": "openai",
            "api_key": "sk-xyz123",
            "name": "gpt-4",
            "temperature": 0.1
        }

config = SimpleConfig()
manager = LLMManager(config)
openai_llm = manager.initialize_llm()

# Now you can call openai_llm.chat(...) or similar
```

### 2. Using Environment Variables
```bash
export OPENAI_API_KEY="sk-env-abc"
```
```python
class EnvConfig:
    def get_model_config(self):
        return {"provider": "openai", "name": "gpt-3.5-turbo"}

env_manager = LLMManager(EnvConfig())
llm = env_manager.initialize_llm()
# API key is pulled from OPENAI_API_KEY
```

### 3. Anthropic Model with Custom Timeout
```python
class AnthropicConfig:
    def get_model_config(self):
        return {
            "provider": "anthropic",
            "api_key": "anthropic-key-123",
            "name": "claude-3.5-sonnet",
            "temperature": 0.5,
            "timeout": 120.0
        }

anthropic_manager = LLMManager(AnthropicConfig())
anthropic_llm = anthropic_manager.initialize_llm()
```

---

By encapsulating provider logic and key management, `LLMManager` ensures consistent LLM setup across your application.

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: ae3dcf853c1e98944816eb7e8e33a09c27f943f416711fcb1206e933a7a8d47d
relative_path: src\llm_manager.py
generation_date: 2025-06-10T22:38:41.199815
```
<!-- END GENERATION METADATA -->
