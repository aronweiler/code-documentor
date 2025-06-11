from pathlib import Path
from typing import List, Optional, Dict, Any
import os


def read_file_content(file_path: str, repo_path: str) -> str:
    """
    Read the content of a file within the repository.

    Args:
        file_path: Relative or absolute path to the file
        repo_path: Root path of the repository

    Returns:
        File content as string

    Raises:
        FileNotFoundError: If file doesn't exist
        PermissionError: If file can't be read
        ValueError: If file is outside repository bounds
    """
    repo_root = Path(repo_path).resolve()

    # Handle both relative and absolute paths
    if Path(file_path).is_absolute():
        target_path = Path(file_path).resolve()
    else:
        target_path = (repo_root / file_path).resolve()

    # Security check: ensure file is within repository
    try:
        target_path.relative_to(repo_root)
    except ValueError:
        raise ValueError(f"File path {file_path} is outside repository bounds")

    if not target_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if not target_path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")

    # Try multiple encodings
    encodings = ['utf-8', 'utf-16', 'cp1252', 'iso-8859-1']

    for encoding in encodings:
        try:
            with open(target_path, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue

    # If all encodings fail, try binary mode with error handling
    with open(target_path, 'rb') as f:
        return f.read().decode('utf-8', errors='ignore')


def list_files_in_directory(directory_path: str, repo_path: str, 
                          extensions: Optional[List[str]] = None,
                          recursive: bool = True) -> List[str]:
    """
    List files in a directory within the repository.

    Args:
        directory_path: Relative path to directory from repo root
        repo_path: Root path of the repository
        extensions: Optional list of file extensions to filter (e.g., ['.py', '.js'])
        recursive: Whether to search subdirectories

    Returns:
        List of relative file paths
    """
    repo_root = Path(repo_path).resolve()
    target_dir = (repo_root / directory_path).resolve()

    # Security check
    try:
        target_dir.relative_to(repo_root)
    except ValueError:
        raise ValueError(f"Directory path {directory_path} is outside repository bounds")

    if not target_dir.exists():
        raise FileNotFoundError(f"Directory not found: {directory_path}")

    if not target_dir.is_dir():
        raise ValueError(f"Path is not a directory: {directory_path}")

    files = []
    pattern = "**/*" if recursive else "*"

    for file_path in target_dir.glob(pattern):
        if file_path.is_file():
            # Filter by extensions if provided
            if extensions and file_path.suffix.lower() not in [ext.lower() for ext in extensions]:
                continue

            # Return path relative to repo root
            relative_path = file_path.relative_to(repo_root)
            files.append(str(relative_path))

    return sorted(files)


def find_files_by_pattern(pattern: str, repo_path: str, 
                         directory: Optional[str] = None) -> List[str]:
    """
    Find files matching a pattern within the repository.

    Args:
        pattern: Glob pattern to match (e.g., "*.py", "test_*.py")
        repo_path: Root path of the repository
        directory: Optional subdirectory to search within

    Returns:
        List of relative file paths matching the pattern
    """
    repo_root = Path(repo_path).resolve()

    if directory:
        search_root = (repo_root / directory).resolve()
        # Security check
        try:
            search_root.relative_to(repo_root)
        except ValueError:
            raise ValueError(f"Directory path {directory} is outside repository bounds")
    else:
        search_root = repo_root

    if not search_root.exists():
        raise FileNotFoundError(f"Search directory not found: {directory or '.'}")

    files = []
    for file_path in search_root.rglob(pattern):
        if file_path.is_file():
            relative_path = file_path.relative_to(repo_root)
            files.append(str(relative_path))

    return sorted(files)


def get_file_info(file_path: str, repo_path: str) -> Dict[str, Any]:
    """
    Get information about a file.

    Args:
        file_path: Relative path to file from repo root
        repo_path: Root path of the repository

    Returns:
        Dictionary with file information
    """
    repo_root = Path(repo_path).resolve()
    target_path = (repo_root / file_path).resolve()

    # Security check
    try:
        target_path.relative_to(repo_root)
    except ValueError:
        raise ValueError(f"File path {file_path} is outside repository bounds")

    if not target_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    stat = target_path.stat()

    return {
        "path": file_path,
        "name": target_path.name,
        "extension": target_path.suffix,
        "size_bytes": stat.st_size,
        "modified_time": stat.st_mtime,
        "is_file": target_path.is_file(),
        "is_directory": target_path.is_dir(),
    }