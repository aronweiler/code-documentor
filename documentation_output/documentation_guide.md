# Documentation Guide

<!-- AUTO-GENERATED DOCUMENTATION GUIDE -->
<!-- This file was automatically generated and should not be manually edited -->

This guide provides an overview of all generated documentation files in this repository.
Use this guide to quickly locate relevant documentation when working on specific features or components.

**Generated on:** 2025-06-30T02:49:21.345520  
**Total documented files:** 34

## Documentation Files

### config.yaml

**Documentation:** `config_documentation.md`

**Summary:** config.yaml is the central configuration file for an AI-driven documentation pipeline, defining all operational parameters, model settings, file processing rules, output formats, and documentation templates. It controls aspects such as AI model/provider selection, token management, file inclusion/exclusion, output formatting (with options like Markdown and side-by-side code/docs), retry and error handling policies, and template structures for various documentation types. This file ensures consistency, scalability, and customization across automated documentation generation workflows. It is essential for guiding how the pipeline processes source files and generates high-quality, customizable documentation outputs.

---

### install.sh

**Documentation:** `install_documentation.md`

**Summary:** The install.sh script automates the environment setup for the Documentation Pipeline project on Mac and Linux by checking for Python 3, creating a virtual environment, installing dependencies from requirements.txt, and preparing environment configuration files. Key functionalities include virtual environment management, Python dependency installation, and automated setup of the .env file for local configuration. This ensures a consistent and reliable development environment for all contributors and users.

---

### main.py

**Documentation:** `main_documentation.md`

**Summary:** main.py serves as the primary command-line interface (CLI) entry point for a tool that generates, analyzes, and validates documentation for code repositories. It parses command-line arguments, supports subcommands (generate, analyze, validate-config), and triggers the appropriate pipeline for each operation. Key components include argument parsing functions, handlers for each operation (documentation generation, repository analysis, config validation), and integration with modules such as DocumentationPipeline, ConfigManager, and CodeAnalyzer. The script handles user interaction, error reporting, and provides usage examples for flexible, user-friendly operation.

---

### mcp_server.py

**Documentation:** `mcp_server_documentation.md`

**Summary:** mcp_server.py implements a stdio-based MCP (Machine Communication Protocol) server for intelligent querying, searching, and understanding of repository documentation. Its core functionality includes two main endpoints: one to retrieve relevant files based on natural language descriptions, and another to generate structured summaries explaining specific features. The server delegates business logic to the MCPManager class, making it extensible for integration with developer tools, documentation assistants, or code analysis pipelines. Extensive logging and schema-driven tool handling are provided for robust and extensible operations.

---

### mcp_server_http.py

**Documentation:** `mcp_server_http_documentation.md`

**Summary:** mcp_server_http.py provides an HTTP (FastAPI-based) and optional stdio server interface to a Machine Control Protocol (MCP) backend for repository documentation and code navigation. Its primary functions include allowing users or tools to find relevant files based on natural language queries and to understand or summarize code features via a web API or direct process communication. Key components include the DocumentationMCPServer for initializing tools and the HTTPMCPWrapper for publishing FastAPI endpoints, with core logic powered by an MCPManager. This makes it suitable for integration with editors, automation scripts, or web UIs for code search and documentation workflows.

---

### .vscode/launch.json

**Documentation:** `.vscode/launch_documentation.md`

**Summary:** The .vscode/launch.json file defines launch and debug configurations for running common Python-based tasks—such as generating documentation, analyzing repositories, and validating configurations—in Visual Studio Code. Each profile specifies command-line arguments, environment settings, and working directories for executing main.py with different commands (e.g., generate, analyze, validate-config). This setup streamlines development workflows by making these tasks easily accessible in VSCode’s Run and Debug interface. The configurations depend on Python, debugpy, and a project-specific main.py script.

---

### .vscode/settings.json

**Documentation:** `.vscode/settings_documentation.md`

**Summary:** The .vscode/settings.json file configures project-specific settings for Visual Studio Code, primarily specifying the use of a local Python virtual environment as the default interpreter for all Python-related tooling. It also defines a custom "documentation-server" command under the mcp.servers configuration, enabling easy launch of a documentation server script within the workspace. These settings ensure consistent development environments and streamlined integration of custom server tasks for all contributors opening the project in VS Code.

