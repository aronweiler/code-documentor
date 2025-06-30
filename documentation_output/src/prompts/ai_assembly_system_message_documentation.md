<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for src\prompts\ai_assembly_system_message.py

# ai_assembly_system_message.py

## Purpose

This file defines a system message prompt template for an AI tasked with assembling a complete document from separate sections. Its core use is to instruct the AI on how to generate a cohesive, well-structured document, ensuring high-quality outputs in applications that require combining individual document fragments into a finished whole.

## Functionality

The file contains a single string constant, `AI_ASSEMBLY_SYSTEM_MESSAGE`, which serves as a template prompt. This message guides the AI to:

1. Create an appropriate document title and introduction.
2. Ensure smooth transitions and logical flow between provided sections.
3. Add connecting or bridging text as needed.
4. Maintain a consistent tone and style throughout the document.
5. Conclude the document effectively, if applicable.
6. Avoid simple concatenation of sections; instead, produce a unified, well-written document.

The `{document_name}` placeholder in the string is designed for dynamic formatting, allowing users to specify the type or name of the document being assembled.

## Key Components

- **AI_ASSEMBLY_SYSTEM_MESSAGE**:  
  A multi-line string template (Python triple-quoted string), containing step-by-step instructions intended for system-level use with LLMs (Large Language Models).

  ```python
  AI_ASSEMBLY_SYSTEM_MESSAGE = """You are assembling a {document_name} document from individual sections.

  Your task is to:
  1. Create a coherent document title and introduction
  2. Ensure smooth transitions between sections
  3. Add any necessary connecting text
  4. Maintain consistency in tone and style
  5. Add a conclusion if appropriate

  The document should read as a unified whole, not just concatenated sections."""
  ```

## Dependencies

- **Dependencies (Imports):**  
  There are no imports or external dependencies in this file.
  
- **Dependent components:**  
  This file is typically imported or referenced by Python code that interacts with language models (like OpenAI GPT), especially in a document-generation or assembly system. Wherever a system prompt is required for guiding an LLM in assembling documents, this template would be used.

## Usage Examples

Below are examples of how this prompt might be used in the context of an AI document assembly pipeline:

```python
from src.prompts.ai_assembly_system_message import AI_ASSEMBLY_SYSTEM_MESSAGE

# Format the system message for use with a specific document type
system_prompt = AI_ASSEMBLY_SYSTEM_MESSAGE.format(document_name="project report")

# Pass the formatted prompt to your LLM API call or document assembly function
response = call_llm_api(
    system_message=system_prompt,
    user_sections=[
        "Section 1: Introduction...",
        "Section 2: Methods...",
        "Section 3: Results...",
        "Section 4: Discussion...",
    ]
)
```

**Typical Workflow:**
1. Import the template.
2. Format it with the desired `document_name`.
3. Use the resulting prompt as the system message for an LLM that is tasked with assembling document sections.

---

**Note:**  
This file is typically used as part of a larger system involving LLM-based document creation, and is not meant to be run standalone. It supports maintainable prompt engineering by centralizing and reusing prompt templates.

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: c6a768940b1be6ef01ee2659d6c18c8329a0660c94b8121c3b2e88d2ffbddaec
relative_path: src\prompts\ai_assembly_system_message.py
generation_date: 2025-06-29T16:53:03.979121
```
<!-- END GENERATION METADATA -->
