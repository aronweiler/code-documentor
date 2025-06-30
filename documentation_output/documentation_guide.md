# Documentation Guide

<!-- AUTO-GENERATED DOCUMENTATION GUIDE -->
<!-- This file was automatically generated and should not be manually edited -->

This guide provides an overview of all generated documentation files in this repository.
Use this guide to quickly locate relevant documentation when working on specific features or components.

**Generated on:** 2025-06-29T16:53:44.575584  
**Total documented files:** 15

## Documentation Files

### .vscode\launch.json

**Documentation:** `.vscode\launch_documentation.md`

**Summary:** The .vscode/launch.json file defines a set of Visual Studio Code debugging configurations for launching and debugging various Python command-line tasks (such as documentation generation, repository analysis, and configuration validation) via main.py. Each configuration specifies arguments, environment settings, and working directories required for specific development tasks, ensuring consistent and reproducible workflows across contributors. This setup leverages VS Code's debugger (debugpy) and allows users to select different operations directly within the IDE's Run and Debug panel. The file streamlines development by centralizing how common project scripts are executed and debugged.

---

### config.yaml

**Documentation:** `config_documentation.md`

**Summary:** The config.yaml file is the central configuration for an AI-powered documentation generation pipeline, allowing users to customize how technical documentation is produced from source code. It specifies the AI model and provider, token management, file processing rules (such as which files to include or exclude), documentation output format, and detailed templates for different document types like project overviews, user guides, and API documentation. The configuration also defines retry logic for AI generation and enables granular control over which types and sections of documentation are generated. All documentation pipeline processes rely on this file to determine documentation structure, processing behavior, and output customization.

---

### install.sh

**Documentation:** `install_documentation.md`

**Summary:** The install.sh script automates the setup of a consistent development environment for the Documentation Pipeline project on Mac and Linux. It checks for Python 3, manages a virtual environment, installs dependencies from requirements.txt, and handles creation of a local .env configuration file. The script guides users through post-installation steps such as environment activation and configuration validation, ensuring quick, consistent project setup. Key components include Python environment validation, dependency installation, and environment variable file management.

---

### main.py

**Documentation:** `main_documentation.md`

**Summary:** main.py serves as the main entry point for an application that provides a command-line interface (CLI) to generate, analyze, and validate documentation for software code repositories. It supports subcommands for generating documentation (via a DocumentationPipeline), analyzing repository structure (with CodeAnalyzer), and validating configuration/API credentials (using ConfigManager), all via flexible command-line argument parsing. The script coordinates these core functions, handles errors, and ensures user-friendly interactions for developers working with code documentation workflows.

---

### mcp_server.py

**Documentation:** `mcp_server_documentation.md`

**Summary:** The mcp_server.py file implements a Machine/Model Control Protocol (MCP) server designed to provide interactive, programmatic access to documentation generated for a code repository. Its primary functions include allowing clients to query for relevant source files based on description and to extract or summarize documentation about specific features, mainly via the endpoints get_relevant_files and understand_feature. The core class, DocumentationMCPServer, handles server setup, tool registration, and documentation loading, while the server is designed for integration with automated agents, AI tools, or developer utilities. Most tool logic is currently placeholder, anticipating future advanced implementation, and the server expects documentation guides as part of its operation.

---

### src\code_analyzer.py

**Documentation:** `src\code_analyzer_documentation.md`

**Summary:** The src\code_analyzer.py module provides tools for analyzing code repositories to prepare source files for automated documentation generation. Its primary component, the CodeAnalyzer class, scans repositories, filters and reads code files based on configurable extensions and exclusion patterns, and aggregates structural statistics such as file counts by extension and directory. It returns results as CodeFile objects and includes robust encoding handling for file reading. This module is essential for processes requiring enumeration or analysis of code files within a documentation or code analysis pipeline.

---

### src\context_manager.py

**Documentation:** `src\context_manager_documentation.md`

**Summary:** The src/context_manager.py file manages and enhances documentation context in an automated pipeline, focusing on summarizing and merging documentation and guides for downstream use. Its core ContextManager class provides methods to load existing guides, summarize large documentation efficiently with LLMs, format guides, and enrich contexts for tasks like design doc generation. It operates with robust error handling, modular dependencies, and is intended for integration in systems leveraging language models for documentation processing. Key components include context orchestration, token management, and markdown guide handling.

---

### src\design_document_generator.py

**Documentation:** `src\design_document_generator_documentation.md`

