# Code Documentation Toolkit with MCP Server

An intelligent, LLM-powered toolkit that automatically generates comprehensive documentation for codebases and provides an integrated Model Context Protocol (MCP) server for AI assistant integration. This tool leverages large language models (OpenAI, Anthropic, Azure OpenAI) to create high-quality, contextual documentation and offers seamless integration with AI coding assistants through MCP.

## Features

### Documentation Generation
- **Automated Code Analysis**: Scans repositories and analyzes code structure
- **LLM-Powered Documentation**: Generates contextual documentation using advanced AI models
- **Multiple Output Types**: Creates file documentation, design documents, and user guides
- **Incremental Processing**: Only processes changed files to save time and API costs
- **Cleanup Operations**: Remove orphaned documentation for deleted source files
- **Multi-Provider Support**: Works with OpenAI, Anthropic, and Azure OpenAI
- **Configurable Pipeline**: Highly customizable through YAML configuration

### MCP Server Integration
- **AI Assistant Integration**: Provides MCP server for seamless AI assistant interaction
- **Intelligent File Discovery**: AI-powered relevant file finding based on natural language descriptions
- **Feature Understanding**: Deep feature analysis and documentation retrieval
- **VS Code Integration**: Built-in tasks and configurations for VS Code development
- **Claude Desktop Support**: Direct integration with Claude Desktop and other MCP-compatible tools

### Interface Options
- **CLI Interface**: Comprehensive command-line interface with subcommands
- **MCP Server**: Standards-compliant Model Context Protocol server
- **API Endpoints**: RESTful API for programmatic access

## Quick Start

### Installation

#### Windows
```powershell
# Run the installation script
.\install.ps1
```

#### Mac/Linux
```bash
# Run the installation script
chmod +x install.sh
./install.sh
```

#### Manual Installation
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

1. **Set up API keys** - Create a `.env` file with your API credentials:
```env
OPENAI_API_KEY=sk-your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
# For Azure OpenAI:
AZURE_OPENAI_API_KEY=your-azure-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=your-deployment
```

2. **Configure the pipeline** - Edit `config.yaml` to match your needs:
```yaml
model:
  provider: "openai"  # or "anthropic", "azure_openai"
  name: "gpt-4"
  temperature: 0.2

file_processing:
  supported_extensions:
    - .py
    - .js
    - .ts
    - .java
    # Add more as needed

```

3. **Validate configuration**:
```bash
python main.py validate-config
```

## Usage

### Documentation Generation

The toolkit supports both subcommand and direct argument syntax for backward compatibility.

#### Subcommand Syntax (Recommended)

Generate all documentation types:
```bash
python main.py generate --repo-path /path/to/your/repo --file-docs --design-docs --guide
```

Generate specific documentation types:
```bash
# File documentation only
python main.py generate --repo-path /path/to/your/repo --file-docs

# Design documents only
python main.py generate --repo-path /path/to/your/repo --design-docs

# Documentation guide only
python main.py generate --repo-path /path/to/your/repo --guide

# Force full guide regeneration (disable incremental updates)
python main.py generate --repo-path /path/to/your/repo --guide --force-full-guide

# Clean up orphaned documentation files
python main.py generate --repo-path /path/to/your/repo --cleanup
```

#### Direct Syntax (Backward Compatible)
```bash
# Generate all documentation types
python main.py --repo-path /path/to/your/repo --file-docs --design-docs --guide

# File documentation only
python main.py --repo-path /path/to/your/repo --file-docs
```

### Repository Analysis

Analyze repository structure without generating documentation:
```bash
python main.py analyze /path/to/your/repo
```

### Configuration Validation

Validate your configuration and API keys:
```bash
python main.py validate-config
```

### MCP Server

Start the MCP server for AI assistant integration:
```bash
# Point to a specific repository
python mcp_server.py /path/to/your/repository

# Use environment variable
export DOCUMENTATION_REPO_PATH=/path/to/your/repository
python mcp_server.py

# Use current directory (default)
cd /path/to/your/repository
python mcp_server.py
```

For detailed MCP server setup and integration instructions, see [MCP_README.md](MCP_README.md).

### Command Line Options

#### Generate Command Options

| Option | Short | Description |
|--------|-------|-------------|
| `--repo-path` | `-r` | Path to the code repository (required) |
| `--docs-path` | `-d` | Path to existing documentation for context |
| `--output-path` | `-o` | Where to save generated documentation |
| `--config` | `-c` | Path to configuration file (default: config.yaml) |
| `--file-docs` | `-f` | Generate individual file documentation |
| `--design-docs` | `-D` | Generate design documentation |
| `--guide` | `-g` | Generate documentation guide |
| `--force-full-guide` | | Force full guide regeneration (disable incremental updates) |
| `--cleanup` | | Clean up orphaned documentation files for deleted source files |
| `--verbose` | `-v` | Enable verbose output |

#### Analyze Command Options

