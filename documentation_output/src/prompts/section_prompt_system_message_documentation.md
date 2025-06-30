<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for src/prompts/section_prompt_system_message.py

# File: `src/prompts/section_prompt_system_message.py`

## Purpose

This file defines a system message prompt template used by a technical documentation generation tool or assistant. The template guides an AI system to generate documentation sections for a project design document. It ensures the AI follows a structured workflow to gather information and produce accurate, comprehensive documentation for each section.

## Functionality

The main functionality of this file is the declaration of a multi-line string (`SECTION_PROMPT_SYSTEM_MESSAGE`) that serves as a prompt. This prompt is formatted for use with an AI language model or documentation generator, setting out:
- Context (project document and section names, prior content)
- Specific instructions for generating a documentation section
- A list of file exploration tools available to the system, with guidance on their use

The prompt ensures the generated documentation is rooted in a thorough understanding of the repository, using file reading and directory browsing tools as necessary.

## Key Components

### Constants

- **`SECTION_PROMPT_SYSTEM_MESSAGE`**
  - **Type:** `str`
  - **Purpose:** Serves as the system-level instruction for guiding the documentation generation process.
  - **Content:** Includes placeholders for:
    - `{document_name}`: Name of the target document
    - `{section_name}`: Name of the section to generate
    - `{context}`: Contextual information from existing documentation or prior sections
    - `{section_template}`: Detailed instructions or a template for the section
  - **Instructions:**
    - Emphasizes exploration of the codebase before writing documentation
    - Lists available helper tools (for reading files, listing directories, etc.) and instructs strategic use of these tools

## Dependencies

### Dependencies this file has:
- **None (runtime):**  
  This file contains only a prompt string and does not import any modules or reference any other parts of the codebase.

### Dependencies on this file:
- **Upstream code or infrastructure that:**
  - Invokes AI agents, documentation assistants, or LLM-driven processes.
  - Loads this prompt string during the documentation generation workflow, passing the formatted message to the AI system with the necessary variable substitutions (e.g., actual document name, section, context, template, etc.).

## Usage Examples

While this file is not directly executable, it is used programmatically as part of a larger documentation generation system. For example:

```python
from src.prompts.section_prompt_system_message import SECTION_PROMPT_SYSTEM_MESSAGE

def generate_section_prompt(document_name, section_name, context, section_template):
    prompt = SECTION_PROMPT_SYSTEM_MESSAGE.format(
        document_name=document_name,
        section_name=section_name,
        context=context,
        section_template=section_template
    )
    return prompt

# Example usage in a documentation workflow:
prompt = generate_section_prompt(
    document_name="API Reference",
    section_name="Authentication Methods",
    context="Previous section covers system overview.",
    section_template="Describe all authentication mechanisms with code examples and security notes."
)
# This prompt would then be sent to the LLM or documentation agent.
```

## Summary

- **Defines:** A system message prompt for AI documentation generation
- **Purpose:** Guides AI to create comprehensive design document sections based on repository exploration
- **Used by:** Documentation generation workflows/modules that interact with AI systems
- **Contains:** One formatted template string with placeholders and detailed instructions

This file is central to ensuring accurate and thorough technical documentation is produced by aligning the AI's process with best practices and providing explicit tools for repository analysis.

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: b271ac2401e94a1d5c37ecce534dedefdd19619f531c7513bdc885ec8cc7848d
relative_path: src/prompts/section_prompt_system_message.py
generation_date: 2025-06-30T00:11:42.536699
```
<!-- END GENERATION METADATA -->
