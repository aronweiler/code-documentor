<!-- AUTO-GENERATED DESIGN DOCUMENT -->
<!-- Generated on: 2025-06-11T11:00:35.961492 -->
<!-- Document: user_guide -->

# Automated Documentation Generation Toolkit: User Guide

---

## Introduction

Welcome to the **Automated Documentation Generation Toolkit User Guide**. This comprehensive guide is designed to help you seamlessly set up, configure, and operate the toolkit for automating code documentation in your projects. Whether you're adopting documentation automation for the first time or fine-tuning its integration within your team, this guide walks you through the essentials, advanced workflows, troubleshooting, and best practices to ensure high-quality, maintainable documentation with minimal effort. 

The guide is structured in two main parts:
1. **Getting Started** – Step-by-step setup, configuration, and first-time usage instructions.
2. **User Workflows** – Detailed workflows and advanced operations for ongoing documentation management.

Let’s begin by installing and setting up the toolkit.

---

## Getting Started

This Getting Started guide will walk you through installing the Automated Documentation Generation Toolkit, configuring it for your codebase, and running your first documentation pipeline. Whether you're automating docs for the first time or evaluating integration with your team's workflow, this section provides the essential steps and common first tasks.

### 1. Installation

#### Requirements

- **Python 3.9+** (recommended: 3.10 or higher)
- **pip** (Python package manager)
- **Internet connection** (required for LLM API access)
- **Unix/MacOS/Windows** environments supported

#### Step-by-Step Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/aronweiler/code-documentor.git
   cd code-documentor
   ```

2. **(Optional) Create a Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate        # On Windows: venv\Scripts\activate
   ```

3. **Install Python Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   > _Note: Requirements include OpenAI, Anthropic, tiktoken, pyyaml, python-dotenv, pydantic, and others._

---

### 2. Initial Setup & Configuration

#### Prepare Your API Keys

Obtain API keys for your preferred LLM provider(s):

