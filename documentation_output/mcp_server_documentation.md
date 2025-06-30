<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for mcp_server.py

# mcp_server.py

## Purpose

This file implements an **MCP (Machine/Model Control Protocol) server** tailored for repository documentation tasks. Its primary function is to provide interactive, programmatic tools for accessing and utilizing documentation that has been generated for a code repository. It allows users (or bots/agents) to query for relevant source files based on descriptions and understand specific features through programmatic interfaces.

Typical use cases include:
- Integrating with AI agents that need guidance on a codebase.
- Interactive tools for developers to find documentation/relevant files faster.
- Automated systems that require contextual documentation for reasoning about codebases.

---

## Functionality

The core logic centers around:
- Initializing the server and loading any top-level documentation guides.
- Exposing programmatic "tools" (API-like endpoints) such as:
    - `get_relevant_files`: Find relevant files given a plain-text description.
    - `understand_feature`: Fetch and summarize documentation about a specific feature.
- Serving and listing these tools for client use.
- (Future Scope) Placeholder implementations that can be augmented with advanced document and code search/synthesis, e.g., via LLMs or semantic search.

### Main Classes and Functions

#### `DocumentationMCPServer`

- **Purpose**: Encapsulates the server setup, documentation loading, and tool registration.
- **Init Parameters**:
    - `repo_path`: The path to the repository root (default: current working directory).
- **Key Methods**:
    - `_load_documentation_guide()`: Loads `documentation_guide.md` from the generated documentation output, if present.
    - `_register_tools()`: Registers main tools for file finding and feature understanding.
    - `_find_relevant_files(description)`: (Placeholder) Returns mock list of file paths matching some description.
    - `_understand_feature(feature_description)`: (Placeholder) Extracts (crudely, for now) documentation for a described feature.
    - `get_server()`: Returns the internal MCP Server instance.

#### `main()`

- **Purpose**: Entrypoint for the module/script.
- **Responsibilities**:
    - Resolves the repository path.
    - Instantiates `DocumentationMCPServer`.
    - Registers the tools and tool schemas.
    - Launches the server on standard IO streams, ready to accept MCP-formatted requests.

#### Tool Functions

- **`get_relevant_files`:**
    - Input: `{ "description": "<user query>" }`
    - Output: JSON list of (mock) relevant file paths. Intended to be implemented with semantic or LLM-based search in future.

- **`understand_feature`:**
    - Input: `{ "feature_description": "<feature/detail>" }`
    - Output: Extracted documentation text from the documentation guide, or fallback if nothing matches.

#### Additional Utilities

- Uses `pydantic` for URL/type validation; and the `mcp.types` and `mcp.server` for MCP protocol compliance.
- Outputs logs/warnings/errors to `stderr` for traceability.

---

## Key Components

- **Classes**:
    - `DocumentationMCPServer`: Central class for server and tool registration.

- **Functions / Aliased Endpoints**:
    - `get_relevant_files`
    - `understand_feature`
    - `handle_list_tools`

- **Variables**:
    - `self.documentation_guide_content`: Stores loaded documentation.
    - `self.server`: Holds the MCP server instance.

- **Tools/Endpoints Defined for Clients:**
    - `list_tools`: Lets clients discover available API/tool endpoints, with input schemas.

---

## Dependencies

### External Packages

- [`asyncio`](https://docs.python.org/3/library/asyncio.html) (built-in): For async execution.
- [`json`](https://docs.python.org/3/library/json.html) (built-in): Serialization.
- [`os`](https://docs.python.org/3/library/os.html), [`sys`](https://docs.python.org/3/library/sys.html): Filesystem and process management.
- [`pathlib`](https://docs.python.org/3/library/pathlib.html): Path manipulation.
- [`pydantic`](https://docs.pydantic.dev/): For URL parsing/validation (minimal use in this file).
- `mcp.server` and `mcp.types` (local/external dependency): Core MCP protocol implementation.
    - MCP server tools: `Server`, `NotificationOptions`, `InitializationOptions`
    - Type models: `Tool`, `TextContent`

### What Depends on This

- Any tool or process that wants to interact with the repository's documentation using MCP protocol would connect to and use this server.
- It expects that the repository contains (or is configured to generate) a `documentation_output/documentation_guide.md`.

---

## Usage Examples

### Run as a Standalone Server

```bash
python3 mcp_server.py /path/to/your/repo
```

Or via environment variable:

```bash
export DOCUMENTATION_REPO_PATH=/path/to/your/repo
python3 mcp_server.py
```

### Querying the Server (Example Conceptual Calls)

Assume you have a client that communicates with the MCP server over stdio.

#### 1. List Tools

```json
{
  "method": "list_tools",
  "params": { }
}
```

#### 2. Find Relevant Files

```json
{
  "method": "get_relevant_files",
  "params": {
    "description": "files related to user authentication"
  }
}
```
_Server replies with a list of relevant file paths (mocked for now)_

#### 3. Understand Feature

```json
{
  "method": "understand_feature",
  "params": {
    "feature_description": "AI workflow calculating drive time"
  }
}
```

### Code Example: Embedding as a Component

```python
from mcp_server import DocumentationMCPServer

repo_path = "/path/to/repo"
doc_server = DocumentationMCPServer(repo_path)
server = doc_server.get_server()
# Use 'server' as needed with MCP communication logic
```

---

## Notes

- **Tool logic is primarily placeholder** pending future implementation of advanced file/feature matching (semantic or LLM-based).
- The server expects a `documentation_guide.md` within a `documentation_output` directory at the repo root for best results.
- All MCP protocol served tools include machine-readable JSON schemas for their required input.

---

## File Structure

```plaintext
mcp_server.py
├── DocumentationMCPServer [class]
│   ├── _load_documentation_guide
│   ├── _register_tools
│   ├── _find_relevant_files
│   ├── _understand_feature
│   └── get_server
├── main [async function]
│   └── handle_list_tools [tool]
│
└── __main__ block
```
---

**End of Documentation**

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: b23efe23684b5b305486a692c5c103a7744835eb6d979939256bff72f96535f2
relative_path: mcp_server.py
generation_date: 2025-06-29T16:51:00.774473
```
<!-- END GENERATION METADATA -->