---

### .vscode/tasks.json

**Documentation:** `.vscode/tasks_documentation.md`

**Summary:** The .vscode/tasks.json file defines reusable Visual Studio Code tasks for automating common development workflows in a Python project that uses a virtual environment. It primarily provides tasks to start a local documentation server and install project dependencies via commands executed in the venv. Key components include task configuration such as command paths, arguments, output display, grouping, and working directory. This setup streamlines running and managing these tasks directly within VS Code, assuming the presence of required scripts and the virtual environment.

---

### src/code_analyzer.py

**Documentation:** `src/code_analyzer_documentation.md`

**Summary:** code_analyzer.py provides core functionality to scan and analyze code repositories, focusing on discovering, robustly reading, and summarizing code files based on configurable inclusion/exclusion criteria. The main component, the CodeAnalyzer class, filters files by extension and pattern, reads contents with encoding fallback, and generates structural statistics like file counts and largest files. It leverages imported CodeFile and PipelineConfig data structures to manage file metadata and processing rules. The module is intended for integration into documentation pipelines or tools needing detailed codebase analysis.

---

### src/config.py

**Documentation:** `src/config_documentation.md`

**Summary:** The src/config.py file centralizes configuration management for the project by loading settings from a YAML file and managing sensitive credentials using environment variables from a .env file. Its core component, the ConfigManager class, parses pipeline settings, securely retrieves API keys for supported providers (such as OpenAI, Anthropic, and Azure OpenAI), and merges static and dynamic configuration data for use throughout the application. This approach separates configuration from code for better maintainability and ensures that all runtime settings and secrets are accessed securely and consistently. The module relies on external packages like PyYAML and python-dotenv, and depends on a PipelineConfig data model defined elsewhere in the project.

---

### src/context_manager.py

**Documentation:** `src/context_manager_documentation.md`

**Summary:** The src/context_manager.py file provides the ContextManager class, which manages documentation context for a documentation generation pipeline. Its primary functions include loading and enhancing documentation with optional guides, summarizing large documents using a large language model (LLM), and ensuring context is accurate and usable for subsequent pipeline stages. Key components involve integrating document processing utilities, LLM invocation, prompt handling, and supporting various context formats for downstream tasks. This module is essential for pipelines needing context-aware, efficiently summarized, and enhanced documentation inputs.

---

### src/design_document_generator.py

**Documentation:** `src/design_document_generator_documentation.md`

**Summary:** The file src/design_document_generator.py provides the core logic for automated generation of structured design documents using a Large Language Model (LLM). Its main component, the DesignDocumentGenerator class, manages the full workflow: planning which documents and sections to generate, creating section content (handling truncation and retries), assembling completed documents, and persisting results as Markdown files. The module supports integration into larger documentation pipelines and relies on project-specific models, prompts, and utilities for state management and LLM interaction. It enables iterative, context-aware creation and updating of design documentation, supporting both granular section management and final document assembly.

---

### src/document_processor.py

**Documentation:** `src/document_processor_documentation.md`

**Summary:** The file document_processor.py provides a utility class, DocumentProcessor, for loading, processing, and preparing documentation files for use in large language model (LLM) pipelines. Its core functions include robustly reading and concatenating documentation from various formats, counting tokens using GPT-4's tokenizer, determining if summarization is needed based on configurable thresholds, and chunking large documents into LLM-friendly segments. The module relies on external libraries such as tiktoken (for token counting) and langchain (for text splitting), and outputs content structured for efficient downstream usage. It is designed for integration as an early step in documentation generation or analysis pipelines that must handle input size limits.

---

### src/file_processor.py

**Documentation:** `src/file_processor_documentation.md`

**Summary:** The file_processor.py module provides core logic for managing source code file processing within a documentation generation pipeline. Its primary functions include detecting file changes using hashes, managing output directory structures, and saving generated documentation—complete with metadata and, optionally, source code. The central FileProcessor class offers methods for determining when to regenerate documentation, computing file hashes, and handling robust file and directory operations. This module is essential for keeping generated documentation synchronized with source code changes in an automated system.