| Option | Description |
|--------|-------------|
| `repo_path` | Path to repository to analyze (positional argument) |
| `--config` | Configuration file (default: config.yaml) |

#### Validate Config Options

| Option | Description |
|--------|-------------|
| `--config` | Configuration file to validate (default: config.yaml) |

### Examples

```bash
# Full documentation generation with custom output path
python main.py generate -r ./my-project -o ./docs -f -D -g

# Quick file documentation only
python main.py generate -r ./my-project -f

# Analyze repository structure
python main.py analyze ./my-project

# Use existing docs as context
python main.py generate -r ./my-project -d ./existing-docs -f -g

# Clean up orphaned documentation
python main.py generate -r ./my-project --cleanup

# Validate configuration
python main.py validate-config --config custom-config.yaml

# Start MCP server for AI assistant integration
python mcp_server.py ./my-project
```

## Output Structure

The toolkit generates organized documentation in your specified output directory:

```
documentation_output/
├── design_documentation/ <-- Design documentation generated when using `--design-docs`
│   ├── architecture.md
│   ├── design.md
│   ├── project_overview.md
│   └── user_guide.md
├── src/ <-- File documentation generated when using `--file-docs` (path may vary)
│   ├── config_documentation.md
│   ├── pipeline_documentation.md
│   └── ...
├── documentation_guide.md <-- Documentation guide generated when using `--guide`
└── documentation_report.md <-- Documentation generation report
```

### Output Types

- **File Documentation**: Individual Markdown files for each source file with purpose, functionality, components, dependencies, and usage examples
- **Design Documents**: High-level architecture, design principles, and system overview documents
- **Documentation Guide**: Consolidated guide with navigation, summaries, and cross-references
- **Reports**: Summary reports with metrics, status, and error information

## MCP Server Integration

The toolkit includes a built-in Model Context Protocol (MCP) server that enables seamless integration with AI assistants like Claude Desktop, VS Code extensions, and other MCP-compatible tools.

### MCP Server Features

- **Intelligent File Discovery**: Find relevant files using natural language descriptions
- **Feature Understanding**: Get detailed explanations of specific features or functionality
- **Real-time Repository Analysis**: AI-powered analysis of your codebase
- **IDE Integration**: Built-in VS Code tasks and configurations

### Quick MCP Setup

1. **Generate documentation for your repository**:
   ```bash
   python main.py generate --repo-path /path/to/your/repo --guide
   ```

2. **Start the MCP server**:
   ```bash
   python mcp_server.py /path/to/your/repo
   ```

3. **Integrate with Claude Desktop** by adding to your configuration:
   ```json
   {
     "mcpServers": {
       "documentation-server": {
         "command": "python",
         "args": ["/path/to/code-documentor/mcp_server.py", "/path/to/your/repo"],
         "cwd": "/path/to/code-documentor"
       }
     }
   }
   ```

For comprehensive MCP server setup instructions, including VS Code integration, troubleshooting, and advanced configurations, see [MCP_README.md](MCP_README.md).

### VS Code Integration

The toolkit includes pre-configured VS Code tasks for easy development and MCP server management:

#### Available Tasks

- **"Start Documentation MCP Server"**: Launches the MCP server using the workspace virtual environment
- **"Install MCP Dependencies"**: Installs required dependencies from requirements.txt

#### Using VS Code Tasks

1. Open the project in VS Code
2. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS)
3. Type "Tasks: Run Task"
4. Select the desired task from the list

The tasks are configured to use the proper Python environment and working directory automatically.

### Available MCP Tools

- **`get_relevant_files`**: Find files relevant to a natural language description
- **`understand_feature`**: Get documentation about specific features or functionality

## Configuration

The toolkit is highly configurable through `config.yaml`. Key configuration sections:

### Model Configuration
```yaml
model:
  provider: "openai"  # openai, anthropic, azure_openai
  name: "gpt-4"
  temperature: 0.2
  max_tokens: 32000
```

### File Processing
```yaml
file_processing:
  supported_extensions: [.py, .js, .ts, .java, .cpp, .c, .cs, .go, .rs, .php, .rb, .swift, .kt]
  exclude_patterns: ["__pycache__", "node_modules", ".git", "*.pyc", "dist", "build", "venv"]
```

### Design Documents
```yaml
design_docs:
  enabled: true
  documents:
    project_overview:
      enabled: true
    architecture:
      enabled: true
    design:
      enabled: true
    user_guide:
      enabled: true
```

### Processing Limits
```yaml
processing:
  max_files: 100  # Limit number of files processed
  save_incrementally: true  # Save files as they're processed

token_limits:
  max_context_tokens: 50000
  summarization_threshold: 50000
  chunk_size: 10000
```

## Advanced Features

### Incremental Processing
The toolkit automatically detects file changes and only processes modified files, saving time and API costs. To force a full rebuild:
- Delete the output directory, or
- Use the `--force-full-guide` flag for guide regeneration

