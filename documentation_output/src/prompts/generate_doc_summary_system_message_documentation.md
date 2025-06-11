<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for src\prompts\generate_doc_summary_system_message.py

```markdown
# Module: src/prompts/generate_doc_summary_system_message.py

## 1. Purpose
This module defines a single system‐level prompt constant used by an AI-driven documentation summarizer.  
It exists to centralize and standardize the instructions that guide an LLM to produce concise 2–4 sentence summaries of code documentation, focusing on what the code does (its purpose and key components).

## 2. Functionality
- Exposes one constant, `GENERATE_DOC_SUMMARY_SYSTEM_MESSAGE`, which contains the exact text of the system prompt.  
- This prompt is designed to be fed into a chat or completion API (e.g., OpenAI’s Chat API) as the “system” message, instructing the model how to generate summary outputs.

## 3. Key Components
- **GENERATE_DOC_SUMMARY_SYSTEM_MESSAGE** (str)  
  A multi-line string that instructs the AI to:
  1. Create a concise 2–4 sentence summary of provided documentation.  
  2. Focus on the primary purpose/function and key components.  
  3. Maintain brevity and relevance, helping the AI quickly assess task relevance.

## 4. Dependencies
- **This file has no external library dependencies.**  
- **Consumers:** Any part of the codebase responsible for constructing or dispatching prompts to an LLM for documentation summarization will import this constant. Typical consumers include:
  - A prompt‐builder or orchestrator module  
  - A documentation evaluation or search service  
  - Testing utilities that verify prompt correctness

## 5. Usage Examples

### Example A: Passing to an LLM client
```python
from src.prompts.generate_doc_summary_system_message import GENERATE_DOC_SUMMARY_SYSTEM_MESSAGE
from openai import ChatCompletion

response = ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": GENERATE_DOC_SUMMARY_SYSTEM_MESSAGE},
        {"role": "user", "content": "'''def add(a, b): return a + b''' – This function adds two numbers."}
    ]
)
summary = response.choices[0].message["content"]
print("Doc summary:", summary)
```

### Example B: Integrating into a prompt builder
```python
# prompt_builder.py
from src.prompts.generate_doc_summary_system_message import GENERATE_DOC_SUMMARY_SYSTEM_MESSAGE

def build_summary_prompt(doc_text: str) -> list[dict]:
    return [
        {"role": "system", "content": GENERATE_DOC_SUMMARY_SYSTEM_MESSAGE},
        {"role": "user",   "content": doc_text}
    ]
```

---

*End of documentation for* `generate_doc_summary_system_message.py`
```

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: 5052cfc72f965151e3a9afd53342b388793ab563f84849998895122b5b9fd3a3
relative_path: src\prompts\generate_doc_summary_system_message.py
generation_date: 2025-06-10T22:39:14.168068
```
<!-- END GENERATION METADATA -->
