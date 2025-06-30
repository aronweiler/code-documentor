#!/usr/bin/env python3
"""
MCP Server for Repository Documentation
Provides tools to interact with generated documentation and find relevant files.
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any, List

import mcp.server.stdio
import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from pydantic import AnyUrl

# Import our MCP manager and models
from src.mcp_manager import MCPManager

class DocumentationMCPServer:
    """MCP Server for repository documentation interaction."""
    
    def __init__(self, repo_path: str = None):
        """Initialize the MCP server with repository path."""
        self.repo_path = Path(repo_path) if repo_path else Path.cwd()
        self.server = Server("documentation-mcp-server")
        
        # Debug logging to file
        debug_log_path = Path("/tmp/mcp_debug.log")
        with open(debug_log_path, "a") as f:
            f.write(f"DEBUG: MCP Server initialized with repo_path: {self.repo_path}\n")
            doc_guide_path = self.repo_path / "documentation_output" / "documentation_guide.md"
            f.write(f"DEBUG: Looking for documentation guide at: {doc_guide_path}\n")
            f.write(f"DEBUG: Documentation guide exists: {doc_guide_path.exists()}\n")
            f.write(f"DEBUG: Current working directory: {Path.cwd()}\n")
            f.write("---\n")
        
        # Initialize MCP manager
        self.mcp_manager = MCPManager()
    
    
    def get_server(self) -> Server:
        """Get the configured MCP server instance."""
        return self.server


async def main():
    """Main entry point for the MCP server."""
    debug_log_path = Path("/tmp/mcp_debug.log")
    try:
        # Get repository path from command line argument or environment variable
        repo_path = None
        if len(sys.argv) > 1:
            repo_path = sys.argv[1]
        else:
            repo_path = os.getenv("DOCUMENTATION_REPO_PATH", os.getcwd())
        
        with open(debug_log_path, "a") as f:
            f.write(f"MCP Server main(): Starting with repo_path: {repo_path}\n")
            f.write(f"MCP Server main(): sys.argv: {sys.argv}\n")
        
        # Initialize the documentation MCP server
        doc_server = DocumentationMCPServer(repo_path)
        server = doc_server.get_server()
        
        with open(debug_log_path, "a") as f:
            f.write(f"MCP Server main(): Server initialized successfully\n")
    except Exception as e:
        with open(debug_log_path, "a") as f:
            f.write(f"MCP Server main(): ERROR during initialization: {str(e)}\n")
        raise
    
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
    
    # Register single tool handler that routes based on name
    @server.call_tool()
    async def handle_tool_call(name: str, arguments: dict) -> List[types.TextContent]:
        """Handle all tool calls and route based on name."""
        debug_log_path = Path("/tmp/mcp_debug.log")
        with open(debug_log_path, "a") as f:
            f.write(f"MCP Server: Tool called with name={name}, arguments={arguments}\n")
        
        if name == "get_relevant_files":
            description = arguments.get("description", "")
            
            if not description:
                return [types.TextContent(
                    type="text",
                    text="Error: Description parameter is required"
                )]
            
            try:
                with open(debug_log_path, "a") as f:
                    f.write(f"MCP Server: Processing get_relevant_files with description: {description}\n")
                
                # Use MCPManager to find relevant files
                result = await doc_server.mcp_manager.find_relevant_files(
                    description=description,
                    repo_path=doc_server.repo_path,
                    max_results=10
                )
                
                with open(debug_log_path, "a") as f:
                    f.write(f"MCP Server: MCPManager returned result: {result}\n")
                
                # Convert to JSON response
                response_data = {
                    "query_description": result.query_description,
                    "relevant_files": [
                        {
                            "file_path": file.file_path,
                            "summary": file.summary,
                            "relevance_score": file.relevance_score,
                            "reasoning": file.reasoning
                        }
                        for file in result.relevant_files
                    ],
                    "total_files_analyzed": result.total_files_analyzed,
                    "processing_time_seconds": result.processing_time_seconds
                }
                
                return [types.TextContent(
                    type="text", 
                    text=json.dumps(response_data, indent=2)
                )]
                
            except Exception as e:
                return [types.TextContent(
                    type="text",
                    text=f"Error processing get_relevant_files request: {str(e)}"
                )]
        
        elif name == "understand_feature":
            feature_description = arguments.get("feature_description", "")
            
            if not feature_description:
                return [types.TextContent(
                    type="text",
                    text="Error: feature_description parameter is required"
                )]
            
            try:
                with open(debug_log_path, "a") as f:
                    f.write(f"MCP Server: Processing understand_feature with description: {feature_description}\n")
                
                # Use MCPManager to understand the feature
                result = await doc_server.mcp_manager.understand_feature(
                    feature_description=feature_description,
                    repo_path=doc_server.repo_path
                )
                
                # Convert to JSON response
                response_data = {
                    "feature_description": result.feature_description,
                    "comprehensive_answer": result.comprehensive_answer,
                    "key_components": result.key_components,
                    "implementation_details": result.implementation_details,
                    "usage_examples": result.usage_examples,
                    "related_concepts": result.related_concepts,
                    "source_documentation_files": result.source_documentation_files
                }
                
                return [types.TextContent(
                    type="text",
                    text=json.dumps(response_data, indent=2)
                )]
                
            except Exception as e:
                return [types.TextContent(
                    type="text",
                    text=f"Error processing understand_feature request: {str(e)}"
                )]
        
        else:
            return [types.TextContent(
                type="text",
                text=f"Unknown tool: {name}"
            )]
    
    # Run the server
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


if __name__ == "__main__":
    asyncio.run(main())