---

### src/guide_generator.py

**Documentation:** `src/guide_generator_documentation.md`

**Summary:** The src/guide_generator.py module orchestrates the generation, updating, and summarization of a project-level documentation guide by compiling per-file documentation into a comprehensive, indexed Markdown guide. It leverages LLMs to create summaries, supports both full and incremental updates in response to codebase changes, and maintains metadata about documentation coverage and changes. The core GuideGenerator class handles loading documentation, summarizing content, detecting changes, and managing guide entries, with robust error handling and extensibility for different LLM backends. This module integrates with supporting data models, document processing utilities, and metadata managers within a larger documentation pipeline.

---

### src/guide_metadata_manager.py

**Documentation:** `src/guide_metadata_manager_documentation.md`

**Summary:** The src/guide_metadata_manager.py file provides the GuideMetadataManager class, which manages metadata for incremental documentation and guide generation in source code repositories. Its main functions include tracking file metadata, detecting changes (new, modified, deleted files), and supporting efficient incremental or full documentation rebuilds. It offers serialization/deserialization for metadata persistence, change detection logic, and integrates with a broader documentation pipeline using supporting data classes like GuideMetadata and ChangeSet. This module is foundational for enabling scalable, selective documentation updates rather than costly full regenerations.

---

### src/llm_manager.py

**Documentation:** `src/llm_manager_documentation.md`

**Summary:** The `src/llm_manager.py` module provides the `LLMManager` class, which abstracts and configures Large Language Model (LLM) clients (OpenAI or Anthropic) using LangChain integrations, based on external configuration or environment variables. It handles provider selection, credential management, and instantiates the appropriate client (`ChatOpenAI` or `ChatAnthropic`). The main functionality enables other application components to easily obtain a ready-to-use, properly configured LLM client for inference or chat tasks, without managing provider-specific details.

---

### src/mcp_manager.py

**Documentation:** `src/mcp_manager_documentation.md`

**Summary:** The `src/mcp_manager.py` file provides the `MCPManager` class, which orchestrates high-level Model Context Protocol (MCP) workflows for codebase analysis using LangGraph and LLMs. Its primary functions are locating source code files relevant to a specific query and synthesizing comprehensive project feature summaries from documentation. Key components include workflow assembly (with various node functions for document loading, LLM querying, and result formatting), async public methods (`find_relevant_files`, `understand_feature`), and robust integration with config, LLM, and prompt management. This module serves as the central service for advanced, context-aware code and documentation exploration in user-facing APIs, CLIs, or tools.

---

### src/mcp_models.py

**Documentation:** `src/mcp_models_documentation.md`

**Summary:** The file src/mcp_models.py defines core Pydantic data models that structure and validate the requests, responses, and workflow state for an MCP (Model Context Protocol) server. It provides schemas essential for searching relevant files, feature understanding, handling documentation files, and managing workflow integration (e.g., with LangGraph). Key components include models for relevant file search requests/responses, feature understanding, documentation file representation, and a comprehensive state object for orchestrating MCP operations. These models serve as the backbone for any server or workflow that requires structured data exchange and workflow management related to MCP functionalities.

---

### src/models.py

**Documentation:** `src/models_documentation.md`

**Summary:** The file src/models.py defines core Pydantic data models used throughout a documentation generation pipeline, providing validated structures for configuration, request/response handling, state tracking, and documentation outputs. Key components include configuration and request models, representations for code files and documentation, guide and design document structures, and mechanisms for incremental processing and overall pipeline state. These models serve as type-safe, serializable building blocks enabling consistent data exchange and validation across all parts of the system. No business logic is implemented—only structured data definitions supporting the documentation workflow.

---

### src/pipeline.py

**Documentation:** `src/pipeline_documentation.md`

**Summary:** The src/pipeline.py file provides an automated pipeline for generating and updating documentation for code repositories. Its main class, DocumentationPipeline, uses a modular, stateful workflow (via LangGraph) to scan source code, generate per-file documentation with an LLM, assemble documentation guides and design documents, manage pipeline state, and orchestrate interactions between various supporting components (like configuration, code analysis, and reporting). The pipeline supports incremental updates and can be integrated programmatically to streamline documentation tasks and improve project maintainability. Key data models and managers abstract state, configuration, LLM interactions, and file processing.

