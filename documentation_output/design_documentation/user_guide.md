<!-- AUTO-GENERATED DESIGN DOCUMENT -->
<!-- Generated on: 2025-07-01T23:11:11.678174 -->
<!-- Document: user_guide -->

# Documentation MCP Server Toolkit – User Guide

## Introduction

Welcome to the **Documentation MCP Server Toolkit**! This user guide is your comprehensive companion to installing, configuring, and operating the toolkit for AI-powered documentation automation. Whether you're a developer aiming to streamline your code documentation, a technical writer seeking robust automation, or an AI assistant user looking to interact with repository artifacts, you'll find clear, practical steps here. The guide walks through initial setup, basic and advanced workflows, common troubleshooting tips, and best practices to ensure you can generate, maintain, and query technical documentation with confidence and efficiency.

Let’s get started—by the end of this guide, you’ll be equipped to generate and manage rich documentation for your projects using the capabilities provided by the Documentation MCP Server Toolkit.

---

## Getting Started

This section will guide you through installation, initial configuration, basic usage, and common first steps to begin automating and exploring your software documentation with AI.

### 1. Installation

#### Prerequisites

Before installing, ensure you have the following:
- **Python 3.8+** (Python 3.10 or later recommended)
- **Git** (for repository cloning)
- An API key for your chosen LLM provider (OpenAI, Anthropic, or Azure OpenAI)
- **VS Code** (optional, for IDE integration)

#### Clone the Repository

Start by cloning the toolkit to your local environment:

```bash
git clone https://github.com/your-org/code-documentor.git
cd code-documentor
```

#### Set Up a Python Virtual Environment

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

#### Install Dependencies

```bash
pip install -r requirements.txt
```

This will pull in all necessary libraries, including those for LLM connectivity and project automation.

---

### 2. Initial Setup & Configuration

#### LLM Provider Setup

