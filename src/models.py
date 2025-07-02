from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from pathlib import Path


class PipelineConfig(BaseModel):
    """Configuration model for the documentation pipeline."""

    logging: Dict[str, Any] = Field(default_factory=dict)
    model: Dict[str, Any] = Field(default_factory=dict)
    token_limits: Dict[str, int] = Field(default_factory=dict)
    file_processing: Dict[str, Any] = Field(default_factory=dict)
    processing: Dict[str, Any] = Field(default_factory=dict)
    output: Dict[str, Any] = Field(default_factory=dict)
    templates: Dict[str, Any] = Field(default_factory=dict)
    design_docs: Dict[str, Any] = Field(default_factory=dict)
    retry_config: Dict[str, Any] = Field(default_factory=dict)  


class DocumentationRequest(BaseModel):
    """Request model for documentation generation."""

    repo_path: Path
    docs_path: Optional[Path] = None
    output_path: Path
    config: PipelineConfig
    file_docs: bool = False
    design_docs: bool = False
    guide: bool = False
    force_full_guide: bool = False


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

    
class DesignDocumentSection(BaseModel):
    """Model representing a section within a design document."""

    name: str
    enabled: bool
    max_tokens: int
    template: str
    content: Optional[str] = None
    success: bool = False
    error_message: Optional[str] = None
    retry_count: int = 0
    
class DesignDocument(BaseModel):
    """Model representing a complete design document."""

    name: str
    sections: List[DesignDocumentSection] = Field(default_factory=list)
    assembled_content: Optional[str] = None
    file_path: Optional[Path] = None
    success: bool = False
    error_message: Optional[str] = None
    
class DesignDocumentationState(BaseModel):
    """Model representing the state of design documentation generation."""

    documents: List[DesignDocument] = Field(default_factory=list)
    current_document_index: int = 0
    current_section_index: int = 0
    completed_documents: List[str] = Field(default_factory=list)  # Names of completed docs
    accumulated_context: str = ""  # Context from previously generated documents
    completed: bool = False
    
class FileMetadata(BaseModel):
    """Tracks metadata for a single file in incremental guide generation."""
    
    source_file_path: str  # Relative path to source file
    source_file_modified: float  # Source file modification timestamp
    doc_file_path: str  # Relative path to documentation file
    doc_generated: float  # Documentation generation timestamp
    doc_file_hash: str  # Content hash for change detection
    guide_entry_generated: float  # When guide entry was last generated
    guide_entry_hash: str  # Hash of current guide entry content

class GuideMetadata(BaseModel):
    """Tracks overall guide state for incremental updates."""
    
    guide_last_generated: float
    guide_version: int = 1
    tracked_files: Dict[str, FileMetadata] = Field(default_factory=dict)  # keyed by relative source path
    guide_structure_hash: str = ""  # to detect template changes

class ChangeSet(BaseModel):
    """Represents detected changes for incremental guide generation."""
    
    new_files: List[str] = Field(default_factory=list)  # New source files
    modified_files: List[str] = Field(default_factory=list)  # Modified source files
    deleted_files: List[str] = Field(default_factory=list)  # Deleted source files
    force_full_rebuild: bool = False  # Force complete guide regeneration

class PipelineState(BaseModel):
    """State model for the LangGraph pipeline."""

    request: DocumentationRequest
    existing_docs: DocumentationContext
    code_files: List[CodeFile] = Field(default_factory=list)
    results: List[DocumentationResult] = Field(default_factory=list)
    current_file_index: int = 0
    completed: bool = False
    documentation_guide: Optional[DocumentationGuide] = None
    design_documentation_state: Optional[DesignDocumentationState] = None
    guide_change_set: Optional[ChangeSet] = None  # For incremental guide updates