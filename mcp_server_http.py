#!/usr/bin/env python3
"""
HTTP MCP Server for Repository Documentation
Provides tools to interact with generated documentation and find relevant files.
Runs on HTTP with SSE (Server-Sent Events) for real-time communication.
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any, List
import argparse

import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions

# Try to import SSE server transport, fallback to custom HTTP implementation
try:
    import mcp.server.sse
    HAS_SSE = True
except ImportError:
    HAS_SSE = False

# Import HTTP dependencies for fallback
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import uvicorn
from starlette.middleware.cors import CORSMiddleware

# Import our MCP manager and models
from src.mcp_manager import MCPManager

class DocumentationMCPServer:
    """MCP Server for repository documentation interaction."""
    
    def __init__(self, repo_path: str = None):
        """Initialize the MCP server with repository path."""
        self.repo_path = Path(repo_path) if repo_path else Path.cwd()
        self.server = Server("documentation-mcp-server")
        
        # Initialize MCP manager
        self.mcp_manager = MCPManager()
        
        # Register tools
        self._register_tools()
    
    def _register_tools(self):
        """Register MCP tools."""
        
        @self.server.call_tool()
        async def get_relevant_files(arguments: dict) -> List[types.TextContent]:
            """
            Find relevant files based on a natural language description.
            
            Args:
                arguments (dict): Dictionary containing description
                
            Returns:
                List of relevant file paths relative to repository root
            """
            try:
                description = arguments.get("description", "")
                if not description:
                    return [types.TextContent(
                        type="text",
                        text="Error: Description parameter is required"
                    )]
                
                # Use MCP manager to get relevant files
                result = await self.mcp_manager.get_relevant_files(
                    description=description,
                    repo_path=str(self.repo_path)
                )
                
                return [types.TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )]
                
            except Exception as e:
                return [types.TextContent(
                    type="text",
                    text=f"Error processing get_relevant_files request: {str(e)}"
                )]
        
        @self.server.call_tool()
        async def understand_feature(arguments: dict) -> List[types.TextContent]:
            """
            Get documentation about a specific feature or functionality.
            
            Args:
                arguments (dict): Dictionary containing feature_description
                
            Returns:
                Documentation content about the feature
            """
            try:
                feature_description = arguments.get("feature_description", "")
                if not feature_description:
                    return [types.TextContent(
                        type="text",
                        text="Error: feature_description parameter is required"
                    )]
                
                # Use MCP manager to understand feature
                result = await self.mcp_manager.understand_feature(
                    feature_description=feature_description,
                    repo_path=str(self.repo_path)
                )
                
                return [types.TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )]
                
            except Exception as e:
                return [types.TextContent(
                    type="text",
                    text=f"Error processing feature understanding request: {str(e)}"
                )]
    
    def get_server(self) -> Server:
        """Get the configured MCP server instance."""
        return self.server


class HTTPMCPWrapper:
    """HTTP wrapper for MCP server when SSE transport is not available."""
    
    def __init__(self, mcp_server: DocumentationMCPServer, port: int = 3333):
        self.mcp_server = mcp_server
        self.port = port
        self.app = FastAPI(title="Documentation MCP Server", version="1.0.0")
        
        # Add CORS middleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup HTTP routes for MCP operations."""
        
        @self.app.get("/")
        async def root():
            return {
                "name": "Documentation MCP Server",
                "version": "1.0.0",
                "description": "MCP server for repository documentation interaction",
                "tools": [
                    {
                        "name": "get_relevant_files",
                        "description": "Find relevant files based on a natural language description"
                    },
                    {
                        "name": "understand_feature", 
                        "description": "Get documentation about a specific feature"
                    }
                ]
            }
        
        @self.app.get("/tools")
        async def list_tools():
            """List available tools."""
            return {
                "tools": [
                    {
                        "name": "get_relevant_files",
                        "description": "Find relevant files based on a natural language description of what you're looking for",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "description": {
                                    "type": "string",
                                    "description": "Plain English description of the files you need"
                                }
                            },
                            "required": ["description"]
                        }
                    },
                    {
                        "name": "understand_feature",
                        "description": "Get documentation and understanding of a specific feature or functionality",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "feature_description": {
                                    "type": "string",
                                    "description": "Description of the feature you want to understand"
                                }
                            },
                            "required": ["feature_description"]
                        }
                    }
                ]
            }
        
        @self.app.post("/tools/{tool_name}")
        async def call_tool(tool_name: str, request: Request):
            """Call a specific tool."""
            try:
                body = await request.json()
                arguments = body.get("arguments", {})
                
                if tool_name == "get_relevant_files":
                    # Call the MCP manager directly
                    description = arguments.get("description", "")
                    if not description:
                        return {"error": "Description parameter is required"}
                    
                    result = await self.mcp_server.mcp_manager.find_relevant_files(
                        description=description,
                        repo_path=Path(self.mcp_server.repo_path)
                    )
                    return {"result": result.dict()}
                    
                elif tool_name == "understand_feature":
                    # Call the MCP manager directly
                    feature_description = arguments.get("feature_description", "")
                    if not feature_description:
                        return {"error": "feature_description parameter is required"}
                    
                    result = await self.mcp_server.mcp_manager.understand_feature(
                        feature_description=feature_description,
                        repo_path=Path(self.mcp_server.repo_path)
                    )
                    return {"result": result.dict()}
                    
                else:
                    return {"error": f"Unknown tool: {tool_name}"}
                    
            except Exception as e:
                return {"error": f"Error calling tool {tool_name}: {str(e)}"}
    
    async def run(self):
        """Run the HTTP server."""
        config = uvicorn.Config(
            self.app,
            host="127.0.0.1",
            port=self.port,
            log_level="info"
        )
        server = uvicorn.Server(config)
        
        print(f"🚀 Documentation MCP Server starting on http://127.0.0.1:{self.port}")
        print(f"📁 Repository path: {self.mcp_server.repo_path}")
        print(f"🔧 Available endpoints:")
        print(f"   GET  / - Server info")
        print(f"   GET  /tools - List available tools")
        print(f"   POST /tools/get_relevant_files - Find relevant files")
        print(f"   POST /tools/understand_feature - Understand features")
        print(f"\n📖 Example usage:")
        print(f"   curl -X POST http://127.0.0.1:{self.port}/tools/get_relevant_files \\")
        print(f"     -H 'Content-Type: application/json' \\")
        print(f"     -d '{{\"arguments\": {{\"description\": \"authentication files\"}}}}'")
        
        await server.serve()


