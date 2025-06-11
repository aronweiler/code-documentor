<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for src\utilities\token_manager.py

# Token Manager Documentation

## 1. Purpose

The **token_manager.py** module provides utilities for token counting and budget tracking when interacting with large language models (LLMs). It abstracts away the complexity of loading model‐specific encoders, counting tokens in free‐form text or chat messages, and falling back to rough estimates when encoders fail. This helps ensure requests to LLM APIs stay within token limits and assists in context optimization.

---

## 2. Functionality

### TokenCounter Class

A single, reusable class that:

- Loads and caches tiktoken encoders for supported models.
- Counts exact tokens in arbitrary text per model.
- Maps ambiguous model names to the correct encoder.
- Estimates token usage for structured chat messages, including protocol overhead.

#### Public Methods

1. **`count_tokens(text: str, model: str = "default") -> int`**  
   - Returns the number of tokens in the given `text`, according to the specified `model`.  
   - Falls back to a rough estimation (`words * 1.3`) if encoding fails.

2. **`estimate_tokens_for_messages(messages: List[Dict[str, str]], model: str = "default") -> int`**  
   - Takes a list of chat‐style messages (each a `{"role": ..., "content": ...}` dict).  
   - Counts tokens for each message’s content and adds fixed overhead per message and for the overall conversation.  
   - Returns the estimated total.

#### Internal Helpers

- **`_load_encoders()`**  
  Loads `tiktoken` encoders for:
  - `gpt-4`
  - `gpt-3.5-turbo`
  - `text-davinci-003`  
  Falls back to a default `cl100k_base` encoder on failure.

- **`_get_encoder_key(model: str) -> str`**  
  Normalizes arbitrary model name strings to one of the encoder keys:
  - `"gpt-4"`
  - `"gpt-3.5-turbo"`
  - `"text-davinci-003"`
  - `"default"`

---

## 3. Key Components

- **TokenCounter**  
  The central class that encapsulates all token‐counting logic.

- **Encoders Cache (`self.encoders`)**  
  A `dict` mapping model‐keys to `tiktoken.Encoding` instances for fast lookup.

- **Logger (`logger`)**  
  A module‐level `logging.Logger` used for warnings when encoder loading or tokenization fails.

---

## 4. Dependencies

### External

- **tiktoken**  
  - Required for precise tokenization per OpenAI model.  
  - Encoder lookup via `tiktoken.encoding_for_model` and `tiktoken.get_encoding`.

- **logging**  
  - Used to report warnings when loading encoders or encoding text fails.

- **typing**  
  - Provides `Dict` and `List` type hints.

### Internal

- No other internal modules depend on this file by default.  
- Other components in the project that need token accounting or context‐length management should import and use `TokenCounter`.

---

## 5. Usage Examples

```python
from src.utilities.token_manager import TokenCounter

# Initialize the token counter
token_counter = TokenCounter()

# 1. Count tokens in plain text
text = "Hello, how are you today?"
num_tokens = token_counter.count_tokens(text, model="gpt-3.5-turbo")
print(f"Text token count: {num_tokens}")

# 2. Estimate tokens for a chat conversation
chat_messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What's the weather like today?"},
    {"role": "assistant", "content": "It's sunny and 75°F."},
]
estimated_tokens = token_counter.estimate_tokens_for_messages(
    chat_messages, model="gpt-4"
)
print(f"Estimated tokens for conversation: {estimated_tokens}")

# 3. Handling fallback for unsupported model
unknown_model_tokens = token_counter.count_tokens(
    "Sample text for unknown model.", model="my-custom-model"
)
print(f"Tokens counted (fallback): {unknown_model_tokens}")
```

---

### Notes

- The per-message overhead of **4 tokens** and the final conversation overhead of **3 tokens** are rough estimates aligned with typical OpenAI chat protocol framing.
- In scenarios where precise token counts are critical (e.g., billing or exact context slicing), always prefer supported models and rely on `tiktoken` rather than the fallback heuristic.
- Ensure that the `tiktoken` package is installed and up to date:
  ```bash
  pip install tiktoken
  ```

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: f712c7ac9c0ca70abd57a06d5ee5bd2587fbbc1ff65cb1c95327d5eb4854f9d9
relative_path: src\utilities\token_manager.py
generation_date: 2025-06-10T21:52:55.563806
```
<!-- END GENERATION METADATA -->