### Documentation Cleanup
Automatically removes orphaned documentation files when source files are deleted:
```bash
python main.py generate --repo-path /path/to/your/repo --cleanup
```

### Token Management
Automatically handles large files by:
- Chunking oversized content
- Summarizing existing documentation when it exceeds token limits
- Managing context windows for different LLM providers

### Multiple LLM Providers
Supports switching between providers by changing the configuration:
- **OpenAI**: GPT-4, GPT-3.5-turbo, GPT-4-turbo
- **Anthropic**: Claude 3 models (Opus, Sonnet, Haiku)
- **Azure OpenAI**: Enterprise-grade OpenAI models

### MCP Server Integration
- **Standards Compliant**: Follows Model Context Protocol specifications
- **AI Assistant Ready**: Works with Claude Desktop, VS Code, and other MCP clients
- **Real-time Analysis**: Live repository analysis through AI assistant interactions
- **Tool-based Interaction**: Structured API for AI assistant tool use

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Invalid API key error | Check your `.env` file and API key validity |
| No documentation generated | Verify `file_extensions` and `exclude_patterns` in config |
| Truncated documentation | Normal behavior - toolkit auto-chunks and continues |
| High API costs | Use incremental mode, exclude unnecessary files |
| Configuration errors | Run `python main.py validate-config` |
| MCP server connection issues | Ensure documentation guide exists, check repository path |
| "ModuleNotFoundError: No module named 'mcp'" | Install MCP dependencies: `pip install mcp>=1.2.0` |
| MCP tools not responding | Verify repository has `documentation_output/documentation_guide.md` |
| VS Code task failures | Check virtual environment activation and file paths |

### Getting Help

```bash
# General help
python main.py --help

# Command-specific help
python main.py generate --help
python main.py analyze --help
python main.py validate-config --help

# Verbose output for debugging
python main.py generate --repo-path ./my-project --file-docs --verbose

# MCP server help
python mcp_server.py --help
```

## Contributing

We welcome contributions to improve the toolkit! Here's how to get started:

### Development Setup

1. **Fork and clone the repository**
2. **Set up development environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure for development**:
   - Copy `.env.example` to `.env` and add your API keys
   - Review and modify `config.yaml` as needed

### Development Guidelines

- **Code Style**: Follow PEP 8 for Python code
- **Testing**: Test your changes with different repository types and configurations
- **Documentation**: Update documentation for any new features
- **Modular Design**: Keep components loosely coupled and highly cohesive

### Areas for Contribution

- **Token Efficiency**: Needs more efficient use of tokens- such as collecting and caching document summaries with the individual documents, rather than regenerating them every time we create the guide
- **New LLM Providers**: Add support for additional AI providers, especially local models
- **Output Formats**: Support for additional output formats beyond Markdown
- **Templates**: Custom documentation templates and styles
- **Integration**: CI/CD integrations and automation tools
- **Performance**: Optimization for large codebases
- **MCP Extensions**: Additional MCP tools and capabilities
- **IDE Plugins**: Enhanced IDE integrations beyond VS Code

### Submitting Changes

1. Create a feature branch from `main`
2. Make your changes with appropriate tests
3. Update documentation as needed
4. Submit a pull request with a clear description

### Code Architecture

The toolkit follows a modular pipeline architecture:

#### Core Components
- **`main.py`**: CLI entry point and command routing with subcommand support
- **`mcp_server.py`**: Model Context Protocol server for AI assistant integration
- **`src/config.py`**: Configuration management and validation
- **`src/pipeline.py`**: Main orchestration and workflow management using LangGraph
- **`src/code_analyzer.py`**: Repository scanning and file analysis
- **`src/document_processor.py`**: Document loading and processing
- **`src/llm_manager.py`**: Multi-provider LLM abstraction and management
- **`src/design_document_generator.py`**: Design document generation
- **`src/guide_generator.py`**: Documentation guide assembly with incremental updates
- **`src/models.py`**: Pydantic data models and schemas

#### MCP Integration
- **`src/mcp_manager.py`**: MCP server orchestration and tool management
- **`src/mcp_models.py`**: MCP-specific data models and state management
- **LangGraph Workflows**: State-based tool execution for AI assistant interactions

#### Supporting Modules
- **`src/state_manager.py`**: Pipeline state and incremental build management
- **`src/context_manager.py`**: Token management and context optimization
- **`src/file_processor.py`**: File processing and metadata management
- **`src/report_generator.py`**: Documentation reporting and metrics

For detailed architecture information, see the generated design documentation in `documentation_output/design_documentation/`.

## License

This project is licensed under the GPL-3 License - see the LICENSE file for details.

## Support

For issues, questions, or feature requests:
1. Check the troubleshooting section above
2. Review existing issues in the repository
3. Create a new issue with detailed information about your problem
4. Include configuration, error messages, and steps to reproduce

---

**Happy documenting!** 🚀📚