**Summary:** The `src/design_document_generator.py` module defines the `DesignDocumentGenerator` class, which manages the automated generation of comprehensive software design documents using large language models (LLMs) via LangChain. It handles initializing document structures, generating content for each section with prompt composition and retry mechanisms, detecting and continuing truncated outputs, and assembling and saving the final documents. The class integrates configurable options, supports modular templates, manages pipeline state, and relies on various supporting components such as token counting and LangChain tool integrations. This module is intended to be called by higher-level orchestration code within a documentation generation pipeline.

---

### src\guide_generator.py

**Documentation:** `src\guide_generator_documentation.md`

**Summary:** The src\guide_generator.py file automates the creation, updating, and management of a comprehensive documentation guide for codebases by aggregating and summarizing individual documentation files. Its main class, GuideGenerator, offers methods to generate top-level guides (with LLM-based summaries), manage incremental updates when files change, handle metadata extraction, and save/load guides and documentation states. It supports both full and incremental guide generation to optimize documentation workflows and is intended to help developers navigate repository documentation efficiently. Key dependencies include LLM interfaces, document processors, and internal models for structured data handling.

---

### src\guide_metadata_manager.py

**Documentation:** `src\guide_metadata_manager_documentation.md`

**Summary:** The `guide_metadata_manager.py` file provides an API for managing and tracking metadata related to incremental documentation (guide) generation in a codebase. Its core functionality includes efficient detection of source or documentation file changes, updating and persisting guide metadata, and determining whether full or partial documentation rebuilds are needed, using robust hashing and change-tracking. The central `GuideMetadataManager` class offers methods for metadata loading, saving, change detection, per-file guide tracking, and resilience against data loss or inconsistencies. It is intended for integration within a larger documentation build pipeline, relying on models like `FileMetadata`, `GuideMetadata`, and `ChangeSet` for structured metadata management.

---

### src\models.py

**Documentation:** `src\models_documentation.md`

**Summary:** The src/models.py file defines all core data models for a documentation generation pipeline, centralizing configuration schemas, request/response models, process state tracking, file representations, guide and design doc structures, and change detection. Key components include models for pipeline configuration, documentation requests, code and documentation artifacts, incremental update tracking, and pipeline orchestration, all leveraging Pydantic for type safety and validation. These models support coordinated documentation creation, guide/design doc management, and efficient incremental updates across the system. The file is essential for maintaining application state, validating data, and enabling modular, robust documentation workflows.

---

### src\pipeline.py

**Documentation:** `src\pipeline_documentation.md`

**Summary:** The src/pipeline.py file defines the main orchestration pipeline for automated codebase documentation using large language models, managing the end-to-end workflow for generating file-level docs, design documents, and documentation guides from source code. Its core class, DocumentationPipeline, establishes a modular, state-driven workflow via a LangGraph state machine, coordinating all process steps including context gathering, LLM invocation, result saving, error-handling, and logging. The pipeline integrates various helper components for configuration, code analysis, document processing, and report generation, and exposes a .run() method for easy automation in scripts or tools. This file serves as the central orchestrator for documentation tasks, supporting extensibility and robust multi-step processing.

---

### src\prompts\ai_assembly_system_message.py

**Documentation:** `src\prompts\ai_assembly_system_message_documentation.md`

**Summary:** This file provides a string template, AI_ASSEMBLY_SYSTEM_MESSAGE, designed as a system prompt for AI language models tasked with assembling complete documents from individual sections. The template guides the AI to create a coherent title, introduction, smooth transitions, consistent tone, and proper conclusion, ensuring the output is a unified document rather than a simple concatenation of parts. It is primarily used in LLM-powered document assembly workflows and includes a placeholder for dynamic document naming. The file is dependency-free and meant to be imported as part of larger document-generation systems.

---

### src\prompts\generate_file_documentation_system_message.py

**Documentation:** `src\prompts\generate_file_documentation_system_message_documentation.md`

**Summary:** This file defines the GENERATED_FILE_DOCUMENTATION_SYSTEM_MESSAGE, a string template used as a system prompt for AI-driven automated technical documentation generation. The template provides detailed instructions and formatting guidelines to ensure comprehensive and consistent documentation of source code files, dynamically inserting context and file-specific metadata via placeholders. It is primarily utilized by scripts or tools that generate documentation using AI models. The file contains no functions or classes—only the template constant.

---

### src\prompts\summarize_docs_system_message.py

**Documentation:** `src\prompts\summarize_docs_system_message_documentation.md`

**Summary:** This file provides a standardized system prompt string, SUMMARIZE_DOCS_SYSTEM_MESSAGE, designed for use with language models to summarize technical documentation. The prompt instructs the model to produce concise yet comprehensive summaries that include key technical concepts, architectural decisions, implementation details, and relationships. It serves as a utility or configuration component for consistent AI-driven documentation summarization workflows and is typically imported by code interfacing with LLM APIs. No additional dependencies are required.

---

