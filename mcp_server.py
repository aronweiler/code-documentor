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
            description = arguments.get("description", "")
            
            if not description:
                return [types.TextContent(
                    type="text",
                    text="Error: Description parameter is required"
                )]
            
            try:
                # Use MCPManager to find relevant files
                result = await self.mcp_manager.find_relevant_files(
                    description=description,
                    repo_path=self.repo_path,
                    max_results=10
                )
                
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
                    text=f"Error processing request: {str(e)}"
                )]
        
        @self.server.call_tool()
        async def understand_feature(*args, **kwargs) -> List[types.TextContent]:
            """
            Get documentation and understanding of a specific feature.
            
            Args:
                arguments (dict): Dictionary containing feature_description
                
            Returns:
                Related documentation content about the feature
            """
            # Debug: log what we receive
            print(f"DEBUG: args={args}, kwargs={kwargs}")
            
            # Try to extract feature_description from different possible formats
            feature_description = ""
            if args and isinstance(args[0], dict):
                feature_description = args[0].get("feature_description", "")
                print(f"DEBUG: Extracted from dict: {feature_description}")
            elif args and isinstance(args[0], str):
                feature_description = args[0]
                print(f"DEBUG: Using string directly: {feature_description}")
            elif "feature_description" in kwargs:
                feature_description = kwargs["feature_description"]
                print(f"DEBUG: Extracted from kwargs: {feature_description}")
            
            print(f"DEBUG: Final feature_description: {feature_description}")
            
            if not feature_description:
                return [types.TextContent(
                    type="text",
                    text="Error: feature_description parameter is required"
                )]
            
            try:
                # Use MCPManager to understand the feature
                result = await self.mcp_manager.understand_feature(
                    feature_description=feature_description,
                    repo_path=self.repo_path
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
                    text=f"Error processing feature understanding request: {str(e)}"
                )]
    
    def get_server(self) -> Server:
        """Get the configured MCP server instance."""
        return self.server


async def main():
    """Main entry point for the MCP server."""
    # Get repository path from command line argument or environment variable
    repo_path = None
    if len(sys.argv) > 1:
        repo_path = sys.argv[1]
    else:
        repo_path = os.getenv("DOCUMENTATION_REPO_PATH", os.getcwd())
    
    # Initialize the documentation MCP server
    doc_server = DocumentationMCPServer(repo_path)
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