- Sign up with [OpenAI](https://platform.openai.com/), [Anthropic](https://console.anthropic.com/), or Azure OpenAI.
- Copy your API keys; you’ll need them for the next step.

#### Configure with `.env` and `config.yaml`

1. **Create a `.env` File:**

   In the project root, add your secret keys, for example:
   ```
   OPENAI_API_KEY=sk-...
   ANTHROPIC_API_KEY=your-anthropic-key
   # If using Azure OpenAI:
   AZURE_OPENAI_API_KEY=azure-key
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_DEPLOYMENT=your-deployment
   ```
   > _Only the relevant keys for your chosen provider are required._

2. **Configure `config.yaml`:**

   Copy the provided template to configure your project settings:
   ```bash
   cp config.example.yaml config.yaml
   ```
   Edit `config.yaml` to match your repository and LLM usage. Example:
   ```yaml
   repo_path: ./my_project
   llm_provider: openai
   llm_model: gpt-4-1106-preview
   output_dir: ./docs_output
   file_extensions: [.py, .js, .ts]
   exclude_dirs: [venv, tests]
   documentation_guide:
     enabled: true
   design_document:
     enabled: true
   ```
   > _For detailed config options, refer to the comments in `config.example.yaml` or see the [Configuration Reference](config_documentation.md)._

3. **(Optional) Validate Your Configuration:**
   ```bash
   python main.py validate-config
   ```
   This checks for required fields and API access, ensuring your setup is ready.

---

### 3. Basic Usage Examples

Now that your toolkit is configured, you’re ready to generate project documentation and analyze your repository:

#### Generate Documentation for Your Repository

Run the toolkit’s main documentation generation command:
```bash
python main.py generate
```

- All steps—repository scan, file-level doc generation, design doc/guide, and summary report—are handled automatically.
- Results appear under the `output_dir` you set in config (e.g., `./documentation_output/`).
- If you rerun the command, only changed or new files will be (re)documented by default.

#### Analyze Repository Structure

Optionally, to get a summary of your codebase before generating docs:
```bash
python main.py analyze
```
This prints a report of file counts, types, and directory breakdowns.

---

### 4. Common First Tasks

Get the most out of the toolkit by leveraging its automation and customization features:

- **Document Only Changed Files (Incremental Mode):**  
  By default, the toolkit skips unchanged files to save time and API costs. To force re-documentation, clear the metadata or output directory.

- **Generate a Project Documentation Guide:**  
  Enabled via `documentation_guide: enabled: true`. After the pipeline runs, find `documentation_guide.md` in your output directory for high-level summaries and navigation.

- **Create a Design Document:**  
  When `design_document: enabled: true` is set, the toolkit generates an LLM-based design/architecture markdown document, ideal for onboarding and codebase reviews.

- **Review Output and Reports:**  
  Explore per-file Markdown docs, consolidated guides and design docs, and summary reports for coverage and error diagnostics.

---

### 5. Troubleshooting and Tips

- _Invalid API Keys_: Double-check your `.env` configuration.
- _Missing Dependencies_: Rerun `pip install -r requirements.txt`.
- _Large Files/Summaries_: The toolkit chunks or summarizes as needed; review reports for warnings or truncation.
- **Verbose Mode:** Use `--verbose` for detailed logs.
- **Help Menu:**  
  ```bash
  python main.py --help
  python main.py generate --help
  ```

---

### 6. Next Steps

- Customize prompts, code scanning rules, or output templates to fit your standards.
- Integrate with CI/CD pipelines for continuous, automatic documentation updates.
- Experiment with advanced configuration for new LLM providers or documentation templates.

---

You are now prepared to automate documentation across your codebase with confidence! To dive deeper into advanced features and configuration options, consult the `/docs` directory or [Documentation Guide](documentation_guide.md).

---

## User Workflows

Having set up the toolkit, you’re ready to dive into common workflows. This section provides actionable, step-by-step instructions for using the toolkit effectively, addressing typical scenarios, troubleshooting, and extending functionality.

---

### 1. Generating Documentation for a Codebase

To generate documentation for your project:

1. **Ensure Initial Setup**
   - Complete the [Getting Started](#getting_started) steps.
2. **Validate Configuration (Optional)**
   - Run `python main.py validate-config` to check connectivity and settings.
3. **Run the Documentation Generator**
   - Execute `python main.py generate`.
   - The process analyzes your repo, generates LLM-based docs, and outputs Markdown files, a design document, a documentation guide (if enabled), and a summary report.
4. **Check the Output**
   - Outputs are organized within your `output_dir`, e.g.:
     ```
     documentation_output/
     ├── src/
     │   ├── code_analyzer_documentation.md
     │   └── ...
     ├── documentation_guide.md
     ├── design_document.md
     └── documentation_report.md
     ```
**Best Practices:** Commit config and output docs to version control and schedule regular CI/CD runs.

---

### 2. Incremental Documentation Updates

The toolkit records metadata to detect changes, ensuring only new or modified files are (re)documented, thereby saving time and API usage.

**How To:**
- Edit/add source files as normal.
- Rerun `python main.py generate`. Only changed/new files are processed.
- Review the summary report for a breakdown of processed files.
- _To force a full rebuild, clear the output directory or delete hash metadata._

---

### 3. Reviewing and Using Generated Documentation

- Outputs (Markdown docs, guides, reports) are found in your chosen output directory, mirroring your source structure.
- The documentation guide provides an indexed summary for easy navigation.
- The design document is ideal for architecture review and team onboarding.

**Tip:** Import Markdown outputs into wiki/collaboration tools for wider team access.

---

### 4. Customizing the Pipeline and Configuration

To tailor the documentation process:

- Edit `config.yaml` for LLM settings, output paths, file types, and generation options.
- Adjust `.env` to switch LLM providers or set credentials as your needs change.
- After updating settings, rerun the generator for updated output.

**Sample Configuration Snippet:**
```yaml
file_extensions: [.py, .js]
exclude_dirs: [venv, tests]
documentation_guide:
  enabled: true
design_document:
  enabled: false
```

_Best practice: test configuration changes on a small subset first._

---

### 5. Repository Analysis Without Documentation Generation

For a quick audit of your codebase’s structure, use:

```bash
python main.py analyze
```
This produces a summary of file counts, types, and directory breakdowns. No documentation is generated or altered.

---

### 6. Troubleshooting and Common Issues

| Symptom                        | Solution                                                            |
|---------------------------------|---------------------------------------------------------------------|
| Invalid API key/error           | Check `.env` for correct keys and provider access                   |
| No docs generated for some files| Check `exclude_dirs` and `file_extensions` in `config.yaml`         |
| Documentation is truncated      | Toolkit auto-chunks/continues output; check reports for warnings    |
| Excessive API usage/cost        | Use incremental runs, exclude 3rd-party/large files                 |
| CLI errors with config          | Run `python main.py validate-config` to identify issues             |
| Changed files not documented    | Ensure hash metadata and outputs are not stale; clear if necessary  |

More detailed solutions and advice are available in the documentation guide.

---

### 7. Best Practices

- Integrate doc generation with your CI for up-to-date documentation.
- Regularly review summary reports for errors or skipped files.
- Securely handle credentials, especially in CI environments.
- Exclude non-essential directories to avoid unnecessary costs and clutter.
- Advanced users: tailor prompt templates in `src/prompts/` for custom documentation styles.

---

### 8. Advanced Usage

- **Force a Full Rebuild:**  
  Remove the output directory and rerun the generator:
  ```bash
  rm -rf documentation_output/
  python main.py generate
  ```
- **Verbose Output:**  
  Add `--verbose` to commands for deeper debugging.
  ```bash
  python main.py generate --verbose
  ```
- **Selective Documentation:**  
  Limit file extensions or directories in your config to target specific project sections.

---

### 9. Example: End-to-End Workflow

1. Clone the repository and install dependencies.
2. Configure `.env` with API keys.
3. Copy and edit `config.yaml`.
4. Run `python main.py validate-config`.
5. Run `python main.py generate`.
6. Review generated documentation in `documentation_output/`.
7. Address issues and iterate as needed.

---

### 10. Getting Help

- Use `python main.py --help` for CLI options and usage.
- Check generated reports for feedback and diagnostics.
- Refer to the [Documentation Guide](documentation_guide.md) or the project README for additional details and advanced usage.
- For unresolved issues, consider raising an issue in the project repository.

---

## Conclusion

By following this guide, you are equipped to automate, review, and maintain robust documentation for your codebase—streamlining onboarding, audits, and ongoing development. For more advanced configurations, troubleshooting, or customization, consult the documentation guide or explore files under `/docs`. 

With the Automated Documentation Generation Toolkit, high-quality documentation is always within reach. Happy documenting!