<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for src\mcp_manager.py

# MCP Manager (`mcp_manager.py`)

## Purpose

The `mcp_manager.py` file defines the `MCPManager` class, which orchestrates the Model Context Protocol (MCP) operations – such as file relevance analysis and feature understanding – using LangGraph workflows and LLM-driven (language model) reasoning. It acts as a controller for intelligent code and documentation exploration, providing high-level APIs for downstream usage in tools or automation.

## Functionality

`MCPManager` is a workflow engine and service layer, which:

- Loads configuration and LLM backends.
- Encapsulates two main LangGraph workflows:
  - **Relevant Files Workflow**: Finds which source files are relevant to a user query.
  - **Feature Understanding Workflow**: Synthesizes a feature answer by discovering and reading relevant documentation files.
- Handles LLM prompt construction, output validation (with retries/correction), and output modeling.
- Provides async methods suitable for use in other services: `find_relevant_files()` and `understand_feature()`.

### Main Functions and Classes

#### `MCPManager`

- **`__init__`**: Loads configuration and initializes LLM.
- **`create_relevant_files_workflow()`**: Constructs a LangGraph workflow for file relevance analysis.
- **`create_feature_understanding_workflow()`**: Defines a LangGraph workflow for feature synthesis using documentation files.
- **Node Functions**:
  - `load_documentation_node`: Loads the documentation guide.
  - `analyze_file_relevance_node`: Calls the LLM to analyze file relevance.
  - `format_relevant_files_results_node`: Formats the LLM's response into an output model.
  - `discover_documentation_files_node`: Uses LLM to determine which docs might aid feature understanding.
  - `load_documentation_file_node`: Loads documentation files one-by-one.
  - `should_load_more_files`: Decides whether to load more docs or start synthesis.
  - `synthesize_feature_understanding_node`: Synthesizes feature info from loaded docs using the LLM.
  - `format_feature_results_node`: Formats and finalizes feature understanding output.
- **User-facing Async Methods**:
  - `find_relevant_files(description, repo_path, max_results)`: Returns ranked, relevant code files for a query.
  - `understand_feature(feature_description, repo_path)`: Synthesizes a human-friendly answer about a feature.

#### Data Models

Uses classes imported from `.mcp_models`:
- `MCPState`
- `MCPRelevantFilesResponse`
- `MCPFileResult`
- `MCPFeatureResponse`
- `MCPDocumentationFile`

All serve as structured containers for state and returned results.

## Key Components

- **Workflows (LangGraph/StateGraph)**:
  - `create_relevant_files_workflow`
  - `create_feature_understanding_workflow`
- **Nodes**:
  - Represented as Python functions, each performing part of the workflow (load file, LLM call, format, etc).
- **LLMManager Integration**:
  - The LLMManager provides model invocation (`self.llm.invoke()`), config-driven.
- **Config Management**:
  - `ConfigManager` reads YAML config files.
- **Extensive Debug Logging**:
  - Writes trace data to `/tmp/mcp_debug.log` for troubleshooting.

## Dependencies

- **Internal**:
  - `.config.ConfigManager`: Loads config file and makes it accessible to the manager.
  - `.llm_manager.LLMManager`: Sets up and manages the LLM used for prompts and completions.
  - `.mcp_models`: Defines workflow data carriers and result models.
  - LangGraph (`langgraph.graph.StateGraph`) for the workflow engine.
  - LangChain core messages (`SystemMessage`, `HumanMessage`) for constructing LLM prompts/messages.
  - Prompt templates (`.prompts.mcp_file_relevance_prompt.*`).
- **Standard Library**: `json`, `logging`, `time`, `pathlib.Path`, `typing`.
- **External Libraries**:
  - [LangChain](https://python.langchain.com/)
  - [LangGraph](https://github.com/langchain-ai/langgraph)

Other application files likely use `MCPManager` for intelligent code reasoning tasks.

## Usage Examples

### 1. Finding Relevant Files for a Query

```python
from pathlib import Path
from src.mcp_manager import MCPManager

async def example_file_relevance():
    mcp = MCPManager("config.yaml")
    repo_path = Path("/path/to/repo")
    user_query = "How does the authentication system work?"
    result = await mcp.find_relevant_files(user_query, repo_path, max_results=5)
    print(result)  # MCPRelevantFilesResponse: list of ranked relevant files + summaries
```

### 2. Understanding a Feature from Documentation

```python
from pathlib import Path
from src.mcp_manager import MCPManager

async def example_feature_understanding():
    mcp = MCPManager("config.yaml")
    repo_path = Path("/path/to/repo")
    feature_description = "user login flow"
    answer = await mcp.understand_feature(feature_description, repo_path)
    print(answer.comprehensive_answer)
    print(answer.source_documentation_files)
```

### 3. Adding Logging

By default, debug logs are written to `/tmp/mcp_debug.log`. To set up application-level logging:

```python
import logging
logging.basicConfig(level=logging.INFO)
```

## File Structure and Flow

1. Instantiation loads config and LLM.
2. To use, call one of its async methods (`find_relevant_files`, `understand_feature`), passing a query and repo path.
3. Internally, this launches a graph-based (LangGraph) workflow with multiple specialized nodes, each advancing state ("loading docs", "LLM call", "formatting", etc.).
4. LLM calls are wrapped in validation and retry logic to ensure robust outputs.

## Summary

`mcp_manager.py` provides the main high-level API and workflow logic for MCP reasoning scenarios, abstracting code exploration and documentation understanding as "relevant files" or feature explanation tasks. It leverages LangChain+LangGraph for workflow control, LLMs for intelligent reasoning, and supports robust error/detour handling for production use.

**See also**: `.mcp_models`, `.llm_manager`, `.config`, and prompt files for full extensibility and integration points.

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: 62728ddceffd1e9361b534cbac83dc593253259c88f6ee2d1db9c7dd93d3bdf0
relative_path: src\mcp_manager.py
generation_date: 2025-07-01T22:15:59.458972
```
<!-- END GENERATION METADATA -->
