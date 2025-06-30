<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for src/utilities/token_manager.py

# token_manager.py

## Purpose

This module provides robust utilities for token management in the context of interacting with Large Language Models (LLMs). It enables precise token counting, budget tracking, and context size optimization—critical for controlling usage and cost with models such as GPT-4, GPT-3.5, and related OpenAI APIs.

---

## Functionality

### TokenCounter Class

The central component of this module is the `TokenCounter` class, which offers methods to:

- **Count tokens** in any text for specific LLM models, using their model-appropriate encoding.
- **Estimate tokens** required for multi-message chat conversations, accounting for structural overhead.
- **Map model names** to the correct encoding tools internally, facilitating compatibility with different OpenAI models.
- **Handle encoder loading and fallback gracefully**, allowing approximate estimation if specific encoders or models are not available.

#### Class: `TokenCounter`

- **Constructor (`__init__`)**
  - Initializes the encoder dictionary and attempts to load encoders for common OpenAI models using `tiktoken`.
- **_load_encoders**
  - Establishes encoder objects for "gpt-4", "gpt-3.5-turbo", "text-davinci-003", and a default encoder.
  - Handles missing or failing encoders by falling back to a base encoding and logging a warning.
- **count_tokens**
  - Counts the tokens of a text string specific to a model, returning an integer.
  - If the encoding is unavailable or an error occurs, it provides a rough token count estimate.
- **_get_encoder_key**
  - Parses a model name into a canonical internal encoder key.
- **estimate_tokens_for_messages**
  - Estimates total token usage for a series of chat messages (list of dicts), adding overhead for each message and for the full conversation structure (matches OpenAI's chat API requirements).

---

## Key Components

- **TokenCounter**: Main utility class for all token calculation tasks.
- **count_tokens(text, model)**: Counts or estimates the number of tokens for the provided text using the model's encoding.
- **estimate_tokens_for_messages(messages, model)**: Estimates token usage for an array of chat messages in OpenAI-style format.
- **encoders (dict)**: Internal mapping of model names to tiktoken `Encoding` objects.
- **Logging**: Uses standard Python logging to warn about encoder or estimation problems.

---

## Dependencies

### External

- [`tiktoken`](https://github.com/openai/tiktoken): Required for model-specific encoding and token counting.
- Python `logging` standard library.

### Internal

- No other application-specific dependencies.
- This module is designed for use anywhere that requires knowledge of LLM token consumption, such as:
  - Prompt construction and limitation
  - Conversation budgeting
  - Usage/cost analysis

### What Depends On It

- Any module, function, or service that interacts with OpenAI APIs or needs to limit prompt/context size to fit under token limits.
- Likely a utility referenced by higher-level LLM interaction, budget, or orchestration components.

---

## Usage Examples

### Example 1: Counting Tokens in Text

```python
from utilities.token_manager import TokenCounter

counter = TokenCounter()
text = "This is an example input for token counting."
num_tokens = counter.count_tokens(text, model="gpt-3.5-turbo")
print(f"Token count for input text: {num_tokens}")
```

### Example 2: Estimating Tokens in a Conversation

```python
from utilities.token_manager import TokenCounter

counter = TokenCounter()
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello, who won the world cup in 2022?"},
    {"role": "assistant", "content": "Argentina won the FIFA World Cup in 2022."}
]
total_tokens = counter.estimate_tokens_for_messages(messages, model="gpt-4")
print(f"Token count for chat conversation: {total_tokens}")
```

### Example 3: Handling Unknown Models

```python
from utilities.token_manager import TokenCounter

counter = TokenCounter()
text = "Some input for a hypothetical LLM model."
num_tokens = counter.count_tokens(text, model="my-unknown-model")  # Uses default encoding
print(f"Token count: {num_tokens}")
```

---

## Notes

- For best accuracy when using proprietary LLMs, specify the correct `model` parameter.
- If a model's encoding is unavailable, the module gracefully falls back to a rough estimate, so total token counts may be slightly off for unsupported models.
- Overhead values (e.g., `4` tokens per message, `3` for conversation structure) are chosen to closely match OpenAI's recommendations, but may need adjustment for other providers.

---

## See Also

- [tiktoken documentation](https://github.com/openai/tiktoken)
- [OpenAI API Usage Guide](https://platform.openai.com/docs/guides/chat/introduction)

---

**Location:** `src/utilities/token_manager.py`

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: f712c7ac9c0ca70abd57a06d5ee5bd2587fbbc1ff65cb1c95327d5eb4854f9d9
relative_path: src/utilities/token_manager.py
generation_date: 2025-06-30T00:14:18.572299
```
<!-- END GENERATION METADATA -->
