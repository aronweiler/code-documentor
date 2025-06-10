from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from pathlib import Path


class PipelineConfig(BaseModel):
    """Configuration model for the documentation pipeline."""

    model: Dict[str, Any] = Field(default_factory=dict)
    token_limits: Dict[str, int] = Field(default_factory=dict)
    file_processing: Dict[str, Any] = Field(default_factory=dict)
    processing: Dict[str, Any] = Field(default_factory=dict)
    output: Dict[str, Any] = Field(default_factory=dict)
    templates: Dict[str, str] = Field(default_factory=dict)
    design_docs: Dict[str, Any] = Field(default_factory=dict)  


class DocumentationRequest(BaseModel):
    """Request model for documentation generation."""

    repo_path: Path
    docs_path: Optional[Path] = None
    output_path: Path
    config: PipelineConfig
    generate_design_docs: bool = False
    design_docs_only: bool = False  


class CodeFile(BaseModel):
    """Model representing a code file to be documented."""

    path: Path
    content: str
    extension: str
    relative_path: str


class DocumentationContext(BaseModel):
    """Model representing the existing documentation context."""

    content: str
    token_count: int
    summarized: bool = False
    original_docs: List[str] = Field(default_factory=list)


class DocumentationResult(BaseModel):
    """Model representing the generated documentation for a file."""

    file_path: Path
    documentation: str
    success: bool
    error_message: Optional[str] = None


class DocumentationGuideEntry(BaseModel):
    """Model representing an entry in the documentation guide."""

    doc_file_path: str  # Relative path to the documentation file
    summary: str        # Short summary of what the documentation contains
    original_file_path: str  # Relative path to the original source file


class DocumentationGuide(BaseModel):
    """Model representing the complete documentation guide."""

    entries: List[DocumentationGuideEntry] = Field(default_factory=list)
    total_files: int = 0
    generation_date: str = ""


class PipelineState(BaseModel):
    """State model for the LangGraph pipeline."""

    request: DocumentationRequest
    existing_docs: DocumentationContext
    code_files: List[CodeFile] = Field(default_factory=list)
    results: List[DocumentationResult] = Field(default_factory=list)
    current_file_index: int = 0
    completed: bool = False
    documentation_guide: Optional[DocumentationGuide] = None  