Obtain an API key for your chosen LLM:
- **OpenAI:** [Get an API key](https://platform.openai.com/account/api-keys)
- **Anthropic:** [Request access](https://www.anthropic.com/)
- **Azure OpenAI:** Create resources and retrieve keys via Azure Portal

#### Configure Environment Variables

Set your API key as an environment variable (recommended for security):

```bash
export OPENAI_API_KEY="your-openai-key"
```

Configure other variables according to your setup as documented in `src/config.py`.

#### Review and Edit Configuration (Optional)

`config.yaml` defines operational settings such as:
- LLM provider and model (e.g., 'gpt-4', 'claude-3')
- File inclusion/exclusion patterns
- Guide and documentation output behavior

Default settings suffice for most; customize for large projects or specific needs.

Example excerpt:
```yaml
llm:
  provider: openai
  model: gpt-4
  api_key_env: OPENAI_API_KEY
doc:
  include:
    - src/**/*.py
  exclude:
    - tests/*
```

---

### 3. Basic Usage Examples

Perform common documentation operations with these commands:

#### Generate Documentation and Guide

```bash
python main.py generate --repo-path /path/to/your/repository --guide
```
- Scans the codebase, generates Markdown docs, and builds a comprehensive `documentation_guide.md`.

##### Incremental Generation

Subsequent runs update only changed or new files:

```bash
python main.py generate --repo-path /path/to/your/repository --guide
```

##### Include Design Documentation

Generate a design doc alongside:

```bash
python main.py generate --repo-path /path/to/your/repository --guide --design
```

#### Clean Up Orphaned Docs

Remove documentation for deleted/moved files:

```bash
python main.py generate --repo-path /path/to/your/repository --cleanup
```

#### Analyze Repository Structure

Preview which files will be included in documentation:

```bash
python main.py analyze --repo-path /path/to/your/repository
```

#### Validate Configuration

Check for configuration or environment errors:

```bash
python main.py validate --repo-path /path/to/your/repository
```

---

### 4. Using the Documentation MCP Server

To access AI-powered endpoints for file discovery and queries, start the MCP Server:

```bash
python mcp_server.py /path/to/your/repository
```

**Alternative method using environment variable:**
```bash
export DOCUMENTATION_REPO_PATH=/path/to/your/repository
python mcp_server.py
```

**Integrate with VS Code:**
- Install the extension (if available).
- Add a suitable configuration to `.vscode/settings.json` or `.vscode/tasks.json` as shown in the previous section for one-click operations.

---

### 5. Common First Tasks

- **Generate docs for a fresh repo:**
  ```bash
  python main.py generate --repo-path /path/to/your/repository --guide
  ```
- **Clean up after code changes:**
  ```bash
  python main.py generate --repo-path /path/to/your/repository --cleanup
  ```
- **Integrate with VS Code for streamlined workflow.**
- **Use the MCP Inspector tool for interactive server exploration.**

---

### 6. Troubleshooting & Next Steps

- **Dependency Errors:** Ensure your virtual environment is active and all dependencies are installed.
- **LLM API Issues:** Double-check API keys, provider choice, and quota.
- **Missing Files or Docs:** Run the generator and validate configuration.
- **For advanced tasks and integration, refer to the full user guide or project README.md.**

With this foundation, you're ready to fully leverage automated, AI-augmented documentation in your workflow.

---

## User Workflows

Efficient documentation depends on well-defined workflows. This section outlines step-by-step processes and best practices for typical usage scenarios with the Documentation MCP Server Toolkit.

### 1. Generating Documentation for a Repository

**Goal:** Produce file-level documentation and a comprehensive project guide—or even a design doc—with minimal effort.

#### Steps:

1. **Prepare Environment** — Confirm Python, dependencies, and LLM credentials.
2. **Generate Docs**:
   ```bash
   python main.py generate --repo-path /path/to/your/repository --guide
   ```
   Optionally, add `--design` to include a design document.

3. **Review Outputs** in `documentation_output/`.

**Troubleshooting tips** are included for common errors such as missing output or LLM API issues.

---

### 2. Incremental Documentation & Updates

Keep documentation current without reprocessing all files:

1. **Modify or add source files** as usual.
2. **Regenerate documentation**; only changed files and the guide are updated:
   ```bash
   python main.py generate --repo-path /path/to/repository --guide
   ```

**Best Practice:** Commit docs before and after regeneration for traceability.

---

### 3. Cleaning Up Orphaned Documentation

Remove docs for files no longer present:

1. **Remove files** from your repo.
2. **Run cleanup:**
   ```bash
   python main.py generate --repo-path /path/to/repository --cleanup
   ```

---

### 4. Analyzing Repository Structure

Preview and verify which files will be documented:

```bash
python main.py analyze --repo-path /path/to/repository
```

Confirm config patterns cover the relevant files before generating docs.

---

### 5. Validating Configuration

Catch issues before a big documentation run:

```bash
python main.py validate --repo-path /path/to/repository
```

This checks API credentials, file patterns, and integration settings.

---

### 6. Using the Documentation MCP Server (Interactive & AI Queries)

Deploy the backend server to enable smart file and feature queries:

```bash
python mcp_server.py /path/to/your/repository
```

Try MCP CLI tools or integrate with editors and desktop AI tools for natural language documentation search and discovery.

---

### 7. Common Troubleshooting Scenarios

A table is provided for rapid issue diagnosis and solution referencing, covering module errors, integration pitfalls, API issues, and permission conflicts.

---

### 8. Best Practices

- **Run incrementally:** After source changes, especially merges or refactors.
- **Version documentation:** Keep generated docs in source control.
- **Secure credentials:** Use environment variables, never hardcode!
- **Automate tasks:** Use scripts or IDE tasks for reliability and speed.

---

### 9. Example Workflow: First Run to AI Query

1. Clone your repo.
2. Set environment and install dependencies.
3. (Optional) Edit `config.yaml`.
4. Generate documentation:
   ```bash
   python main.py generate --repo-path . --guide
   ```
5. Clean up old documentation:
   ```bash
   python main.py generate --repo-path . --cleanup
   ```
6. Start the server for AI/IDE integration:
   ```bash
   python mcp_server.py .
   ```
7. Query via CLI/editor for features or relevant files.

**Result:** Up-to-date, queryable documentation, ready for developer and AI assistant use.

---

## Conclusion

With the Documentation MCP Server Toolkit, you can rapidly deploy and maintain automated, high-quality documentation pipelines tailored for both human readers and AI agents. By following the workflows and best practices outlined in this guide, your projects gain reliable, discoverable, and always-current documentation with minimal manual effort.

For further reference, consult the [Implementation Details](#implementation-details), [Troubleshooting](#troubleshooting), or browse the project’s README.md.

Start automating your documentation process today, and unlock new levels of productivity and insight for your development teams and toolchains!