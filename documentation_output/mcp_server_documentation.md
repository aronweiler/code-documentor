<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for mcp_server.py

# mcp_server.py

## Purpose

This file implements the **MCP Server** specialized for repository documentation interaction. It acts as a backend service that exposes tools to analyze and understand code repositories based on their documentation. The server allows downstream tools or user interfaces to:

- Search for source files relevant to a natural language description.
- Provide a comprehensive documentation overview of specific project features.

It primarily operates in developer and code review environments where understanding, analysis, and documentation of complex repositories are required.

---

## Functionality

The key function of this file is to define, configure, and launch a documentation-aware MCP (Multi-Component Processing) server using the `mcp` framework. The server exposes two primary tools:

1. **get_relevant_files**:  
   Given a human-readable description, returns relevant source code files, with reasoning and relevance scores.

2. **understand_feature**:  
   Given a feature description, analyzes documentation to synthesize a comprehensive explanation, implementation details, usage, and related concepts.

### Key Functional Steps

- **Initialization**  
  - Determines repository path (from CLI, environment variable, or defaults to CWD).
  - Sets up debug logging for troubleshooting and traceability.
  - Instantiates an `MCPManager` (which is responsible for actual file and feature analysis).

- **Tool Registration**  
  - Defines tool schemas via `@server.list_tools()`.  
  - Handles tool invocations via `@server.call_tool()`, with routing logic for each supported tool.

- **Request Handling**
  - For each tool call, extracts necessary parameters, delegates work to `MCPManager`, formats the response as JSON, and returns it.

- **Server Execution**
  - Launches the standard I/O MCP server.
  - Responds to requests using the configured server and registered handlers.

---

## Key Components

### Classes

- **DocumentationMCPServer**
  - Central server wrapper holding repository context, server instance, and `MCPManager`.
  - Methods:
    - `get_server()`: Returns the underlying MCP `Server` instance for further configuration or execution.

### Functions

- **main()** *(async)*
  - Entry point.
  - Parses configuration, instantiates server, registers tools, and runs server loop.

- **handle_list_tools()** *(@server.list_tools)*
  - Returns available tool schemas, including their expected input structure.

- **handle_tool_call(name: str, arguments: dict)** *(@server.call_tool)*
  - Handles incoming tool requests.
  - Delegates calls to either `get_relevant_files` or `understand_feature`, leveraging `MCPManager`.

### Tool Definitions

- Tool: `get_relevant_files`
  - Input: `{ description: string }`
  - Output includes file paths, summaries, relevance scores, and reasoning.
- Tool: `understand_feature`
  - Input: `{ feature_description: string }`
  - Output includes an explanation, implementation details, examples, related concepts, and source docs.

### Debug Logging

- All major actions and exceptions are logged to `/tmp/mcp_debug.log` for diagnostics.

---

## Dependencies

### Imports

- **mcp.server, mcp.types, mcp.server.models**  
  Core MCP protocol and server support.

- **src.mcp_manager.MCPManager**
  Custom project logic for analyzing repository files and documentation. *This is a critical dependency for repository-specific intelligence.*

- **Pydantic, Standard Library Imports**
  Used for type validation and basic IO/OS operations.

### What Depends on This File

- Any process that wants to deploy a documentation-aware MCP server as a back-end service, typically invoked via CLI or as a subprocess in an IDE or intelligent code analysis tool.

---

## Usage Examples

### As a Standalone Server

```bash
python mcp_server.py /path/to/repo
```
or (with default to current directory):

```bash
python mcp_server.py
```
or (with environment variable):

```bash
DOCUMENTATION_REPO_PATH=/path/to/repo python mcp_server.py
```

### As an MCP Tool Provider

The server is intended for use by MCP protocol clients. They will:

1. **Ask for available tools**

    ```json
    { "jsonrpc": "2.0", "method": "MCP.listTools", "params": null, "id": 1 }
    ```

2. **Invoke a Tool, e.g., `get_relevant_files`**

    ```json
    {
      "jsonrpc": "2.0",
      "method": "MCP.callTool",
      "params": {
        "name": "get_relevant_files",
        "arguments": { "description": "code that handles authentication" }
      },
      "id": 2
    }
    ```

3. **Parse the textual JSON response for results.**

---

## Example Tool Usage (Pseudo-Python)

```python
import asyncio
from mcp.types import Tool

# Assume we have a running server process...

async def get_files(server_client, description):
    response = await server_client.call_tool(
        name="get_relevant_files",
        arguments={"description": description}
    )
    # returns JSON-encoded string in response[0].text

asyncio.run(get_files(server_client, "files that process image uploads"))
```

---

## Notes

- The logic for actual code and documentation analysis is delegated to `MCPManager`, which must be implemented in `src/mcp_manager.py`.
- Debug logging is verbose and always written to `/tmp/mcp_debug.log`.
- This file is designed to be invoked directly (`if __name__ == "__main__":`) and run its event loop.

---

## See Also

- [`src/mcp_manager.py`](src/mcp_manager.py): Implementation of repository analysis logic used by this server.
- [MCP Protocol Documentation](https://github.com/mcp-protocol/spec): Underlying protocol standard implemented here.

---

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: cf058927afa1ed3fa24bc8ee42eca7b656ab84df23152871e3d3025e4e017ced
relative_path: mcp_server.py
generation_date: 2025-07-01T22:12:53.795200
```
<!-- END GENERATION METADATA -->
