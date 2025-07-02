<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for src\prompts\generate_file_documentation_system_message.py

# File Documentation: `src/prompts/generate_file_documentation_system_message.py`

## 1. Purpose

This file defines a formatted system message template, `GENERATED_FILE_DOCUMENTATION_SYSTEM_MESSAGE`, intended for use in automated or AI-driven documentation generation workflows. The template guides a documentation agent (e.g., an LLM) to systematically document a Python code file based on supplied context and file-specific information.

## 2. Functionality

The main purpose of this file is to provide a reusable multi-line string (Python triple-quoted string) that acts as a prompt or instruction set. This prompt is likely used to standardize documentation output across files in a codebase.

The `GENERATED_FILE_DOCUMENTATION_SYSTEM_MESSAGE` string is designed to be dynamically formatted with relevant project context, file extension, and relative file path. Its structure includes instructions to:
- Parse project documentation context
- Generate sections such as Purpose, Functionality, Key Components, Dependencies, and Usage Examples
- Output the result in clean Markdown
- Specify file metadata (extension and path)

## 3. Key Components

- **`GENERATED_FILE_DOCUMENTATION_SYSTEM_MESSAGE`**  
  A multi-line (triple-quoted) string template containing placeholders:
  - `{context}`: for existing project documentation or contextual information
  - `{current_file_extension}`: for the file extension to be documented
  - `{current_file_relative_path}`: for the relative path of the file to be documented

  Example placeholder usage:
  ```python
  formatted_message = GENERATED_FILE_DOCUMENTATION_SYSTEM_MESSAGE.format(
      context=project_docs, 
      current_file_extension='.py', 
      current_file_relative_path='src/utils/some_file.py'
  )
  ```

## 4. Dependencies

- **What this file depends on:**  
  - Python standard formatting capabilities (`str.format`)
  - It is typically invoked by a larger documentation generation or prompt orchestration system that provides required values for formatting.

- **What depends on this file:**  
  - Any system or module responsible for generating documentation prompts for code files—especially where LLMs are task-driven by system prompts (e.g., an AI documentation bot).

## 5. Usage Examples

### Example 1: Formatting the Prompt for a Specific File

```python
from src.prompts.generate_file_documentation_system_message import GENERATED_FILE_DOCUMENTATION_SYSTEM_MESSAGE

# Context and file metadata
existing_docs = "No existing documentation available."
file_ext = "py"
relative_path = "src/utils/helpers.py"

# Format the template for use
system_message = GENERATED_FILE_DOCUMENTATION_SYSTEM_MESSAGE.format(
    context=existing_docs,
    current_file_extension=file_ext,
    current_file_relative_path=relative_path,
)

# The system_message can now be fed to an LLM as a system prompt
```

### Example 2: Using within a Documentation Pipeline

```python
def generate_documentation(file_path, context):
    from src.prompts.generate_file_documentation_system_message import GENERATED_FILE_DOCUMENTATION_SYSTEM_MESSAGE
    
    file_ext = file_path.split('.')[-1]
    system_prompt = GENERATED_FILE_DOCUMENTATION_SYSTEM_MESSAGE.format(
        context=context,
        current_file_extension=file_ext,
        current_file_relative_path=file_path
    )
    # Send system_prompt and code context to an LLM-based doc generator

# Example invocation
generate_documentation('src/api/data_api.py', "Project is a RESTful data API.")
```

---

**Summary**:  
This file centralizes the definition of a documentation generation system message template, promoting consistency and reusability in automated code documentation workflows.

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: 1382296ba5634db83b43c0773a79a0bfd131d284a5e610c6f1dcda3b0c07e8d9
relative_path: src\prompts\generate_file_documentation_system_message.py
generation_date: 2025-07-01T22:18:47.795874
```
<!-- END GENERATION METADATA -->
