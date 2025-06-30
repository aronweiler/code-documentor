<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for mcp_server_http.py

# mcp_server_http.py

## Purpose

This file provides an HTTP server for interacting with a Machine Control Protocol (MCP) backend specialized for repository documentation and code navigation. It enables users or external tools to query documentation, discover relevant files in a repository, and understand code features through a web API or via stdio. The server supports both HTTP/SSE transports and a command-line stdio mode, making it flexible for integration in editors, automation, or web UIs.

---

## Functionality

At its core, `mcp_server_http.py` offers a set of MCP-based tools for:

- **Finding relevant files** in a codebase, given a natural language description.
- **Understanding features** of a codebase, providing summarized documentation for given functionalities.

It exposes these tools through:
- An HTTP/FastAPI-based API (default)
- Optionally, a stdio-based protocol for direct editor/CLI integration

It also provides metadata endpoints for tool discovery.

---

## Key Components

### Classes

#### 1. `DocumentationMCPServer`
- **Purpose**: Initializes and configures an MCP server for documentation-related tasks.
- **Initialization**:
  - Loads the project repository path (default: current directory).
  - Instantiates `MCPManager` for code/documentation queries.
  - Registers tools for:
    - `get_relevant_files` – Finds source files matching a description.
    - `understand_feature` – Summarizes and explains a feature.
- **Key Method**:
  - `get_server()`: Returns the configured MCP `Server` instance.

#### 2. `HTTPMCPWrapper`
- **Purpose**: Provides an HTTP API for the MCP tools if SSE transport is unavailable.
- **Initialization**:
  - Wraps an MCP server and publishes endpoints using FastAPI.
  - Adds CORS middleware for browser compatibility.
  - Sets up endpoints:
    - `GET /` - Info and tool listing
    - `GET /tools` - Schema and description for each tool
    - `POST /tools/{tool_name}` - Execute a tool
- **Key Method**:
  - `run()`: Starts the Uvicorn-powered HTTP server with instructive logging.

### Functions

#### 1. `main()`
- **Purpose**: Entry point for the server.
- **Actions**:
  - Parses command-line arguments (repository path, port, stdio or HTTP mode).
  - Initializes the `DocumentationMCPServer`.
  - Depending on mode:
    - **HTTP Mode**: Runs the FastAPI web server with endpoints described above.
    - **Stdio Mode**: Runs an MCP stdio server for direct process communication.

### Endpoints

| Endpoint                               | Method | Purpose                                             |
|-----------------------------------------|--------|-----------------------------------------------------|
| `/`                                    | GET    | Server info and available tools                     |
| `/tools`                               | GET    | Detailed tool listing with input schemas            |
| `/tools/get_relevant_files`            | POST   | Finds files based on a description                  |
| `/tools/understand_feature`            | POST   | Gets documentation about a feature                  |

---

## Key Modules and Variables

- **Imports**
  - `mcp.types`: MCP type annotations.
  - `mcp.server`, `mcp.server.models`: MCP server infrastructure.
  - `fastapi`, `uvicorn`, `starlette`: HTTP server stack (when not using SSE).
  - `src.mcp_manager.MCPManager`: Your main code/documentation manager logic.
- **Variables**
  - `repo_path`: Filesystem path to the code repository to analyze.
  - `HAS_SSE`: Boolean for optional SSE transport support.

---

## Dependencies

### Imports/Requirements

- **Direct Dependencies**  
  - [FastAPI](https://fastapi.tiangolo.com/)
  - [Uvicorn](https://www.uvicorn.org/)
  - [Starlette](https://www.starlette.io/) (cors middleware)
  - [mcp.* (custom MCP protocol/server implementation)](https://github.com/your-org/mcp)
  - `src.mcp_manager.MCPManager` (application-specific management logic)

- **What Depends on This File**
  - Used as a standalone server process for documentation navigation and code search workflows, integrated directly by users, editors, or CI scripts.

---

## Usage Examples

### 1. **Running as an HTTP server (default):**

```bash
python mcp_server_http.py /path/to/my/repo --port 4000
```

This will output usage and start the server. The main endpoints become available:

#### Example: Find relevant files

```bash
curl -X POST http://127.0.0.1:4000/tools/get_relevant_files \
  -H 'Content-Type: application/json' \
  -d '{"arguments": {"description": "authentication files"}}'
```

#### Example: Understand a feature

```bash
curl -X POST http://127.0.0.1:4000/tools/understand_feature \
  -H 'Content-Type: application/json' \
  -d '{"arguments": {"feature_description": "user login system"}}'
```

### 2. **Running with stdio (for editors or IDE integration):**

```bash
python mcp_server_http.py /path/to/my/repo --stdio
```

This will start the stdio transport for MCP, expected to be used by an editor integration or plugin.

---

## Additional Notes

- When the SSE server transport is installed (`mcp.server.sse`), SSE may be used for real-time communication with clients. Otherwise, the HTTP-only fallback is activated (as in the code).
- The **tools' core logic** is delegated to the `MCPManager`: you should ensure that it is implemented and accessible under `src.mcp_manager`.
- A tool registry pattern allows for easy expansion with additional tools.

---

## Example Output Structure

- **POST /tools/get_relevant_files**  
  ```json
  {
    "result": [
      "src/auth/login.py",
      "src/auth/session.py"
    ]
  }
  ```
- **POST /tools/understand_feature**  
  ```json
  {
    "result": {
      "summary": "The user login system covers authentication, session management, and password encryption...",
      ...
    }
  }
  ```

---

## Troubleshooting

- **Missing Dependencies**: Ensure `FastAPI`, `uvicorn`, `starlette`, and your custom `mcp` and `src.mcp_manager` modules are available in your Python environment.
- **CORS Issues**: CORS is enabled for all origins by default for development. Adjust as appropriate for production.

---

## Conclusion

`mcp_server_http.py` turns your repository into a documented, indexed, and queryable service, supporting both modern HTTP API access and traditional stdio-based MCP protocol flows. Its modular design makes it extendable for additional documentation, code search, and code navigation tasks.

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: 5a3028e553b5180c482b2a503f361fe9b32a64bc9028b81746cf9b66f8a5ad8c
relative_path: mcp_server_http.py
generation_date: 2025-06-30T00:04:04.536129
```
<!-- END GENERATION METADATA -->