---

### src/report_generator.py

**Documentation:** `src/report_generator_documentation.md`

**Summary:** The src/report_generator.py module provides the central reporting and output logic for a documentation generation pipeline. Its main class, ReportGenerator, handles saving results, generating Markdown summary reports, and reporting on both file-level and design-level documentation statuses. Key features include configurable output handling, detailed statistics, and breakdowns of design documentation outcomes, enabling users and developers to quickly assess overall pipeline results and areas needing attention. This module is typically invoked at the conclusion of a pipeline run to finalize and summarize documentation generation.

---

### src/state_manager.py

**Documentation:** `src/state_manager_documentation.md`

**Summary:** The src/state_manager.py file defines the StateManager class, which centralizes the decision-making logic for managing state transitions in a documentation generation pipeline. It uses the current pipeline state (PipelineState) and a doc processor to determine which workflow steps to execute next—such as loading existing docs, summarizing, generating file or design docs, and progressing through files or sections. Core methods enable orchestration of conditional progression through the pipeline, providing a stateless, modular controller to support complex documentation workflows. This module is intended to be used by higher-level orchestration code to streamline and clarify pipeline management.

---

### src/prompts/ai_assembly_system_message.py

**Documentation:** `src/prompts/ai_assembly_system_message_documentation.md`

**Summary:** This file defines the AI system prompt used to instruct language models on assembling a coherent, unified document from multiple sections. The core component is the AI_ASSEMBLY_SYSTEM_MESSAGE string, which outlines requirements such as generating a title/introduction, adding transitions and connecting text, ensuring consistent tone, and concluding the document. It is intended for use in LLM-powered workflows that require automated document assembly, with no external dependencies. This prompt standardizes guidance for creating professional, well-structured documents via AI.

---

### src/prompts/continue_truncated_content_system_prompt.py

**Documentation:** `src/prompts/continue_truncated_content_system_prompt_documentation.md`

**Summary:** This file provides a multi-line string template, CONTINUE_TRUNCATED_CONTENT_SYSTEM_PROMPT, designed as a system prompt for AI-driven documentation tools to seamlessly continue writing truncated documentation sections. The template includes placeholders for document name, section, context, instructions, and specific continuation prompts, and informs the AI about helper functions for accessing additional file and directory content. The file contains no executable code or logic, serving solely as a reusable prompt template for integration into documentation automation workflows.

---

### src/prompts/generate_doc_summary_system_message.py

**Documentation:** `src/prompts/generate_doc_summary_system_message_documentation.md`

**Summary:** This file provides a single string constant, GENERATE_DOC_SUMMARY_SYSTEM_MESSAGE, containing explicit instructions for AI models to generate concise, 2-4 sentence summaries of technical documentation. Its primary function is to guide the AI to focus on a code file’s main purpose and key components, while ignoring formatting or style. The file is fully self-contained and designed to be imported as a system message prompt for AI-powered summarization tasks. It serves as a template rather than containing any executable logic.

---

### src/prompts/generate_file_documentation_system_message.py

**Documentation:** `src/prompts/generate_file_documentation_system_message_documentation.md`

**Summary:** This file provides a template string, GENERATED_FILE_DOCUMENTATION_SYSTEM_MESSAGE, designed as a system prompt for AI-based code documentation generators. It includes placeholders for project context and file metadata to produce consistent, well-structured Markdown documentation covering purpose, functionality, key components, dependencies, and usage examples for a given code file. The template is intended to be imported and dynamically filled elsewhere in the project to guide automated documentation creation. No external dependencies are required.

---

### src/prompts/mcp_file_relevance_prompt.py

**Documentation:** `src/prompts/mcp_file_relevance_prompt_documentation.md`

