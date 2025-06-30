<!-- AUTO-GENERATED DOCUMENTATION -->
<!-- This file was automatically generated and should not be manually edited -->
<!-- To update this documentation, regenerate it using the documentation pipeline -->

# Documentation for src/mcp_models.py

# `src/mcp_models.py` Documentation

## Purpose

This file defines the core [Pydantic](https://pydantic-docs.helpmanual.io/) data models used by an MCP (Model Context Protocol) server. These models are used for request and response structures as part of the server's key features, such as searching for relevant files and understanding codebase features. The file serves as a central place to define clear, validated schemas for communication and workflow state management in the MCP system.

---

## Functionality

The file provides structured representations for the following operations:

- **Relevant Files Search**: Models for querying and returning relevant files from a codebase.
- **Feature Understanding**: Models for querying and generating comprehensive information about specific features or components.
- **Documentation Handling**: Models for handling loaded documentation files.
- **Workflow State Management**: A model for representing the end-to-end state of a request/response flow within the MCP, supporting integration with tools like LangGraph.

Each model is implemented as a Pydantic `BaseModel` for validation, conversion, and improved developer ergonomics.

---

## Key Components

### Classes

#### 1. `MCPFileResult`
Represents a single relevant file found during file search operations.

- `file_path`: `str` — Path to the file.
- `summary`: `str` — Short summary of file content or relevance.
- `relevance_score`: `Optional[float]` — Relevance score (if calculated).
- `reasoning`: `Optional[str]` — Justification for file's relevance.

#### 2. `MCPRelevantFilesRequest`
Structure of a request for relevant files.

- `description`: `str` — Description of what files to search for.
- `max_results`: `int` (default: 10) — Maximum number of files to return.
- `include_test_files`: `bool` (default: False) — Whether to include test files.

#### 3. `MCPRelevantFilesResponse`
Response model listing results of the relevant files search.

- `query_description`: `str` — Description used in the search query.
- `relevant_files`: `List[MCPFileResult]` — List of matching files.
- `total_files_analyzed`: `int` — Total files considered during search.
- `processing_time_seconds`: `Optional[float]` — Time taken for processing.

#### 4. `MCPFeatureRequest`
Request model for generating documentation or understanding a feature.

- `feature_description`: `str` — Description of the feature/component.
- `include_implementation_details`: `bool` (default: True) — Whether to add implementation specifics.
- `max_sections`: `int` (default: 5) — Limit on how many documentation sections to include.

#### 5. `MCPDocumentationFile`
Represents a loaded documentation file or artifact.

- `file_path`: `str` — Path to the documentation file.
- `content`: `str` — File contents.
- `loaded_successfully`: `bool` (default: True) — Whether file loaded without error.
- `error_message`: `Optional[str]` — Error info if loading failed.

#### 6. `MCPFeatureResponse`
Response model for a feature understanding request.

- `feature_description`: `str` — What was requested.
- `comprehensive_answer`: `str` — Detailed answer/summary.
- `key_components`: `List[str]` — List of important concepts/components.
- `implementation_details`: `str` — Technical implementation information.
- `usage_examples`: `str` — Code snippets or usage guidance.
- `related_concepts`: `List[str]` — Related topics.
- `source_documentation_files`: `List[str]` — Source files/docs referenced.

#### 7. `MCPState`
Global state for the MCP request/response workflow, especially for integration with orchestrators like LangGraph.

- **Request and Query Info**
    - `request_type`: `str` — Either `"relevant_files"` or `"understand_feature"`.
    - `user_query`: `str` — Original user input.
- **Documentation Context**
    - `documentation_guide_content`: `str`
    - `documentation_loaded`: `bool`
- **Workflow State**
    - `discovered_documentation_files`: `List[str]`
    - `loaded_documentation_files`: `List[MCPDocumentationFile]`
    - `current_file_index`: `int`
    - `files_discovery_complete`: `bool`
    - `all_files_loaded`: `bool`
- **Processing State**
    - `llm_analysis_complete`: `bool`
- **Raw LLM Responses**
    - `raw_llm_response`: `dict`
    - `raw_synthesis_response`: `dict`
- **Results**
    - `relevant_files_result`: `Optional[MCPRelevantFilesResponse]`
    - `feature_understanding_result`: `Optional[MCPFeatureResponse]`
- **Error Handling**
    - `error_occurred`: `bool`
    - `error_message`: `str`
- **Configuration**
    - `repo_path`: `Path`
    - `max_results`: `int`

---

## Dependencies

- **Third-party**
    - `pydantic`: Used for robust model/field validation and easy data serialization.
- **Standard library**
    - `typing`: For type annotations.
    - `pathlib`: For the `Path` type, used in `MCPState`.

**Downstream Usage**  
Any server implementation, API layer, or workflow engine (e.g., LangGraph) that requires structured state or request/response envelopes for MCP operations will depend on these models.

---

## Usage Examples

### 1. Finding Relevant Files

```python
from src.mcp_models import MCPRelevantFilesRequest, MCPRelevantFilesResponse

# Formulate a request
request = MCPRelevantFilesRequest(
    description="Find all files related to authentication",
    max_results=5,
    include_test_files=True
)

# After processing (pseudo-code)
response = MCPRelevantFilesResponse(
    query_description=request.description,
    relevant_files=[
        MCPFileResult(
            file_path="src/auth.py",
            summary="Handles login and token validation",
            relevance_score=0.92
        ),
    ],
    total_files_analyzed=120,
    processing_time_seconds=0.45
)
```

### 2. Understanding a Feature

```python
from src.mcp_models import MCPFeatureRequest, MCPFeatureResponse

# Feature understanding request
feature_req = MCPFeatureRequest(
    feature_description="Explain how user login is implemented"
)

# After processing (pseudo-code)
feature_resp = MCPFeatureResponse(
    feature_description=feature_req.feature_description,
    comprehensive_answer="User login is handled by ...",
    key_components=["auth.py", "token.py"],
    usage_examples="See /examples/login_example.py"
)
```

### 3. In a Workflow State

```python
from src.mcp_models import MCPState, MCPDocumentationFile
from pathlib import Path

state = MCPState(
    request_type="understand_feature",
    user_query="How does file upload work?",
    repo_path=Path("/path/to/project"),
    max_results=10
)

# Add discovered and loaded documentation files within workflow
state.discovered_documentation_files.append("docs/upload.md")
state.loaded_documentation_files.append(
    MCPDocumentationFile(
        file_path="docs/upload.md",
        content="...",
        loaded_successfully=True
    )
)
```

---

## Summary

This file provides robust data models for using, validating, and managing requests, responses, and workflow state within the Model Context Protocol server and its related tooling. All central MCP objects for searching and explaining parts of a codebase are defined here, forming the backbone of server operations and workflow orchestration.

---
<!-- GENERATION METADATA -->
```yaml
# Documentation Generation Metadata
file_hash: e48743ca06ac853c859897e075c3941e2b2fd115e61500acbcf3f06c6aafdf7a
relative_path: src/mcp_models.py
generation_date: 2025-06-30T00:09:19.091107
```
<!-- END GENERATION METADATA -->
