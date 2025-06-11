# Automated Documentation Generation Toolkit

An intelligent, LLM-powered toolkit that automatically generates comprehensive documentation for codebases. This tool leverages large language models (OpenAI, Anthropic, Azure OpenAI) to create high-quality, contextual documentation including file-level docs, design documents, and consolidated guides.

## Features

- **Automated Code Analysis**: Scans repositories and analyzes code structure
- **LLM-Powered Documentation**: Generates contextual documentation using advanced AI models
- **Multiple Output Types**: Creates file documentation, design documents, and user guides
- **Incremental Processing**: Only processes changed files to save time and API costs
- **Multi-Provider Support**: Works with OpenAI, Anthropic, and Azure OpenAI
- **Configurable Pipeline**: Highly customizable through YAML configuration
- **CLI Interface**: Easy-to-use command-line interface with multiple commands

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

### Generate Documentation

#### Generate all documentation types:
```bash
python main.py generate --repo-path /path/to/your/repo --file-docs --design-docs --guide
```

#### Generate only file documentation:
```bash
python main.py generate --repo-path /path/to/your/repo --file-docs
```

#### Generate only design documents:
```bash
python main.py generate --repo-path /path/to/your/repo --design-docs
```

#### Generate only documentation guide:
```bash
python main.py generate --repo-path /path/to/your/repo --guide
```

### Analyze Repository Structure

Get insights into your codebase without generating documentation:
```bash
python main.py analyze /path/to/your/repo
```

### Command Line Options

| Option | Short | Description |
|--------|-------|-------------|
| `--repo-path` | `-r` | Path to the code repository (required) |
| `--docs-path` | `-d` | Path to existing documentation for context |
| `--output-path` | `-o` | Where to save generated documentation |
| `--config` | `-c` | Path to configuration file (default: config.yaml) |
| `--file-docs` | `-f` | Generate individual file documentation |
| `--design-docs` | `-D` | Generate design documentation |
| `--guide` | `-g` | Generate documentation guide |
| `--verbose` | `-v` | Enable verbose output |

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
- **Documentation Guide**: Consolidated guide with navigation and summaries
- **Reports**: Summary reports with metrics, status, and error information

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
The toolkit automatically detects file changes and only processes modified files, saving time and API costs. To force a full rebuild, delete the output directory.

### Token Management
Automatically handles large files by:
- Chunking oversized content
- Summarizing existing documentation when it exceeds token limits
- Managing context windows for different LLM providers

### Multiple LLM Providers
Supports switching between providers by changing the configuration:
- **OpenAI**: GPT-4, GPT-3.5-turbo
- **Anthropic**: Claude models
- **Azure OpenAI**: Enterprise-grade OpenAI models

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Invalid API key error | Check your `.env` file and API key validity |
| No documentation generated | Verify `file_extensions` and `exclude_patterns` in config |
| Truncated documentation | Normal behavior - toolkit auto-chunks and continues |
| High API costs | Use incremental mode, exclude unnecessary files |
| Configuration errors | Run `python main.py validate-config` |

### Getting Help

```bash
# General help
python main.py --help

# Command-specific help
python main.py generate --help
python main.py analyze --help

# Verbose output for debugging
python main.py generate --repo-path ./my-project --file-docs --verbose
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

- **New LLM Providers**: Add support for additional AI providers
- **Output Formats**: Support for additional output formats beyond Markdown
- **Language Support**: Enhanced support for more programming languages
- **Templates**: Custom documentation templates and styles
- **Integration**: CI/CD integrations and automation tools
- **Performance**: Optimization for large codebases

### Submitting Changes

1. Create a feature branch from `main`
2. Make your changes with appropriate tests
3. Update documentation as needed
4. Submit a pull request with a clear description

### Code Architecture

The toolkit follows a modular pipeline architecture:

- **`main.py`**: CLI entry point and command routing
- **`src/config.py`**: Configuration management and validation
- **`src/pipeline.py`**: Main orchestration and workflow management
- **`src/code_analyzer.py`**: Repository scanning and file analysis
- **`src/document_processor.py`**: Document loading and processing
- **`src/llm_manager.py`**: LLM provider abstraction and management
- **`src/design_document_generator.py`**: Design document generation
- **`src/guide_generator.py`**: Documentation guide assembly
- **`src/models.py`**: Data models and schemas

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