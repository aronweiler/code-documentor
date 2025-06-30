<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for src/mcp_manager.py

# `mcp_manager.py`

## Purpose

The `mcp_manager.py` file provides a centralized manager (`MCPManager`) that orchestrates high-level Model Context Protocol (MCP) operations using LangGraph workflows and large language models (LLMs). It primarily enables two core functionalities:

1. **Finding source code files most relevant to a specific query** (via documentation analysis)
2. **Synthesizing a comprehensive understanding of a project feature** using structured documentation file analysis

This class integrates the configuration, LLM management, prompt engineering, and workflow logic required for advanced model-assisted codebase comprehension and feature tracing.

---

## Functionality

The chief functionality is encapsulated in the `MCPManager` class, which:

- Initializes configuration and LLM infrastructure.
- Constructs LangGraph workflows (via `StateGraph`) for two main operations:
  - **Relevant file discovery**: Identifying source code files matching a user query.
  - **Feature understanding**: Synthesizing a rich answer to a feature query, leveraging documentation files.
- Defines node functions for individual workflow steps such as loading documentation, invoking the LLM, formatting results, and handling errors.
- Provides public async methods for clients to execute these tasks (`find_relevant_files`, `understand_feature`).

---

## Key Components

### 1. **MCPManager**
   - **Constructor**:
     - Loads configuration (`ConfigManager`).
     - Initializes the LLM (`LLMManager`).
     - Sets up logging.

   - **Workflow Constructors**:
     - `create_relevant_files_workflow()`: Workflow to locate relevant source code files.
     - `create_feature_understanding_workflow()`: Workflow to analyze and understand a codebase feature using documentation.

   - **Workflow Node Methods**:
     - `load_documentation_node`: Loads the documentation guide that provides high-level context.
     - `analyze_file_relevance_node`: Uses the LLM to match query with code files.
     - `format_relevant_files_results_node`: Transforms LLM results into structured output.
     - `discover_documentation_files_node`: Uses the LLM to identify docs pertinent to a feature.
     - `load_documentation_file_node`: Loads and accumulates relevant doc files.
     - `should_load_more_files`: Logic for iterating through documentation files.
     - `synthesize_feature_understanding_node`: LLM synthesis across loaded documentation.
     - `format_feature_results_node`: Formats synthesis into the API response model.

   - **Public Async Methods**:
     - `find_relevant_files(description, repo_path, max_results)`: End-to-end pipeline for code file location.
     - `understand_feature(feature_description, repo_path)`: End-to-end pipeline for feature understanding.

### 2. **Workflow State and Models**
   - The workflow state is modeled via the `MCPState` dataclass.
   - Results and intermediate data use models such as:
     - `MCPRelevantFilesResponse`
     - `MCPFileResult`
     - `MCPFeatureResponse`
     - `MCPDocumentationFile`

### 3. **Prompts**
   - Imports system prompts to structure LLM calls:
     - `MCP_FILE_RELEVANCE_SYSTEM_PROMPT`
     - `MCP_FEATURE_DISCOVERY_SYSTEM_PROMPT`
     - `MCP_FEATURE_SYNTHESIS_SYSTEM_PROMPT`

---

## Dependencies

**External Dependencies**:
- [LangGraph](https://github.com/langchain-ai/langgraph): For workflow orchestration (`StateGraph`)
- [LangChain](https://python.langchain.com/): For LLM message objects (`SystemMessage`, `HumanMessage`)
- Standard library modules: `json`, `logging`, `time`, `pathlib.Path`, etc.

**Internal Project Dependencies**:
- `.config.ConfigManager`: Loads configuration files
- `.llm_manager.LLMManager`: Initializes and manages LLM interface
- `.mcp_models.*`: Dataclasses for workflow state and API/model responses
- `.prompts.mcp_file_relevance_prompt`: Prompt texts for LLM interaction

**Downstream/Who Depends on This**:
- Any user-facing API or CLI that needs contextual file searching or feature understanding via LLMs should interface with `MCPManager`.

---

## Usage Examples

> See below for basic usage patterns, suitable for FastAPI endpoints, CLI commands, or notebook interfaces.

### 1. **Find Relevant Code Files**

```python
from pathlib import Path
from src.mcp_manager import MCPManager

import asyncio

description = "Where is user authentication handled?"
repo_path = Path("/path/to/repo")
manager = MCPManager()

relevant_files_resp = asyncio.run(
    manager.find_relevant_files(description, repo_path, max_results=5)
)

# Access the results:
for file_result in relevant_files_resp.relevant_files:
    print(f"File: {file_result.file_path}")
    print(f"Summary: {file_result.summary}\n")
```

### 2. **Understand a Feature via Documentation**

```python
from pathlib import Path
from src.mcp_manager import MCPManager

import asyncio

feature_question = "How does the plugin system work?"
repo_path = Path("/path/to/repo")
manager = MCPManager()

feature_resp = asyncio.run(
    manager.understand_feature(feature_question, repo_path)
)

print("Feature Description:", feature_resp.feature_description)
print("Comprehensive Answer:", feature_resp.comprehensive_answer)
print("Key Components:", feature_resp.key_components)
print("Implementation Details:", feature_resp.implementation_details)
print("Usage Examples:", feature_resp.usage_examples)
```

---

## Design Notes

- **Workflow Pattern**: Nodes (functions) progress the state through steps; each can return new state dict fragments.
- **LLM Integration**: Centralized logic for prompt construction, LLM invocation, and (JSON) output parsing.
- **Robust Logging/Debugging**: Extensive debug logs to `/tmp/mcp_debug.log` for troubleshooting workflow progress and LLM outputs.
- **Error Handling**: Every node can gracefully record error state, allowing upstream code to detect and format error responses safely.
- **Customization**: Additional workflow/nodes could be added for new MCP tasks.

---

## Summary Table

| Class/Function Name                | Purpose/Role                                           |
|------------------------------------|--------------------------------------------------------|
| `MCPManager`                       | Main class, exposes async API for workflows            |
| `create_relevant_files_workflow()` | Relevant file discovery workflow assembly              |
| `create_feature_understanding_workflow()` | Constructs feature understanding workflow        |
| `load_documentation_node`          | Loads entrypoint "documentation guide" file            |
| `analyze_file_relevance_node`      | LLM-based file relevance analysis                      |
| `format_relevant_files_results_node` | Build structed `MCPRelevantFilesResponse`           |
| `find_relevant_files`              | Orchestrates relevant files workflow async call        |
| `discover_documentation_files_node` | LLM workflow to find feature docs                    |
| `load_documentation_file_node`      | Sequentially loads discovered documentation files    |
| `should_load_more_files`            | Workflow loop control                                  |
| `synthesize_feature_understanding_node` | Final LLM synthesis from all docs               |
| `format_feature_results_node`       | Output structuring for feature understanding         |
| `understand_feature`                | Orchestrates feature understanding workflow           |

---

## Extending

- **To add more MCP workflows**: Define new methods to assemble workflows with required nodes following the patterns above.
- **To change LLM**: Update configuration/implementation in `LLMManager` only.
- **To refine prompts/outputs**: Edit the corresponding prompt modules and model response classes.

---

**This file is central for intelligent, workflow-based project code and documentation understanding via LLMs. It should be imported and used as a service by all high-level programmatic interfaces that need advanced context-aware codebase analysis.**


---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: 9ad07dba4bdb604ed3427b85e4421d93c5734da4bc199e0b1668a71f5532f6d5
relative_path: src/mcp_manager.py
generation_date: 2025-06-30T00:08:36.882354
```
<!-- END GENERATION METADATA -->
