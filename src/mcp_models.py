"""
Models for MCP (Model Context Protocol) server operations.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from pathlib import Path


class MCPFileResult(BaseModel):
    """Model representing a relevant file result from MCP operations."""
    
    file_path: str
    summary: str
    relevance_score: Optional[float] = None
    reasoning: Optional[str] = None


class MCPRelevantFilesRequest(BaseModel):
    """Request model for finding relevant files."""
    
    description: str
    max_results: int = 10
    include_test_files: bool = False


class MCPRelevantFilesResponse(BaseModel):
    """Response model for relevant files results."""
    
    query_description: str
    relevant_files: List[MCPFileResult] = Field(default_factory=list)
    total_files_analyzed: int = 0
    processing_time_seconds: Optional[float] = None


class MCPFeatureRequest(BaseModel):
    """Request model for understanding a feature."""
    
    feature_description: str
    include_implementation_details: bool = True
    max_sections: int = 5


class MCPDocumentationFile(BaseModel):
    """Model representing a loaded documentation file."""
    
    file_path: str
    content: str
    loaded_successfully: bool = True
    error_message: Optional[str] = None


class MCPFeatureResponse(BaseModel):
    """Response model for feature understanding."""
    
    feature_description: str
    comprehensive_answer: str
    key_components: List[str] = Field(default_factory=list)
    implementation_details: str = ""
    usage_examples: str = ""
    related_concepts: List[str] = Field(default_factory=list)
    source_documentation_files: List[str] = Field(default_factory=list)


class MCPState(BaseModel):
    """State model for MCP operations using LangGraph."""
    
    # Request information
    request_type: str  # "relevant_files" or "understand_feature"
    user_query: str
    
    # Documentation context
    documentation_guide_content: str = ""
    documentation_loaded: bool = False
    
    # Feature understanding workflow state
    discovered_documentation_files: List[str] = Field(default_factory=list)
    loaded_documentation_files: List[MCPDocumentationFile] = Field(default_factory=list)
    current_file_index: int = 0
    files_discovery_complete: bool = False
    all_files_loaded: bool = False
    
    # Processing state
    llm_analysis_complete: bool = False
    
    # Raw LLM responses (for internal workflow processing)
    raw_llm_response: dict = Field(default_factory=dict)
    raw_synthesis_response: dict = Field(default_factory=dict)
    
    # Results
    relevant_files_result: Optional[MCPRelevantFilesResponse] = None
    feature_understanding_result: Optional[MCPFeatureResponse] = None
    
    # Error handling
    error_occurred: bool = False
    error_message: str = ""
    
    # Configuration
    repo_path: Path
    max_results: int = 10