# Documentation Generation Report

## Summary
- **Total files processed**: 32
- **Successfully documented**: 9
- **Skipped (unchanged)**: 23
- **Failed**: 0

## Successfully Documented Files
- .vscode\launch.json
- .vscode\settings.json
- .vscode\tasks.json
- config.yaml
- main.py
- src\code_analyzer.py
- src\config.py
- src\design_document_generator.py
- src\models.py

## Skipped Files (No Changes)
- install.sh
- mcp_server.py
- src\context_manager.py
- src\document_processor.py
- src\file_processor.py
- src\guide_generator.py
- src\guide_metadata_manager.py
- src\llm_manager.py
- src\mcp_manager.py
- src\mcp_models.py
- src\pipeline.py
- src\prompts\ai_assembly_system_message.py
- src\prompts\continue_truncated_content_system_prompt.py
- src\prompts\generate_doc_summary_system_message.py
- src\prompts\generate_file_documentation_system_message.py
- src\prompts\mcp_file_relevance_prompt.py
- src\prompts\section_prompt_system_message.py
- src\prompts\summarize_docs_system_message.py
- src\report_generator.py
- src\state_manager.py
- src\tools\file_tools.py
- src\tools\lc_tools\lc_file_tools.py
- src\utilities\token_manager.py

## Design Documentation
- **Total document types configured**: 0
- **Enabled document types**: 0
- **Disabled document types**: 0
- **Successfully generated**: 3
- **Failed**: 1

### Successfully Generated Design Documents
- **project_overview**: 2/2 sections
  - File: design_documentation\project_overview.md
- **architecture**: 2/2 sections
  - File: design_documentation\architecture.md
- **user_guide**: 2/2 sections
  - File: design_documentation\user_guide.md

### Failed Design Documents
- **developer_guide**: None
  - Failed sections:
    - development_setup: None
    - contribution_guidelines: None

### Section Statistics
- **Total sections**: 8
- **Successful sections**: 6
- **Failed sections**: 2

## Existing Documentation Context
- **Token count**: 7066
- **Summarized**: False
- **Original documents**: 3

## Processing Configuration
- **Max files limit**: 1000
- **Incremental saving**: True
- **File documentation**: True
- **Design docs**: True
- **Documentation guide**: True
