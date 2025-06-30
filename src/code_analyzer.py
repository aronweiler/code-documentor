import os
from typing import List
from pathlib import Path
from .models import CodeFile, PipelineConfig


class CodeAnalyzer:
    """Analyzes code repositories and extracts files for documentation."""
    
    def __init__(self, config: PipelineConfig):
        self.config = config
    
    def scan_repository(self, repo_path: Path) -> List[CodeFile]:
        """Scan repository and return list of code files to document."""
        if not repo_path.exists() or not repo_path.is_dir():
            raise ValueError(f"Repository path does not exist or is not a directory: {repo_path}")
        
        code_files = []
        supported_extensions = self.config.file_processing.get("supported_extensions", [])
        exclude_patterns = self.config.file_processing.get("exclude_patterns", [])
        
        for file_path in repo_path.rglob('*'):
            if self._should_include_file(file_path, supported_extensions, exclude_patterns):
                try:
                    content = self._read_code_file(file_path)
                    relative_path = str(file_path.relative_to(repo_path))
                    
                    code_file = CodeFile(
                        path=file_path,
                        content=content,
                        extension=file_path.suffix,
                        relative_path=relative_path
                    )
                    code_files.append(code_file)
                    
                except Exception as e:
                    print(f"Warning: Could not read {file_path}: {e}")
        
        return sorted(code_files, key=lambda x: x.relative_path)
    
    def _should_include_file(self, file_path: Path, supported_extensions: List[str], exclude_patterns: List[str]) -> bool:
        """Check if a file should be included in documentation generation."""
        try:
            # See if the file is acecssible first
            if not file_path.exists():
                return False
            
            if not file_path.is_file():
                return False
        except OSError:
            return False
        
        # Check file extension
        if supported_extensions and file_path.suffix not in supported_extensions:
            return False
        
        # Check exclude patterns
        file_str = str(file_path)
        for pattern in exclude_patterns:
            if pattern in file_str:
                return False
        
        # Skip empty files
        try:
            if file_path.stat().st_size == 0:
                return False
        except OSError:
            return False
        
        return True
    
    def _read_code_file(self, file_path: Path) -> str:
        """Read content from a code file."""
        encodings = ['utf-8', 'utf-16', 'cp1252', 'iso-8859-1']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
        
        # If all encodings fail, try binary mode with error handling
        with open(file_path, 'rb') as f:
            return f.read().decode('utf-8', errors='ignore')
    
    def analyze_file_structure(self, code_files: List[CodeFile]) -> dict:
        """Analyze the structure of code files for better documentation context."""
        structure = {
            "total_files": len(code_files),
            "by_extension": {},
            "by_directory": {},
            "largest_files": []
        }
        
        # Group by extension
        for code_file in code_files:
            ext = code_file.extension
            if ext not in structure["by_extension"]:
                structure["by_extension"][ext] = 0
            structure["by_extension"][ext] += 1
        
        # Group by directory
        for code_file in code_files:
            directory = str(Path(code_file.relative_path).parent)
            if directory not in structure["by_directory"]:
                structure["by_directory"][directory] = 0
            structure["by_directory"][directory] += 1
        
        # Find largest files
        structure["largest_files"] = sorted(
            [(cf.relative_path, len(cf.content)) for cf in code_files],
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        return structure