**Summary:** This file defines three system prompt templates used to guide large language models (LLMs) within the Modular Code Platform (MCP) for automated codebase and documentation analysis. The key components—MCP_FILE_RELEVANCE_SYSTEM_PROMPT, MCP_FEATURE_DISCOVERY_SYSTEM_PROMPT, and MCP_FEATURE_SYNTHESIS_SYSTEM_PROMPT—enable LLMs to determine relevant source code files, locate documentation for specific features, and synthesize comprehensive feature explanations from multiple docs, respectively. Each prompt enforces strict output formatting to enable reliable downstream parsing. The module contains only these string constants and is designed to be imported as prompt context for LLM invocations supporting code understanding and documentation navigation tasks.

---

### src/prompts/section_prompt_system_message.py

**Documentation:** `src/prompts/section_prompt_system_message_documentation.md`

**Summary:** The file defines a system message prompt template (SECTION_PROMPT_SYSTEM_MESSAGE) intended for use by AI-driven documentation generation tools. Its primary function is to guide the AI in producing accurate, structured documentation sections by instructing it to explore and understand the codebase using available file and directory exploration tools. The template is a formatted string with placeholders for document and section names, context, and instructions, and is used programmatically in documentation workflows to standardize prompts for AI agents. It contains no runtime dependencies and serves as a key component in aligning AI-generated documentation with project best practices.

---

### src/prompts/summarize_docs_system_message.py

**Documentation:** `src/prompts/summarize_docs_system_message_documentation.md`

**Summary:** This file provides a specialized system prompt template (SUMMARIZE_DOCS_SYSTEM_MESSAGE) for guiding AI language models to summarize technical documentation chunks while preserving key concepts, architectural decisions, implementation details, and dependencies. The constant is intended for use in AI-powered documentation summarization workflows, ensuring summaries are both concise and technically comprehensive. It contains no external dependencies and is meant to be integrated into larger LLM-based systems or tools requiring consistent and high-quality technical documentation summaries.

---

### src/tools/file_tools.py

**Documentation:** `src/tools/file_tools_documentation.md`

**Summary:** The src/tools/file_tools.py module provides secure and convenient functions for reading file contents, listing and searching for files, and retrieving file metadata, all restricted to stay within a specified repository boundary. Key functionalities include reading files with robust encoding handling, listing files with extension and recursive options, pattern-based file searching, and gathering file metadata, with all operations ensuring paths do not escape the repository. Core components rely on pathlib for path management and enforce security checks on every access. This module is self-contained and suitable for any tool or script that requires controlled and safe file system operations within a project.

---

### src/utilities/token_manager.py

**Documentation:** `src/utilities/token_manager_documentation.md`

**Summary:** The src/utilities/token_manager.py module provides utilities for managing and estimating token usage with Large Language Models (LLMs), particularly those from OpenAI like GPT-4 and GPT-3.5. Its core TokenCounter class enables precise token counting for texts and multi-message chat conversations according to model-specific encodings, handles unknown models with graceful fallbacks, and supports budgeting and prompt size optimization. Key functions include count_tokens for text, estimate_tokens_for_messages for conversation threads, and internal handling of encoding mappings via the tiktoken library. This utility is essential for any application interacting with OpenAI APIs where token limits and usage control are important.

---

### src/tools/lc_tools/lc_file_tools.py

**Documentation:** `src/tools/lc_tools/lc_file_tools_documentation.md`

**Summary:** The file defines a factory function, `create_file_tools`, which generates a set of LangChain Tool objects for performing safe and controlled file operations within a specified repository. It provides tools for reading file contents, listing and searching files, and retrieving file metadata, each exposed via a standardized interface for use by language model agents. These tools leverage underlying utility functions and are designed for agent-driven tasks such as code analysis or automation, with robust input handling and user-friendly error reporting. The module is primarily intended for integration with LangChain agents needing repository-level file access.

---

### documentation_output/.documentation_state/guide_metadata.json

**Documentation:** `documentation_output/.documentation_state/guide_metadata_documentation.md`

**Summary:** The guide_metadata.json file is a machine-generated metadata registry used by the project's documentation generation system to track and manage the state of documentation for each source file. It records details like file paths, modification and generation timestamps, hashes, and schema versioning, enabling incremental documentation updates and consistent integrity checks. Key components include global guide metadata and a tracked_files mapping that links source files to their documentation status. This file is read and updated exclusively by documentation tools to automate the detection of changes and control documentation regeneration.

---

