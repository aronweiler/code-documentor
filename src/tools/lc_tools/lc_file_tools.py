from typing import List
from pathlib import Path
from langchain.tools import Tool
from ..file_tools import (
    read_file_content,
    list_files_in_directory,
    find_files_by_pattern,
    get_file_info
)


def create_file_tools(repo_path: Path) -> List[Tool]:
    """Create LangChain tools for file operations within a repository."""

    def read_file_wrapper(file_path: str) -> str:
        """Read the content of a file within the repository."""
        try:
            return read_file_content(file_path, str(repo_path))
        except Exception as e:
            return f"Error reading file {file_path}: {str(e)}"

    def list_files_wrapper(directory_path: str, extensions: str = "", recursive: str = "true") -> str:
        """List files in a directory. Extensions should be comma-separated (e.g., '.py,.js'). Recursive is 'true' or 'false'."""
        try:
            ext_list = [ext.strip() for ext in extensions.split(",")] if extensions else None
            is_recursive = recursive.lower() == "true"
            files = list_files_in_directory(directory_path, str(repo_path), ext_list, is_recursive)
            return "\n".join(files) if files else "No files found"
        except Exception as e:
            return f"Error listing files in {directory_path}: {str(e)}"

    def find_files_wrapper(pattern: str, directory: str = "") -> str:
        """Find files matching a pattern. Directory is optional."""
        try:
            files = find_files_by_pattern(pattern, str(repo_path), directory if directory else None)
            return "\n".join(files) if files else "No files found matching pattern"
        except Exception as e:
            return f"Error finding files with pattern {pattern}: {str(e)}"

    def get_file_info_wrapper(file_path: str) -> str:
        """Get information about a file."""
        try:
            info = get_file_info(file_path, str(repo_path))
            return f"File: {info['path']}\nSize: {info['size_bytes']} bytes\nExtension: {info['extension']}\nModified: {info['modified_time']}"
        except Exception as e:
            return f"Error getting info for {file_path}: {str(e)}"

    file_tools = [
        Tool(
            name="read_file_content",
            description="Read the content of any file in the repository. Use relative paths from repository root.",
            func=read_file_wrapper
        ),
        Tool(
            name="list_files_in_directory", 
            description="List files in a directory. Parameters: directory_path (required), extensions (optional, comma-separated like '.py,.js'), recursive (optional, 'true' or 'false', default 'true')",
            func=list_files_wrapper
        ),
        Tool(
            name="find_files_by_pattern",
            description="Find files matching a glob pattern. Parameters: pattern (required, e.g., '*.py', 'test_*.py'), directory (optional, subdirectory to search within)",
            func=find_files_wrapper
        ),
        Tool(
            name="get_file_info",
            description="Get information about a file including size, extension, and modification time.",
            func=get_file_info_wrapper
        )
    ]

    return file_tools