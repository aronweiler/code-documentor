<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for src\prompts\continue_truncated_content_system_prompt.py

# File: `src/prompts/continue_truncated_content_system_prompt.py`

## Purpose

This file defines a system prompt template, `CONTINUE_TRUNCATED_CONTENT_SYSTEM_PROMPT`, intended for use in automated documentation generation or augmentation systems. Its purpose is to provide a consistent and context-rich prompt when a section of documentation has previously been truncated and needs to be continued and completed by an AI, typically in an LLM-based workflow.

## Functionality

The primary functionality provided by this file is the definition of a multi-line string template. This template is designed to be filled in with specific variables (such as `document_name`, `section_name`, `context`, etc.), and then used to guide an AI assistant or agent in continuing the writing of a documentation section.

The prompt informs the assistant that it is continuing previously truncated content and provides it with:
- The current document and section context
- Original instructions for the section
- Access to specific file reading tools to facilitate information gathering
- The necessary cues (`continuation_prompt`) for smooth content continuation

## Key Components

### Variables

#### `CONTINUE_TRUNCATED_CONTENT_SYSTEM_PROMPT`
- **Type**: `str` (multi-line string)
- **Purpose**: Acts as a system prompt template with placeholders for runtime substitution.
- **Placeholders**:
  - `{document_name}`: Name of the documentation being worked on.
  - `{section_name}`: Name of the section being continued.
  - `{context}`: Relevant context from previous documentation.
  - `{section_template}`: Instructions describing what this section should contain.
  - `{continuation_prompt}`: Custom instructions or hint on how to resume writing the section.

### Prompt Tools Introduced

The template describes a set of file reading tools that the agent may access:
- `read_file_content(file_path)`: Read content from a given file.
- `list_files_in_directory(directory_path, extensions="", recursive="true")`: List files in a directory, optionally filtering by extension and recursion.
- `find_files_by_pattern(pattern, directory="")`: Search for files matching a specific pattern.
- `get_file_info(file_path)`: Retrieve file metadata.

These are references and not actual implementations in this file, but they are expected to be available in the environment where the prompt is used.

## Dependencies

### Imported Modules
- **None**: This file is self-contained and does not import any modules.

### External Dependencies
- **Template Variables**: The prompt relies on runtime code (elsewhere in the application) to provide the appropriate values for its placeholders.
- **Prompt Usage Environment**: Designed for use in systems that handle dynamic text substitution and execute/dispatch the prompt to an LLM-powered agent.

### Downstream Dependencies

Other code files or services in the repository may import and use `CONTINUE_TRUNCATED_CONTENT_SYSTEM_PROMPT` when they need to generate a task or prompt for resuming or completing documentation sections.

## Usage Examples

### Example: Using the Prompt in a Documentation Tool

```python
from src.prompts.continue_truncated_content_system_prompt import CONTINUE_TRUNCATED_CONTENT_SYSTEM_PROMPT

# Sample data
document_name = "API Reference"
section_name = "Authentication"
context = "Previous sections have explained the basics of user registration and login."
section_template = "Describe how to obtain and refresh authentication tokens."
continuation_prompt = "Continue describing token expiration policies, and provide code examples."

# Fill the template with specific values
system_prompt = CONTINUE_TRUNCATED_CONTENT_SYSTEM_PROMPT.format(
    document_name=document_name,
    section_name=section_name,
    context=context,
    section_template=section_template,
    continuation_prompt=continuation_prompt
)

# The resulting system_prompt can now be passed to an LLM or automation agent
print(system_prompt)
```

### Typical Use Case

1. An LLM-based documentation generator detects an incomplete or truncated section.
2. The generator collects relevant context and prepares instructions for continuing the section.
3. The generator fills in `CONTINUE_TRUNCATED_CONTENT_SYSTEM_PROMPT` with the necessary data.
4. The filled-in prompt is sent to an AI agent, which resumes or completes the writing accordingly.

---

**Note:**  
This file serves as a static resource for system prompt standardization in documentation tools. It does not execute any logic itself. To use it, import the string and format/dispatch it as needed in your application's document generation workflow.

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: 1e800d7677c5b13a63d17bf7c6ad891279b13c769722c54eebd014695771a503
relative_path: src\prompts\continue_truncated_content_system_prompt.py
generation_date: 2025-07-01T22:18:16.762910
```
<!-- END GENERATION METADATA -->
