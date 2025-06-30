<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for mcp_server.py

# mcp_server.py

## Purpose

This file implements the **Documentation MCP Server**, an MCP (Machine Communication Protocol) server designed to provide intelligent interaction with repository documentation. It enables advanced tooling for searching, retrieving, and understanding codebase documentation—primarily for use in documentation assistants, developer tools, or code analysis pipelines.

The primary goals are:

- **Enabling tools** to query for relevant files based on natural language descriptions.
- **Supporting feature comprehension** by producing documentation summaries for specific features.
- **Integrating with MCP-compliant clients** via a standardized stdio server.

---

## Functionality

The server provides two main tools (endpoints) usable by client interfaces:

1. **get_relevant_files**:  
   Finds files within the repository that are most relevant to a provided natural language description (e.g., "files related to database migrations").

2. **understand_feature**:  
   Provides a structured, comprehensive summary and understanding of a feature, including key components, implementation details, usage examples, and documentation sources, based on a feature description.

The server is started typically as a command-line script. It logs debug information to `/tmp/mcp_debug.log`.

### Main Steps:

- Parses configuration (repo path) from arguments or environment.
- Initializes the MCP server and tools.
- Handles incoming tool requests, routes them to the MCPManager business logic, and formats responses as structured JSON for downstream clients.
- Runs as a stdio-based async server for MCP.

---

## Key Components

### 1. Classes

#### `DocumentationMCPServer`
- **Purpose**: Sets up the server, links it to a repository, and manages access to `MCPManager`, which contains the core analysis and documentation retrieval logic.
- **Members**:
  - `repo_path` (`Path`): Path to the root of the documentation repository.
  - `server` (`mcp.server.Server`): The MCP stdio server instance.
  - `mcp_manager` (`MCPManager`): Logic handler for search/documentation features.

#### `MCPManager` *(from `src.mcp_manager`)*  
Handles actual business logic for:
- Finding relevant files (`find_relevant_files`)
- Understanding specific features (`understand_feature`)
*(Interface only referenced in this file; details assumed in `src/mcp_manager.py`)*

### 2. Functions

#### `main()`
- Bootstraps the server, sets up the repository path, registers tools, and starts the stdio server.

#### Tool Handlers
- `handle_list_tools`: Returns metadata about the available tools/endpoints.
- `handle_tool_call`: Central tool dispatcher which:
  - For `get_relevant_files`: delegates to `MCPManager.find_relevant_files(...)`
  - For `understand_feature`: delegates to `MCPManager.understand_feature(...)`
  - For other names: returns an error response.

### 3. Tool Schemas

#### `get_relevant_files`
- **Input Schema**: Requires a `description` (str) field, containing natural language query.

#### `understand_feature`
- **Input Schema**: Requires a `feature_description` (str) field describing the feature of interest.

### 4. Logging
- Writes extensive debug/log output to `/tmp/mcp_debug.log`.

---

## Dependencies

- **Standard libraries**:
  - `asyncio`, `json`, `os`, `sys`, `pathlib`, `typing`
- **Third-party libraries** (or project modules):
  - `mcp.server.stdio`, `mcp.types`, `mcp.server`, `mcp.server.models`
  - `pydantic.AnyUrl`
  - **Local project**: `src.mcp_manager.MCPManager`

### What depends on this file?

- Any process that launches the documentation MCP server (e.g., a code documentation assistant, dev environment, or integration test).

---

## Usage Examples

### Running the server

```bash
python mcp_server.py /path/to/your/repo
```
or set via environment variable:
```bash
export DOCUMENTATION_REPO_PATH=/path/to/your/repo
python mcp_server.py
```

### As a MCP Client

Send a tool invocation matching the registered schemas, for example:

#### 1. Find relevant files

```json
{
  "tool": "get_relevant_files",
  "arguments": {
    "description": "files handling OAuth login"
  }
}
```

**Response Example:**
```json
{
  "query_description": "files handling OAuth login",
  "relevant_files": [
    {
      "file_path": "auth/oauth_backend.py",
      "summary": "Handles OAuth callbacks.",
      "relevance_score": 0.95,
      "reasoning": "File imports OAuth client and manages login flows."
    }
    // ...
  ],
  "total_files_analyzed": 240,
  "processing_time_seconds": 2.1
}
```

#### 2. Understand a feature

```json
{
  "tool": "understand_feature",
  "arguments": {
    "feature_description": "user registration system"
  }
}
```

**Response Example:**
```json
{
  "feature_description": "user registration system",
  "comprehensive_answer": "The user registration system handles ...",
  "key_components": [
    "auth/routes/signup.py", "auth/models/user.py"
  ],
  "implementation_details": "Implements email confirmation, stores user in database ...",
  "usage_examples": [
    "POST /api/register with payload { ... }"
  ],
  "related_concepts": [
    "authentication", "email service"
  ],
  "source_documentation_files": [
    "docs/authentication.md"
  ]
}
```

### Extending Functionality

You may add new tools by:
- Adding definitions to the `handle_list_tools` handler.
- Extending dispatching in `handle_tool_call`.

---

## Summary

**mcp_server.py** is a flexible, stdio-based server for advanced documentation interaction and repository analysis. It provides a plug-and-play interface for developer tools requiring sophisticated codebase query and documentation understanding capabilities. Tooling is easily extensible, and all business logic routing is delegated to the pluggable `MCPManager` class.

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: a5b95495382459789c2ed10654d9d08a22dbf5dfc94ca306676c870880571244
relative_path: mcp_server.py
generation_date: 2025-06-30T00:03:27.800471
```
<!-- END GENERATION METADATA -->
