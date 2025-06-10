# Usage Guide - Documentation Pipeline

This guide walks you through setting up and using the Documentation Pipeline to automatically generate comprehensive documentation for your code repositories.

## Quick Start

### 1. Setup

First, set up the environment:

```powershell
# Create and activate a virtual environment (recommended)
python -m venv venv
venv\Scripts\activate

# Install dependencies
python setup.py
```

### 2. Configure API Keys

Edit the `.env` file and add your API keys:

```env
# For OpenAI (default)
OPENAI_API_KEY=sk-your-openai-api-key-here

# For Anthropic Claude (alternative)
ANTHROPIC_API_KEY=your-anthropic-api-key-here
```

### 3. Test Configuration

```powershell
python main.py validate-config
```

### 4. Generate Documentation

```powershell
# Basic usage - document a repository
python main.py --repo-path "C:\path\to\your\repository"

# With existing documentation as context
python main.py --repo-path "C:\path\to\repo" --docs-path "C:\path\to\existing\docs"

# Specify output location
python main.py --repo-path "C:\path\to\repo" --output-path "C:\path\to\output"
```

## Detailed Usage

### Command Line Options

```powershell
python main.py --help
```

**Required:**
- `--repo-path`: Path to the code repository to document

**Optional:**
- `--docs-path`: Path to existing documentation (used as context)
- `--output-path`: Where to save generated documentation (default: repo-path/documentation_output)
- `--config`: Path to configuration file (default: config.yaml)
- `--verbose, -v`: Enable verbose output

### Configuration Options

Edit `config.yaml` to customize the pipeline:

#### AI Model Settings
```yaml
model:
  provider: "openai"  # openai, anthropic, azure_openai
  name: "gpt-4o"       # Model name
  temperature: 0.2    # Creativity level (0.0-1.0)
  max_tokens: 4000    # Maximum response length
```

#### Token Management
```yaml
token_limits:
  max_context_tokens: 8000        # Max tokens for existing docs
  summarization_threshold: 6000   # When to summarize
  chunk_size: 2000               # Chunk size for processing
```

#### File Processing
```yaml
file_processing:
  supported_extensions:           # File types to document
    - .py
    - .js
    - .ts
    # ... add more as needed
  exclude_patterns:              # Patterns to exclude
    - "__pycache__"
    - "node_modules"
    - ".git"
```

### Examples

#### Example 1: Document a Python Project
```powershell
# Navigate to your project directory
cd "C:\MyProjects\my-python-app"

# Generate documentation
python "C:\Repos\documentor\main.py" --repo-path "." --verbose
```

#### Example 2: Use Existing Documentation as Context
```powershell
python main.py ^
  --repo-path "C:\MyProjects\web-app" ^
  --docs-path "C:\MyProjects\web-app\docs" ^
  --output-path "C:\Generated-Docs\web-app"
```

#### Example 3: Use Different AI Model
Edit `config.yaml`:
```yaml
model:
  provider: "anthropic"
  name: "claude-3-sonnet-20240229"
  temperature: 0.1
```

Then run:
```powershell
python main.py --repo-path "C:\path\to\repo"
```

## Utility Commands

### Analyze Repository Structure
```powershell
python main.py analyze "C:\path\to\repository"
```

This shows:
- Total files found
- Files by extension
- Files by directory
- Largest files

### Validate Configuration
```powershell
python main.py validate-config
```

Checks:
- Configuration file syntax
- API key availability
- Model settings

### Run Examples
```powershell
python example.py
```

Demonstrates:
- Repository analysis
- Document processing
- Token counting

## Output Structure

The pipeline generates:

```
documentation_output/
├── src/
│   ├── main_documentation.md
│   ├── config_documentation.md
│   └── ...
├── tests/
│   └── ...
└── documentation_report.md
```

Each documentation file includes:
- **Purpose**: What the file does
- **Functionality**: Detailed explanation
- **Key Components**: Important elements
- **Dependencies**: What it depends on
- **Usage Examples**: How to use it
- **Original Code**: (if enabled)

## Troubleshooting

### Common Issues

#### 1. API Key Errors
```
❌ API key not found for openai
```
**Solution**: Check your `.env` file has the correct API key.

#### 2. Configuration Errors
```
❌ Configuration error: model section missing
```
**Solution**: Ensure `config.yaml` is properly formatted.

#### 3. Large Documentation Context
The pipeline automatically summarizes large existing documentation to fit within token limits.

#### 4. File Processing Issues
Check the `exclude_patterns` in config.yaml if files are being skipped unexpectedly.

### Getting Help

1. **Verbose Mode**: Use `--verbose` flag for detailed output
2. **Configuration Check**: Run `validate-config` command
3. **Analysis**: Use `analyze` command to see what files will be processed

## Advanced Usage

### Custom Templates

Edit the `templates` section in `config.yaml`:

```yaml
templates:
  file_documentation: |
    # Documentation for {filename}
    
    ## Custom Section
    {custom_content}
    
    ## Purpose
    {purpose}
    # ... customize as needed
```

### Multiple Models

You can run the pipeline multiple times with different configurations:

```powershell
# Generate with GPT-4o
python main.py --repo-path "C:\repo" --config config-gpt4o.yaml

# Generate with Claude
python main.py --repo-path "C:\repo" --config config-claude.yaml
```

### Batch Processing

Create a batch script to process multiple repositories:

```powershell
# batch_process.ps1
$repos = @("C:\Repos\project1", "C:\Repos\project2", "C:\Repos\project3")

foreach ($repo in $repos) {
    Write-Host "Processing $repo"
    python main.py --repo-path $repo --output-path "C:\Generated-Docs\$(Split-Path $repo -Leaf)"
}
```

## Best Practices

1. **Use Existing Documentation**: Provide existing docs for better context
2. **Review Generated Documentation**: Always review and edit as needed
3. **Iterate on Configuration**: Adjust token limits and templates based on results
4. **Version Control**: Keep generated documentation in version control
5. **Regular Updates**: Regenerate documentation when code changes significantly

## Performance Tips

- Use `--verbose` to monitor progress
- Adjust `chunk_size` for better performance with large documents
- Consider using faster models for initial drafts, then higher-quality models for final documentation