async def main():
    """Main entry point for the MCP server."""
    parser = argparse.ArgumentParser(description="Documentation MCP Server")
    parser.add_argument("repo_path", nargs="?", help="Path to the repository (default: current directory)")
    parser.add_argument("--port", "-p", type=int, default=3333, help="Port to run HTTP server on (default: 3333)")
    parser.add_argument("--stdio", action="store_true", help="Use stdio transport instead of HTTP")
    
    args = parser.parse_args()
    
    # Get repository path
    repo_path = args.repo_path or os.getenv("DOCUMENTATION_REPO_PATH", os.getcwd())
    
    # Initialize the documentation MCP server
    doc_server = DocumentationMCPServer(repo_path)
    
    if args.stdio:
        # Use stdio transport (original MCP way)
        print(f"🚀 Starting MCP server with stdio transport")
        print(f"📁 Repository path: {repo_path}")
        
        server = doc_server.get_server()
        
        # Define available tools
        @server.list_tools()
        async def handle_list_tools() -> List[types.Tool]:
            """List available tools."""
            return [
                types.Tool(
                    name="get_relevant_files",
                    description="Find relevant files based on a natural language description of what you're looking for",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "description": {
                                "type": "string",
                                "description": "Plain English description of the files you need (e.g., 'files related to user authentication', 'implementation of workflow X')"
                            }
                        },
                        "required": ["description"]
                    }
                ),
                types.Tool(
                    name="understand_feature",
                    description="Get documentation and understanding of a specific feature or functionality",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "feature_description": {
                                "type": "string",
                                "description": "Description of the feature you want to understand (e.g., 'AI workflow calculating drive time', 'user registration system')"
                            }
                        },
                        "required": ["feature_description"]
                    }
                )
            ]
        
        # Run with stdio
        import mcp.server.stdio
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="documentation-mcp-server",
                    server_version="1.0.0",
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={}
                    )
                )
            )
    else:
        # Use HTTP transport
        http_wrapper = HTTPMCPWrapper(doc_server, args.port)
        await http_wrapper.run()


if __name__ == "__main__":
    asyncio.run(main())
