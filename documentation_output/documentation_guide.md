# Documentation Guide

<!-- AUTO-GENERATED DOCUMENTATION GUIDE -->
<!-- This file was automatically generated and should not be manually edited -->

This guide provides an overview of all generated documentation files in this repository.
Use this guide to quickly locate relevant documentation when working on specific features or components.

**Generated on:** 2025-07-01T23:06:34.897376  
**Total documented files:** 31

## Documentation Files

### .vscode\launch.json

**Documentation:** `.vscode\launch_documentation.md`

**Summary:** The .vscode/launch.json file provides Visual Studio Code launch configurations tailored for automating documentation-related tasks with the project's main.py toolkit. It defines multiple debug/run profiles for generating file-level docs, guides, design docs, performing cleanup, repository analysis, and configuration validation—all directly from the VS Code interface. Each profile specifies program arguments, environment variables (notably setting PYTHONPATH), and supports platform-specific settings to streamline and standardize documentation generation workflows for developers. This setup ensures quick, consistent, and environment-aware execution of complex documentation tasks within the IDE.

---

### config.yaml

**Documentation:** `config_documentation.md`

**Summary:** The 'config.yaml' file serves as the central configuration for an AI-driven documentation generation pipeline, controlling all aspects of model invocation, file selection, processing, output formatting, template management, and robustness features. Key components include settings for LLM provider/model (OpenAI, Anthropic, Azure), token and context limits, file inclusion/exclusion rules, output format options, customizable documentation templates, and retry/continuation logic for handling failures. This file enables maintainers to fully customize and extend the documentation workflow without changing the codebase. It is essential for tailoring the documentation generator and related tools to specific project, workflow, or organizational requirements.

---

### mcp_server.py

**Documentation:** `mcp_server_documentation.md`

**Summary:** mcp_server.py implements a backend MCP Server that provides tools for interacting with and analyzing repository documentation. Its key features include retrieving relevant source files based on natural language descriptions and synthesizing detailed documentation for specific project features. The server exposes these functionalities via the MCP protocol, delegating analysis tasks to an MCPManager component, and is intended for use as a backend service in development or IDE environments. It includes robust logging and is primarily designed for integration with client tools needing repository documentation insights.

---

### src\context_manager.py

**Documentation:** `src\context_manager_documentation.md`

**Summary:** The src\context_manager.py file provides the ContextManager class, which serves to manage, summarize, and enrich documentation context within an LLM-driven documentation generation pipeline. Key functions include loading and formatting documentation guides, summarizing large documentation sources using a language model, and combining these elements to create context-aware documentation artifacts. The class integrates with the pipeline’s state, document processing utilities, and language model, supporting efficient downstream tasks such as design document generation. It relies on supporting data models and manages interaction with the filesystem and logging for diagnostics.

---

### src\document_processor.py

**Documentation:** `src\document_processor_documentation.md`

**Summary:** The src\document_processor.py file provides the DocumentProcessor class and support tools for loading, aggregating, token counting, chunking, and preparing textual documentation for use in AI-driven pipelines. It can handle various documentation formats, determine if content needs summarization based on configurable token thresholds, and split large docs into size-limited chunks. Key dependencies include tiktoken for tokenization and LangChain’s text splitter for chunking. This module is essential for preprocessing, context creation, and managing documentation size for downstream language model tasks.

---

### src\file_processor.py

**Documentation:** `src\file_processor_documentation.md`

**Summary:** The src/file_processor.py module manages source code file handling within a documentation generation pipeline. It provides a FileProcessor class that detects when documentation should be regenerated, processes and saves generated documentation (including metadata and optional code snippets), computes file hashes for change detection, and organizes output directory structures. Core components include support for robust file I/O, error handling, configuration-driven options, and integration with pipeline data models and tooling. This module serves as the central point for all file-specific logic related to generating and managing documentation output.

---

### src\guide_generator.py

**Documentation:** `src\guide_generator_documentation.md`

**Summary:** The src\guide_generator.py module automates the aggregation, summarization, and maintenance of a centralized Documentation Guide for large code repositories. Its core GuideGenerator class loads existing documentation, generates or incrementally updates a Markdown guide by detecting code changes, and produces concise, LLM-powered summaries of each documented file. It integrates with both OpenAI and Anthropic models, efficiently manages metadata, and supports workflows requiring full or incremental guide regeneration. Key dependencies include internal models, a document processor, a metadata manager, and third-party LLM libraries.

---

### src\guide_metadata_manager.py

**Documentation:** `src\guide_metadata_manager_documentation.md`

