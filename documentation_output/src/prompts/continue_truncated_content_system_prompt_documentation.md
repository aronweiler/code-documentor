<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for src/prompts/continue_truncated_content_system_prompt.py

# continue_truncated_content_system_prompt.py

## Purpose

This file defines a system prompt template intended for use with AI or automated documentation generation tools. The template is specifically designed to support the continuation of truncated documentation sections—i.e., when the documentation for a particular section of a document has been cut off and needs to be resumed and completed. 

It sets the context for the system to continue writing the documentation seamlessly, using provided context, previous content, section instructions, and suggested tools for gathering additional information.

## Functionality

### Main Functionality

- **Prompt Template Definition**: The core functionality is the definition of a multi-line string template named `CONTINUE_TRUNCATED_CONTENT_SYSTEM_PROMPT`. This template incorporates several placeholders that will be programmatically replaced with relevant values at runtime.
- **System Message for AI Tools**: The template is constructed to be used as a system prompt for Large Language Models (LLMs) or AI agents tasked with auto-generating or completing documentation.
- **Tool Instructions**: The prompt informs the system about available helper functions for reading files and directories, which the AI can use to gather extra content or clarify section requirements.

## Key Components

### Global Variables

- **`CONTINUE_TRUNCATED_CONTENT_SYSTEM_PROMPT`**:  
  - *Type*: `str` (multi-line string)
  - *Purpose*: Serves as a system prompt template for continuing documentation sections.  
  - *Placeholders*:  
    - `{document_name}`: Name of the document being completed.
    - `{section_name}`: Current section that needs to be continued.
    - `{context}`: Relevant context from the existing documentation or previous sections.
    - `{section_template}`: Original instructions or template for this section.
    - `{continuation_prompt}`: Specific task or instruction on how to continue.

*No functions or classes are defined in this file; the only item is the prompt template string.*

## Dependencies

### External Dependencies

- **None at the File Level**:  
  The file itself does not import or depend on other Python modules.

### Usage/Integration Dependencies

- **This file is intended to be imported and used by**:  
  - Documentation generation tools or scripts
  - AI systems that process and fill in documentation prompts

- **Placeholder Tools Mentioned in the Prompt for AI Systems**:  
  The prompt references the following tools which *the AI system* is expected to use:
    - `read_file_content(file_path)`
    - `list_files_in_directory(directory_path, extensions="", recursive="true")`
    - `find_files_by_pattern(pattern, directory="")`
    - `get_file_info(file_path)`
    
  These are informational for the LLM/AI that uses the prompt—they are not implemented in this file.

## Usage Examples

### Example: Filling the Prompt and Sending to an AI System

```python
from src.prompts.continue_truncated_content_system_prompt import CONTINUE_TRUNCATED_CONTENT_SYSTEM_PROMPT

prompt = CONTINUE_TRUNCATED_CONTENT_SYSTEM_PROMPT.format(
    document_name="API Reference",
    section_name="Authentication",
    context="Earlier sections described the overall API structure and error handling.",
    section_template="Describe how users authenticate with the system, including token usage.",
    continuation_prompt="The last sentence was: 'After obtaining a token, users can...'. Please continue from here."
)

# Pass `prompt` as a system message or context when calling your LLM
response = call_llm_system_api(system_prompt=prompt)
```

### Example: Integration in a Documentation Automation Script

```python
def generate_continue_prompt(doc_name, sec_name, prev_context, sec_template, cont_prompt):
    from src.prompts.continue_truncated_content_system_prompt import CONTINUE_TRUNCATED_CONTENT_SYSTEM_PROMPT
    return CONTINUE_TRUNCATED_CONTENT_SYSTEM_PROMPT.format(
        document_name=doc_name,
        section_name=sec_name,
        context=prev_context,
        section_template=sec_template,
        continuation_prompt=cont_prompt
    )
```

---

**Note:**  
- This file is purely a template provider; to be functional, it must be used in conjunction with external code that fills its format placeholders and supplies it to an AI documentation agent.
- No executable code or logic exists in this file apart from the prompt string.

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: 1e800d7677c5b13a63d17bf7c6ad891279b13c769722c54eebd014695771a503
relative_path: src/prompts/continue_truncated_content_system_prompt.py
generation_date: 2025-06-30T00:10:53.084301
```
<!-- END GENERATION METADATA -->
