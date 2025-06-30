<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for src/prompts/ai_assembly_system_message.py

# File: `src/prompts/ai_assembly_system_message.py`

## Purpose

This file defines a system message prompt for an AI agent tasked with assembling a document from multiple sections. The prompt guides the AI's behavior, ensuring the resulting output is coherent, unified, and polished, rather than a simple paste of independently written parts.

## Functionality

The core content of this file is the `AI_ASSEMBLY_SYSTEM_MESSAGE` string. This string serves as an instructional message, typically provided as a "system prompt" to Large Language Models (LLMs) such as OpenAI's GPT or similar systems. The message outlines the agent's responsibilities in constructing the final document, notably:

1. **Generating a title and introduction** for context and framing.
2. **Ensuring smooth transitions** to improve readability and flow.
3. **Adding connecting text** as necessary for coherence.
4. **Maintaining a consistent tone and style** throughout the document.
5. **Concluding the document** if appropriate.

These guidelines help the AI produce output that meets higher standards of narrative quality and professionalism.

## Key Components

- **`AI_ASSEMBLY_SYSTEM_MESSAGE`**  
  A multi-line string containing detailed step-by-step instructions for assembling a document from sections. The `{document_name}` placeholder allows customization for the specific document type or title, providing context for the AI.

## Dependencies

### Imports

- **None.**  
  This file contains only a single string definition and has no imports or external dependencies.

### Depended on by

- Any code that creates or configures LLM-powered assembly agents or pipelines and needs to instruct the AI on how to combine multiple document sections into a finished, well-organized document.
- Typically used in prompt engineering or AI pipeline definition for document assembly tasks.

## Usage Examples

Below are example usage scenarios for this file:

```python
from src.prompts.ai_assembly_system_message import AI_ASSEMBLY_SYSTEM_MESSAGE

def assemble_document(sections, document_name, llm_client):
    # Format the system message with a specific document name
    system_prompt = AI_ASSEMBLY_SYSTEM_MESSAGE.format(document_name=document_name)
    
    # Prepare the user message with the section contents
    user_message = "\n\n".join(sections)
    
    # Send the prompt and content to the language model
    result = llm_client.chat([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ])
    return result["choices"][0]["message"]["content"]
```

**Example prompt sent to an LLM:**
```
You are assembling a Research Report document from individual sections.

Your task is to:
1. Create a coherent document title and introduction
2. Ensure smooth transitions between sections
3. Add any necessary connecting text
4. Maintain consistency in tone and style
5. Add a conclusion if appropriate

The document should read as a unified whole, not just concatenated sections.
```

## Summary

The `ai_assembly_system_message.py` file provides a reusable, clearly-defined system message for instructing AI models on best practices for compiling a multi-part document. By centralizing this prompt, the project ensures consistency and makes it easy to update instructions project-wide.

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: c6a768940b1be6ef01ee2659d6c18c8329a0660c94b8121c3b2e88d2ffbddaec
relative_path: src/prompts/ai_assembly_system_message.py
generation_date: 2025-06-30T00:10:33.610394
```
<!-- END GENERATION METADATA -->