**Summary:** The src\guide_metadata_manager.py file defines the GuideMetadataManager class, which manages metadata for the incremental generation of documentation guides in a codebase. Its primary functions include detecting file changes, persisting metadata, and determining which source files require documentation updates, thereby enabling efficient incremental builds. Key components involve file and guide metadata management, change detection logic, and APIs for coordinating state across documentation runs. The class interacts with various data models and is intended for use within a larger documentation generation pipeline.

---

### src\llm_manager.py

**Documentation:** `src\llm_manager_documentation.md`

**Summary:** The src\llm_manager.py module provides a unified interface for initializing and configuring language models (LLMs) from OpenAI or Anthropic using the LangChain library. Its main component, the LLMManager class, retrieves settings from an external configuration manager, handles provider selection, manages API keys, and returns a ready-to-use LangChain chat model instance. This abstraction allows seamless switching and integration of different LLM providers within an application.

---

### src\mcp_manager.py

**Documentation:** `src\mcp_manager_documentation.md`

**Summary:** The src\mcp_manager.py file defines the MCPManager class, which provides high-level APIs for intelligent code and documentation exploration using LangGraph workflows orchestrated with LLMs. Its core functions include finding relevant code files for a user query and synthesizing feature explanations from project documentation. Key components are two primary async methods (`find_relevant_files` and `understand_feature`), workflow node functions for LLM interaction and file processing, integration with configuration and prompt management, and use of structured data models for results. This module serves as a central workflow engine for automating code reasoning and feature understanding tasks in larger applications.

---

### src\mcp_models.py

**Documentation:** `src\mcp_models_documentation.md`

**Summary:** The src/mcp_models.py file defines core Pydantic data models for the MCP server, which programmatically analyzes source code repositories and documents features using language models. It includes models for representing requests and responses related to relevant file discovery, in-depth feature understanding, workflow state tracking, documentation file handling, and error management. These models enable type-safe, validated communication between MCP API endpoints, workflow engines, and LLM integrations. The code is essential for structuring and orchestrating the analysis and documentation workflow within applications interacting with code repositories.

---

### src\models.py

**Documentation:** `src\models_documentation.md`

**Summary:** The src/models.py file defines Pydantic-based data models and schemas that structure and validate all major configuration, state, request, input, output, and metadata objects for the documentation generation toolkit. It provides type-safe, serializable contracts for orchestrating complex documentation workflows—including file-level, guide, design document, and incremental generation features—through models like PipelineConfig, DocumentationRequest, CodeFile, DocumentationResult, DocumentationGuide, DesignDocument, PipelineState, and related metadata/state classes. This module serves as the backbone for input validation, workflow state tracking, and inter-component data sharing throughout the toolkit's processing and orchestration layers. All main components and pipelines in the toolkit depend on these models for reliable, reproducible, and extensible documentation processes.

---

### src\pipeline.py

**Documentation:** `src\pipeline_documentation.md`

**Summary:** The src/pipeline.py file implements the main orchestrator for an automated, LLM-powered documentation pipeline for software repositories, coordinating tasks such as codebase scanning, documentation summarization, and generation of new documentation artifacts. Its core component is the DocumentationPipeline class, which defines a modular, stateful LangGraph-based workflow, manages pipeline state and transitions, and delegates processing to specialized manager components. The pipeline supports incremental processing, conditional branching, robust error handling, and extensive configurability, serving as the entry point for end-to-end documentation generation invoked by external interfaces like CLI tools. Key dependencies include LangGraph for workflow, LangChain for LLM integration, and various domain-specific managers for document, design, and guide generation.

---

### src\prompts\ai_assembly_system_message.py

**Documentation:** `src\prompts\ai_assembly_system_message_documentation.md`

**Summary:** The src\prompts\ai_assembly_system_message.py file provides a formatted system prompt template, AI_ASSEMBLY_SYSTEM_MESSAGE, designed to guide AI agents in assembling multiple document sections into a coherent, stylistically consistent whole. Its key function is to ensure the AI creates a unified title, introduction, smooth transitions, appropriate connective text, and a conclusion, rather than simply merging sections. The file is self-contained with no external dependencies and is typically used by components interfacing with AI models for automated document generation.

---

### src\prompts\continue_truncated_content_system_prompt.py

**Documentation:** `src\prompts\continue_truncated_content_system_prompt_documentation.md`

**Summary:** The file defines CONTINUE_TRUNCATED_CONTENT_SYSTEM_PROMPT, a multi-line string template used to guide AI agents in continuing previously truncated documentation sections within automated documentation generation or augmentation systems. The template incorporates variables for document name, section name, context, section instructions, and specific continuation cues, and informs the agent about file-reading tools available for further information retrieval. It does not execute logic or import modules; instead, it serves as a static prompt resource to be filled and dispatched by other components in an LLM-powered documentation workflow. This makes the file essential for ensuring consistent, context-aware continuation of incomplete documentation by AI assistants.

