<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for src/prompts/mcp_file_relevance_prompt.py

# mcp_file_relevance_prompt.py

## Purpose

This file provides system prompt templates for large language model (LLM) interactions within the MCP (Modular Code Platform) project. These prompts are specifically crafted to guide LLM agents in three essential tasks:

1. Analyzing documentation to determine which source code files are relevant to user queries.
2. Identifying documentation files where certain features are described.
3. Synthesizing information from multiple documentation files to deliver comprehensive, actionable answers.

These system prompts facilitate automated, context-aware analysis and response generation, supporting code understanding, documentation navigation, and feature discovery.

---

## Functionality

This module contains three multi-line string constants, each representing a detailed system prompt instructing an LLM how to behave for a specific task. The prompts are designed to enforce strict output formatting and clear guidelines, so that downstream processes can reliably parse the LLM's output.

### 1. `MCP_FILE_RELEVANCE_SYSTEM_PROMPT`

- **Role**: Guides the LLM to identify and rank source code files relevant to a user query, based on analysis of provided documentation.
- **Responsibilities**:
  - Only include actual source code files (.py, .js, .ts, etc.), excluding documentation and markdown/text files.
  - Produce output strictly in a specified JSON schema, listing relevant files, brief summaries, relevance scores, and reasoning with a total file count.
  - Explain relevance scoring and clarify distinctions between code and documentation files.

### 2. `MCP_FEATURE_DISCOVERY_SYSTEM_PROMPT`

- **Role**: Instructs the LLM to identify documentation files (not source code) that describe a user-specified feature.
- **Responsibilities**:
  - Focus solely on documentation files output by generators, typically within `documentation_output/`.
  - Enforce exclusion of source code files and non-generated docs.
  - Output a strictly structured JSON response listing relevant documentation files and the discovery rationale.

### 3. `MCP_FEATURE_SYNTHESIS_SYSTEM_PROMPT`

- **Role**: Directs the LLM to generate a synthesized, coherent technical explanation for a specific feature, grounded in the contents of multiple documentation files.
- **Responsibilities**:
  - Structure the answer with clear sections: feature description, comprehensive answer, key components, implementation details, usage examples, related concepts, and source files.
  - Aggregate and organize disparate documentation snippets into a cohesive, actionable narrative in a prescribed JSON format.

---

## Key Components

- **Prompt Strings**:  
  - `MCP_FILE_RELEVANCE_SYSTEM_PROMPT`
  - `MCP_FEATURE_DISCOVERY_SYSTEM_PROMPT`
  - `MCP_FEATURE_SYNTHESIS_SYSTEM_PROMPT`

  Each is a detailed instruction set for relevant LLM-driven analysis or synthesis.

There are no classes or functions; the sole contents of this module are string templates for prompt engineering.

---

## Dependencies

### Imports

- None. This file is self-contained and purely data-driven.

### Used By

- Modules or code that interface with language models for:
  - Code file relevance analysis.
  - Documentation feature discovery.
  - Feature synthesis across documentation.
- Typically, these constants would be imported and passed to LLM APIs (like OpenAI, Azure OpenAI, or open-source LLM wrappers) as the initial “system” message or prompt context.

---

## Usage Examples

Here is how typical code may utilize these prompt constants:

```python
from src.prompts.mcp_file_relevance_prompt import (
    MCP_FILE_RELEVANCE_SYSTEM_PROMPT,
    MCP_FEATURE_DISCOVERY_SYSTEM_PROMPT,
    MCP_FEATURE_SYNTHESIS_SYSTEM_PROMPT,
)
import openai

# Example 1: File Relevance Analysis
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": MCP_FILE_RELEVANCE_SYSTEM_PROMPT},
        {"role": "user", "content": "I need to find all files related to user authentication in the app."},
        {"role": "assistant", "content": "Documentation guide text here..."}
    ]
)

# Example 2: Feature Documentation Discovery
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": MCP_FEATURE_DISCOVERY_SYSTEM_PROMPT},
        {"role": "user", "content": "Where is the user login flow described?"}
    ]
)

# Example 3: Feature Synthesis
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": MCP_FEATURE_SYNTHESIS_SYSTEM_PROMPT},
        {"role": "user", "content": "Explain password reset functionality."},
        {"role": "assistant", "content": "Documentation file contents here..."}
    ]
)
```

---

## Summary

- **This file**: Provides reusable, detailed LLM system prompts to reliably structure code and documentation analysis tasks.
- **Consumers**: Any module invoking LLMs for codebase understanding, search, or documentation synthesis.
- **Advice**: Use these constants as the `system` prompt when starting an LLM-based workflow in code discovery or documentation analysis tools.

---

**File location**: `src/prompts/mcp_file_relevance_prompt.py`

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: 0c6f7e4951a7e36fbeab9f4387e2e6716fb8e568fe5e449820c6d9e5f2c723e4
relative_path: src/prompts/mcp_file_relevance_prompt.py
generation_date: 2025-06-30T00:11:24.123807
```
<!-- END GENERATION METADATA -->
