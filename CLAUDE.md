# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Basic Usage
```bash
# Generate all documentation types
python main.py generate --repo-path /path/to/repo --file-docs --design-docs --guide

# Generate only file documentation
python main.py generate --repo-path /path/to/repo --file-docs

# Generate only design documents
python main.py generate --repo-path /path/to/repo --design-docs

# Generate only documentation guide
python main.py generate --repo-path /path/to/repo --guide

# Analyze repository structure without generating docs
python main.py analyze /path/to/repo

# Validate configuration
python main.py validate-config
```

### Environment Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

### Configuration
- Main config: `config.yaml`
- Environment variables: `.env` file
- API keys required for OpenAI, Anthropic, or Azure OpenAI

## Architecture Overview

This is an AI-powered documentation generation toolkit built with **LangGraph** for workflow orchestration and **LangChain** for LLM integration.

### Core Pipeline Architecture

The system uses a **state-based workflow** (`langgraph.StateGraph`) with the following key components:

1. **DocumentationPipeline** (`src/pipeline.py`) - Main orchestrator using LangGraph
2. **ConfigManager** (`src/config.py`) - Configuration and API key management
3. **LLMManager** (`src/llm_manager.py`) - Multi-provider LLM abstraction
4. **Code Analysis** (`src/code_analyzer.py`) - Repository scanning and file analysis
5. **Document Processing** (`src/document_processor.py`) - Context preparation and document loading
6. **Specialized Generators**:
   - `src/design_document_generator.py` - Design documentation
   - `src/guide_generator.py` - Documentation guides
   - `src/file_processor.py` - Individual file documentation

### State Management
- **PipelineState** model tracks workflow state
- **StateManager** (`src/state_manager.py`) handles state transitions
- **ContextManager** (`src/context_manager.py`) manages documentation context and token limits

### Data Flow
1. **Configuration Loading**: Config and API keys loaded
2. **Repository Scanning**: Code files discovered and filtered
3. **Context Preparation**: Existing docs loaded and summarized if needed
4. **Documentation Generation**: Files processed individually or in batches
5. **Guide Assembly**: Optional consolidated guide generation
6. **Design Documents**: High-level architecture documentation
7. **Report Generation**: Summary reports and metrics

### Key Models (`src/models.py`)
- `PipelineState` - Main workflow state
- `DocumentationRequest` - Input parameters
- `DocumentationResult` - Output results
- `CodeFile` - File metadata and content
- `DocumentationContext` - Context with token management

### LLM Integration
- Multi-provider support: OpenAI, Anthropic, Azure OpenAI
- Token management with automatic chunking and summarization
- Retry logic for failed generations
- Incremental processing to minimize API costs

## Important Configuration

### Model Configuration
The system supports multiple LLM providers configured in `config.yaml`:
```yaml
model:
  provider: "openai"  # openai, anthropic, azure_openai
  name: "gpt-4"
  temperature: 0.2
  max_tokens: 32000
```

### Processing Limits
```yaml
processing:
  max_files: 1000  # Limit number of files processed
  save_incrementally: true  # Save files as processed

token_limits:
  max_context_tokens: 50000
  summarization_threshold: 50000
  chunk_size: 10000
```

### File Processing
The system processes files based on extensions and exclusion patterns defined in `config.yaml`. Key exclusions include `__pycache__`, `node_modules`, `.git`, etc.

## Development Notes

### Error Handling
- Robust error handling with retry logic
- Incremental saving prevents data loss
- Detailed logging and error reporting

### State-Based Workflow
The LangGraph pipeline uses conditional edges and decision nodes to:
- Skip unchanged files (incremental processing)
- Handle different documentation types
- Manage token limits through summarization
- Process large repositories efficiently

### Token Management
- Automatic context summarization when limits exceeded
- Chunking for large files
- Provider-specific token counting

### Output Structure
```
documentation_output/
├── design_documentation/    # Design docs
├── src/                    # File documentation (mirrors source structure)
├── documentation_guide.md  # Consolidated guide
└── documentation_report.md # Generation report
```