---

### src\prompts\generate_doc_summary_system_message.py

**Documentation:** `src\prompts\generate_doc_summary_system_message_documentation.md`

**Summary:** This file defines the GENERATE_DOC_SUMMARY_SYSTEM_MESSAGE constant, a prompt template designed for instructing AI models to generate concise, 2-4 sentence summaries of technical documentation. Its primary function is to standardize summary outputs by focusing on the main purpose and key components of a codebase or file. The file contains no dependencies and serves as a reusable configuration asset for LLM-powered summarization workflows.

---

### src\prompts\generate_file_documentation_system_message.py

**Documentation:** `src\prompts\generate_file_documentation_system_message_documentation.md`

**Summary:** This file provides a reusable string template, GENERATED_FILE_DOCUMENTATION_SYSTEM_MESSAGE, designed to standardize and automate the generation of Python file documentation by AI agents or documentation tools. The template accepts project context, file extension, and file path as input, and instructs the agent to generate Markdown-formatted documentation sections such as Purpose, Functionality, Components, Dependencies, and Usage Examples. It is typically used within AI-driven documentation pipelines that generate system prompts for codebase documentation tasks.

---

### src\prompts\mcp_file_relevance_prompt.py

**Documentation:** `src\prompts\mcp_file_relevance_prompt_documentation.md`

**Summary:** The src/prompts/mcp_file_relevance_prompt.py file defines three specialized system prompt templates as string constants for use with Large Language Models (LLMs) in code and documentation analysis tasks. These prompts enable LLMs to (1) identify relevant source code files for a user query, (2) discover documentation files related to specific features, and (3) synthesize structured, comprehensive feature overviews from multiple documentation sources. The file serves as a centralized resource for prompt injection in developer tools, documentation assistants, or code analysis pipelines, ensuring consistent, context-aware outputs. It does not contain any dependencies or executable logic beyond the prompt definitions.

---

### src\prompts\section_prompt_system_message.py

**Documentation:** `src\prompts\section_prompt_system_message_documentation.md`

**Summary:** This file defines SECTION_PROMPT_SYSTEM_MESSAGE, a parameterized string template used as a system prompt for AI-based technical documentation generation. It instructs the AI on how to utilize available codebase exploration tools and contextual information to create detailed documentation sections within a design document. The template is designed to be dynamically filled with document-specific details and is intended for integration into larger documentation automation workflows, ensuring consistency and reusability.

---

### src\prompts\summarize_docs_system_message.py

**Documentation:** `src\prompts\summarize_docs_system_message_documentation.md`

**Summary:** The file src/prompts/summarize_docs_system_message.py defines a string variable containing detailed system-level instructions for AI models to use when summarizing technical documentation. Its main function is to guide summarization engines to produce concise but comprehensive summaries, preserving key technical concepts, architectural decisions, and dependencies. The file is dependency-free and is intended to be imported by AI-driven tools or scripts that require standardized, high-quality summarization prompts for technical contexts.

---

### src\report_generator.py

**Documentation:** `src\report_generator_documentation.md`

**Summary:** The src\report_generator.py file defines the ReportGenerator class, which generates summary reports and tracks the status of file and design documentation runs within a documentation pipeline. Its key functions include saving documentation outputs, assembling comprehensive Markdown reports (detailing successes, failures, and skips), and providing detailed status updates for design documentation generation. The module interfaces with PipelineState and a file processor to collate process outcomes, prints summaries to the console, and writes a final Markdown report to the output directory. It is intended to be used as the final reporting step in an automated documentation workflow.

---

### src\state_manager.py

**Documentation:** `src\state_manager_documentation.md`

**Summary:** The src/state_manager.py file provides centralized management of state transitions and branching logic within a documentation generation pipeline. Its main component, the StateManager class, determines when to load existing docs, summarize content, generate documentation, and handle iteration over files, documents, and sections, using the current pipeline state and external processors. The module ensures maintainable and consistent flow control and is designed to be used by higher-level pipeline controllers orchestrating the documentation workflow. Key dependencies include typing support, a PipelineState model, and external processors for summarization decisions.

---

### src\tools\file_tools.py

**Documentation:** `src\tools\file_tools_documentation.md`

**Summary:** The src\tools\file_tools.py module provides utility functions for secure file and directory handling within a repository, ensuring all operations remain inside the project boundaries. Key features include reading file content with encoding support, listing and searching for files by extension or glob pattern, and extracting detailed file metadata—all while enforcing security checks and returning consistent, repository-relative paths. It is especially suited for tools that perform automated code analysis, repository searches, or developer utilities needing safe and flexible access to project files.

