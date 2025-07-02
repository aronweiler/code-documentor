<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for src\prompts\mcp_file_relevance_prompt.py

# `mcp_file_relevance_prompt.py`

## Purpose

This file provides a set of **system prompts** designed for use with Large Language Models (LLMs) in the context of automated documentation analysis and codebase exploration. The prompts guide the language model to perform specialized tasks, such as:

- Identifying the most relevant source code files in a codebase based on user queries.
- Discovering documentation files pertinent to specific features.
- Synthesizing comprehensive feature explanations from multiple documentation sources.

These prompts are intended for integration into LLM-powered developer tools, documentation assistants, or code analysis systems to deliver structured, context-aware responses.

---

## Functionality

The file defines **three main system prompt templates** as string constants:

### 1. `MCP_FILE_RELEVANCE_SYSTEM_PROMPT`

Instructs the LLM to:

- Analyze a documentation guide and a user query.
- Identify source code files that are most relevant to the described functionality.
- **Output:** Strictly a JSON object with fields for relevant file paths, summaries, scoring, and reasoning.

**Key Constraints:**
- Only source code files should be selected (e.g., .py, .js, .cpp).
- Documentation files should be excluded.
- File paths must be relative to the repository root.
- Includes guidelines for relevance scoring and example outputs for clarity.

---

### 2. `MCP_FEATURE_DISCOVERY_SYSTEM_PROMPT`

Instructs the LLM to:

- Analyze documentation guides to find documentation files related to a user's feature request.
- **Output:** A JSON object listing relevant documentation file paths (`.md`), reasoning for their inclusion, and the original feature description.

**Key Constraints:**
- Only documentation files (`_documentation.md` within `documentation_output/`) should be returned.
- Excludes code files and incorrectly formatted documentation paths.
- Provides both correct and incorrect examples of valid documentation paths.

---

### 3. `MCP_FEATURE_SYNTHESIS_SYSTEM_PROMPT`

Instructs the LLM to:

- Synthesize a comprehensive, practical, and structured answer about a feature by integrating multiple documentation sources and the user’s query.
- **Output:** A JSON object with fields for the synthesized answer, key components, implementation details, usage examples, related concepts, and source documentation files.

**Key Constraints:**
- Output must be organized, actionable, complete, and developer-oriented.
- Fields are explicitly detailed to ensure output consistency.

---

## Key Components

| Name                                    | Type    | Description                                                                                         |
|------------------------------------------|---------|-----------------------------------------------------------------------------------------------------|
| `MCP_FILE_RELEVANCE_SYSTEM_PROMPT`       | `str`   | Prompt template for discovering relevant source code files in response to a query.                   |
| `MCP_FEATURE_DISCOVERY_SYSTEM_PROMPT`    | `str`   | Prompt template for finding documentation files related to a user-described feature.                 |
| `MCP_FEATURE_SYNTHESIS_SYSTEM_PROMPT`    | `str`   | Prompt template for synthesizing feature overviews from multiple documentation files.                |


---

## Dependencies

### Internal

- **None:** This file only defines string constants and does not import or depend on any other modules within the project.

### External

- **Consumers:** These prompts are meant to be injected into LLM requests by other components—typically in code analysis tools, documentation generation pipelines, or conversational AI interfaces.

---

## Usage Examples

Here are typical patterns for how this file would be used:

### 1. Selecting the appropriate prompt for an LLM request

```python
from src.prompts.mcp_file_relevance_prompt import (
    MCP_FILE_RELEVANCE_SYSTEM_PROMPT,
    MCP_FEATURE_DISCOVERY_SYSTEM_PROMPT,
    MCP_FEATURE_SYNTHESIS_SYSTEM_PROMPT,
)

# Example: Gathering which prompt to use based on user intention
if user_action == "find_code_files":
    prompt = MCP_FILE_RELEVANCE_SYSTEM_PROMPT
elif user_action == "find_doc_files":
    prompt = MCP_FEATURE_DISCOVERY_SYSTEM_PROMPT
elif user_action == "synthesize_feature":
    prompt = MCP_FEATURE_SYNTHESIS_SYSTEM_PROMPT

llm_response = llm_api.query(
    system_prompt=prompt,
    user_input=input_data
)
```

### 2. Integrating with an LLM pipeline

```python
from src.prompts import mcp_file_relevance_prompt

def get_relevant_files(doc_guide: str, user_query: str) -> dict:
    # Compose the full prompt with input substitutions
    prompt = mcp_file_relevance_prompt.MCP_FILE_RELEVANCE_SYSTEM_PROMPT.format(...)
    response = call_llm_api(system_prompt=prompt, user_input=f"{doc_guide}\n{user_query}")
    return parse_json(response)
```

### 3. Documentation assistant scenario

A documentation assistant tool may use these prompts to:

- Identify which code files a user should edit or review.
- Surface only relevant documentation during onboarding.
- Generate feature overviews by combining multiple documentation files.

---

## Summary

- **File**: `src/prompts/mcp_file_relevance_prompt.py`
- **Role**: Centralized repository of crafted prompt templates for code and documentation analysis using LLMs.
- **Use Cases**: Prompt injection for code analysis/chatbots, automated documentation tools, and developer support systems.
- **Integration**: Import these prompt constants in LLM-driven workflows for consistent, high-quality AI responses.

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: 3723755eebe59adb3e2e30f08fc6938d231fd3756f5cc847102509b10bcd7b1f
relative_path: src\prompts\mcp_file_relevance_prompt.py
generation_date: 2025-07-01T22:19:10.389866
```
<!-- END GENERATION METADATA -->
