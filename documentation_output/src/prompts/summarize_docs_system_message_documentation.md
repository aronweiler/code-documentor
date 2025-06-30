<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for src\prompts\summarize_docs_system_message.py

# File: `src/prompts/summarize_docs_system_message.py`

## Purpose

This file defines a system message prompt string used for instructing a language model (such as ChatGPT or other LLMs) on how to summarize technical documentation chunks. It is specifically crafted to guide the model toward producing summaries that retain essential technical information, architectural decisions, and relevant relationships.

## Functionality

The primary function of this file is to act as a configuration or utility that exposes a standardized system prompt. This prompt can be supplied to a language model as part of a summarization workflow to ensure consistency in summaries and adherence to desired summarization criteria.

### Details

- **Prompt Focus**: The prompt emphasizes retention of:
  1. Key technical concepts and terminology
  2. Important architectural decisions
  3. Critical implementation details
  4. Dependencies and relationships

- **Output Requirement**: Summaries should be both concise and comprehensive.

## Key Components

### Variables

- **`SUMMARIZE_DOCS_SYSTEM_MESSAGE`**:  
  A multi-line string containing explicit instructions for a language model acting as a "technical documentation summarizer."

  ```python
  SUMMARIZE_DOCS_SYSTEM_MESSAGE = """You are a technical documentation summarizer. 
  Summarize the following documentation chunk while preserving:
  1. Key technical concepts and terminology
  2. Important architectural decisions
  3. Critical implementation details
  4. Dependencies and relationships

  Keep the summary concise but comprehensive."""
  ```

## Dependencies

- **Internal Dependencies**:  
  None. This file is standalone and only provides a string constant.

- **External Dependencies**:  
  - Typically, this file will be used by code interfacing with a language model API, such as the OpenAI API or other summarization engines.

- **Downstream Usage**:  
  Other parts of the codebase that handle AI-driven documentation summarization will import and use this prompt.

## Usage Examples

### Example 1: Integrating with an LLM-based Summarization Pipeline

```python
from src.prompts.summarize_docs_system_message import SUMMARIZE_DOCS_SYSTEM_MESSAGE

def summarize_document_chunk(chunk, llm_client):
    response = llm_client.chat(
        system_message=SUMMARIZE_DOCS_SYSTEM_MESSAGE,
        user_message=chunk
    )
    return response['summary']

# Example use
documentation_chunk = "'''Documentation detailing system architecture...'''"
summary = summarize_document_chunk(documentation_chunk, llm_client)
print(summary)
```

### Example 2: Setting Up the System Prompt for an Agent

```python
import openai
from src.prompts.summarize_docs_system_message import SUMMARIZE_DOCS_SYSTEM_MESSAGE

messages = [
    {"role": "system", "content": SUMMARIZE_DOCS_SYSTEM_MESSAGE},
    {"role": "user", "content": "Paste documentation chunk here..."}
]

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=messages
)
print(response['choices'][0]['message']['content'])
```

---

This file is essential for maintaining a consistent approach to AI-assisted summarization of technical documentation across the project.

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: e4ac01d0bd7334d96e56907542f3b87fa44372917fa897e19b14c18800b7d6e0
relative_path: src\prompts\summarize_docs_system_message.py
generation_date: 2025-06-29T16:53:18.470983
```
<!-- END GENERATION METADATA -->