---

### src\tools\lc_tools\lc_file_tools.py

**Documentation:** `src\tools\lc_tools\lc_file_tools_documentation.md`

**Summary:** The code in src/tools/lc_tools/lc_file_tools.py provides a factory function, create_file_tools, that generates LangChain-compatible Tool objects for performing file operations within a specific repository path. Key functionalities offered include reading file contents, listing files (with filtering and recursion), searching files by pattern, and retrieving file metadata. These tools expose AI-friendly wrappers around underlying file system functions, handling errors gracefully and making them suitable for integration into LangChain agents or chains. All operations are scoped to the provided repository root, enabling controlled file access for LLM-driven workflows.

---

### src\utilities\token_manager.py

**Documentation:** `src\utilities\token_manager_documentation.md`

**Summary:** The src\utilities\token_manager.py module provides utilities for managing and estimating token usage in applications that interact with Large Language Models (LLMs) like GPT-3.5 or GPT-4. Its core component, the TokenCounter class, counts tokens in texts using model-specific encoders from the tiktoken library, estimates token usage for sequences of chat messages (including structural overhead), and manages model-to-encoder mappings with fallbacks and logging. This enables precise budget tracking and context window management for LLM applications.

---

### .vscode\tasks.json

**Documentation:** `.vscode\tasks_documentation.md`

**Summary:** The .vscode/tasks.json file defines automated VS Code tasks to streamline development workflows for the Documentation MCP Server project. It provides shell-based tasks to start the MCP server using the workspace's Python virtual environment and to install project dependencies from requirements.txt. These tasks facilitate quick server launch and dependency management directly within the VS Code interface, enhancing developer convenience and consistency. The configuration assumes a Windows environment and requires a virtual environment, mcp_server.py, and requirements.txt in the project workspace.

---

### main.py

**Documentation:** `main_documentation.md`

**Summary:** main.py serves as the command-line interface (CLI) entry point for a documentation generation toolkit. It enables users to generate, analyze, and clean up documentation for a source code repository through various subcommands and arguments, including documentation generation, repository analysis, configuration validation, and orphaned documentation cleanup. Key components include the DocumentationPipeline for orchestrating documentation, ConfigManager for configuration handling, and CodeAnalyzer for repository structure analysis. The script emphasizes flexible argument parsing, robust error handling, and ease of use for managing code documentation workflows.

---

### src\config.py

**Documentation:** `src\config_documentation.md`

**Summary:** The src/config.py file provides a centralized configuration manager for the documentation toolkit and MCP server, handling the secure loading and access of settings and sensitive credentials. Its primary component, the ConfigManager class, loads and validates configuration from a YAML file, manages environment variables (including API keys for LLM providers), and supplies aggregated runtime configuration dictionaries for downstream use. Supporting methods include loading and caching config data, secure API key lookup, and constructing LLM provider configuration objects. This module ensures unified, consistent, and secure configuration management across the project.

---

### .vscode\settings.json

**Documentation:** `.vscode\settings_documentation.md`

**Summary:** The .vscode/settings.json file configures project-level settings for Visual Studio Code, focusing on Python development and integrating the MCP (Model Context Protocol) documentation server within the workspace. Key components include specifying the Python interpreter path (typically a project virtual environment) and providing detailed commands for launching and managing the MCP server via the MCP VS Code extension. These settings ensure consistent Python environment usage and enable automated code documentation and analysis directly from VS Code. The configuration relies on a local virtual environment, the mcp_server.py script, and compatible VS Code extensions for full functionality.

---

### src\design_document_generator.py

**Documentation:** `src\design_document_generator_documentation.md`

**Summary:** The src/design_document_generator.py module provides the DesignDocumentGenerator class, which automates the creation of comprehensive, multi-section software design documents using a Large Language Model (LLM) through LangChain. It manages workflow state, context assembly, section-by-section generation (with truncation and error handling), and final Markdown file output, integrating various prompts and tooling to ensure context-aware, high-quality documentation. The generator depends on project-specific configuration and a document processor, outputs documents with metadata, and is designed for seamless integration within an AI-powered documentation pipeline.

---

### src\code_analyzer.py

**Documentation:** `src\code_analyzer_documentation.md`

**Summary:** The src/code_analyzer.py module provides the core functionality for scanning, filtering, and analyzing source code files in a repository to support automated documentation workflows. Its main class, CodeAnalyzer, recursively identifies relevant code files based on configurable inclusion/exclusion rules, robustly reads their contents, and generates structured metadata and summary statistics. Key components include the scan_repository method for collecting code files, helpers for file inclusion logic and robust reading, and utilities for analyzing file structure. Outputs from this module are essential for downstream documentation generators and tooling.

---

