<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for src\prompts\section_prompt_system_message.py

# File: src/prompts/section_prompt_system_message.py

## Purpose

This file defines a system prompt template for generating technical documentation sections within a design document. The prompt is designed to guide an AI-driven documentation generator, instructing it on how to gather information and organize content for specific sections of technical documentation based on available project files and context.

## Functionality

The primary functionality of this file is to provide the `SECTION_PROMPT_SYSTEM_MESSAGE` string—a detailed, multi-line prompt. This prompt is intended for use with AI language models (such as GPT-4 or similar) that are capable of generating technical documentation. 

The prompt achieves the following:
- Clearly states the role of the AI (as a documentation generator).
- Provides context by referencing the document and section names, previous context, and section-specific instructions.
- Enumerates available file reading and project exploration tools for the AI to use in understanding the codebase.
- Emphasizes the importance of utilizing these tools to build comprehensive and accurate documentation content.

## Key Components

### Variables

- **SECTION_PROMPT_SYSTEM_MESSAGE** (`str`):  
  A format string that is parameterized with placeholders for dynamic content:
    - `{document_name}`: The name of the document being generated.
    - `{section_name}`: The specific section to generate within the document.
    - `{context}`: Existing documentation context or previously generated sections.
    - `{section_template}`: Section-specific instructions or templates to guide content creation.

  The message also:
    - Lists available functions (tools) for exploring the codebase:
        - `read_file_content(file_path)`
        - `list_files_in_directory(directory_path, extensions="", recursive="true")`
        - `find_files_by_pattern(pattern, directory="")`
        - `get_file_info(file_path)`
    - Instructs the AI to:
        - Explore the repository structure.
        - Read key files.
        - Strategically apply these tools.
        - Generate well-structured and comprehensive documentation for the given section.

## Dependencies

### Depends On

This file is standalone in terms of code, defining only a static string. However, effective use of this prompt assumes:
- An external system capable of:
    - Formatting the string with the appropriate context, document name, etc.
    - Passing the prompt to an AI language model for completion.
    - Providing the aforementioned file exploration tools for the AI model to use.

### Depended On By

Other modules or scripts within the repository responsible for:
- Technical documentation generation via AI.
- Construction of prompts for LLMs.
- Workflow orchestration for documentation creation.

## Usage Examples

Below are typical examples of how this prompt might be used in an AI-assisted documentation system:

```python
from src.prompts.section_prompt_system_message import SECTION_PROMPT_SYSTEM_MESSAGE

# Example context to fill the template
formatted_prompt = SECTION_PROMPT_SYSTEM_MESSAGE.format(
    document_name="API Design Document",
    section_name="Authentication System",
    context="Previous sections: Introduction, Architecture Overview",
    section_template="- Describe the authentication flow.\n- List used libraries and security considerations.\n- Provide example code snippets."
)

# Sending the prompt to an LLM-powered documentation generator
generated_section = llm_client.generate(
    prompt=formatted_prompt,
    tools=file_tools  # Providing file reading/listing tools to the LLM agent
)

print(generated_section)
```

**Typical Workflow**:
1. The system fills in the prompt template with relevant context, document, and section data.
2. The formatted prompt is fed to an AI model, along with access to file reading/listing tools.
3. The AI agent uses the prompt and the available tools to investigate the codebase and generate documentation for the specified section.

---

**Note:**  
This file is typically not executed directly but imported and used as part of a larger documentation automation pipeline. It modularizes the system prompt for reuse, consistency, and clarity within the codebase.

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: b271ac2401e94a1d5c37ecce534dedefdd19619f531c7513bdc885ec8cc7848d
relative_path: src\prompts\section_prompt_system_message.py
generation_date: 2025-07-01T22:19:27.034744
```
<!-- END GENERATION METADATA -->
