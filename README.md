# Documentation Pipeline with LangGraph

An intelligent documentation pipeline that uses LangGraph to automatically generate comprehensive documentation for code repositories.

## Features

- **Intelligent Documentation Generation**: Uses AI models to create detailed documentation for each code file
- **Context-Aware Processing**: Leverages existing documentation as context for better results
- **Token Management**: Automatically summarizes large documentation sets to fit within token limits
- **Multi-Model Support**: Configurable AI models (OpenAI GPT, Anthropic Claude, etc.)
- **Side-by-Side Output**: Generates markdown documentation alongside original code files

## Installation

1. Clone or navigate to this repository
2. Run the setup script:
   ```bash
   python setup.py
   ```
3. Edit `.env` file and add your API keys:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```

## Usage

### Quick Start
```bash
# Setup
python setup.py

# Test configuration  
python main.py validate-config

# Generate documentation
python main.py --repo-path /path/to/repository
```

### Advanced Usage
```bash
# With existing documentation context
python main.py --repo-path /path/to/repo --docs-path /path/to/existing/docs

# Custom output location
python main.py --repo-path /path/to/repo --output-path /path/to/output

# Analyze repository structure
python main.py analyze /path/to/repo

# Run examples
python example.py
```

### Configuration Options
Edit `config.yaml` to configure:
- AI model settings (OpenAI GPT, Anthropic Claude, Azure OpenAI)
- Token limits and processing options
- Supported file types and exclusion patterns  
- Output formatting and templates

For detailed usage instructions, see [USAGE.md](USAGE.md).

## Project Structure

```
documentor/
├── main.py                     # CLI entry point
├── setup.py                   # Setup script
├── example.py                  # Usage examples
├── config.yaml                # Configuration file
├── requirements.txt           # Python dependencies
├── .env.example              # Environment template
├── .gitignore               # Git ignore rules
├── README.md                # This file
├── USAGE.md                 # Detailed usage guide
└── src/                     # Source code
    ├── __init__.py
    ├── config.py            # Configuration management
    ├── pipeline.py          # Main LangGraph pipeline
    ├── document_processor.py # Document processing utilities
    ├── code_analyzer.py     # Code analysis utilities
    └── models.py            # Pydantic data models
```

## License

MIT License
