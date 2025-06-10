from typing import Dict, Any, Optional
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from pathlib import Path

from .models import PipelineState, DocumentationContext, DocumentationResult, CodeFile, DocumentationRequest
from .config import ConfigManager
from .document_processor import DocumentProcessor
from .code_analyzer import CodeAnalyzer


class DocumentationPipeline:
    """Main LangGraph pipeline for generating documentation."""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config_manager = ConfigManager(config_path)
        self.config = self.config_manager.load_config()
        self.doc_processor = DocumentProcessor(self.config)
        self.code_analyzer = CodeAnalyzer(self.config)
        self.llm = self._initialize_llm()
        
    def _initialize_llm(self):
        """Initialize the language model based on configuration."""
        model_config = self.config_manager.get_model_config()
        provider = model_config.get("provider", "openai")
        
        if provider == "openai":
            # Use environment variable or passed key
            import os
            api_key = model_config.get("api_key") or os.getenv("OPENAI_API_KEY")
            return ChatOpenAI(
                model=model_config.get("name", "gpt-4"),
                temperature=model_config.get("temperature", 0.2),
                api_key=api_key
            )
        elif provider == "anthropic":
            import os
            api_key = model_config.get("api_key") or os.getenv("ANTHROPIC_API_KEY")
            return ChatAnthropic(
                model=model_config.get("name", "claude-3-sonnet-20240229"),
                temperature=model_config.get("temperature", 0.2),
                api_key=api_key
            )
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    def create_pipeline(self):
        """Create the LangGraph pipeline."""
        workflow = StateGraph(PipelineState)
        
        # Add nodes
        workflow.add_node("load_existing_docs", self.load_existing_docs)
        workflow.add_node("summarize_docs", self.summarize_docs)
        workflow.add_node("scan_repository", self.scan_repository)
        workflow.add_node("generate_documentation", self.generate_documentation)
        workflow.add_node("save_results", self.save_results)
        
        # Add edges
        workflow.set_entry_point("load_existing_docs")
        workflow.add_conditional_edges(
            "load_existing_docs",
            self.should_summarize,
            {
                "summarize": "summarize_docs",
                "continue": "scan_repository"
            }
        )
        workflow.add_edge("summarize_docs", "scan_repository")
        workflow.add_edge("scan_repository", "generate_documentation")
        workflow.add_conditional_edges(
            "generate_documentation",
            self.has_more_files,
            {
                "continue": "generate_documentation",
                "finish": "save_results"
            }
        )
        workflow.add_edge("save_results", END)
        
        return workflow.compile()
    
    def load_existing_docs(self, state: PipelineState) -> Dict[str, Any]:
        """Load and process existing documentation."""
        print("Loading existing documentation...")
        
        # Handle optional docs_path
        docs_path = state.request.docs_path
        docs = self.doc_processor.load_existing_docs(docs_path)
        
        return {
            "existing_docs": docs
        }
    
    def should_summarize(self, state: PipelineState) -> str:
        """Determine if documentation needs summarization."""
        if self.doc_processor.needs_summarization(state.existing_docs):
            return "summarize"
        return "continue"
    
    def summarize_docs(self, state: PipelineState) -> Dict[str, Any]:
        """Summarize existing documentation if it's too large."""
        print("Summarizing existing documentation...")
        
        docs = state.existing_docs
        chunks = self.doc_processor.create_chunks(docs.content)
        
        summarization_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""You are a technical documentation summarizer. 
            Summarize the following documentation chunk while preserving:
            1. Key technical concepts and terminology
            2. Important architectural decisions
            3. Critical implementation details
            4. Dependencies and relationships
            
            Keep the summary concise but comprehensive."""),
            HumanMessage(content="Summarize this documentation:\n\n{chunk}")
        ])
        
        summaries = []
        for chunk in chunks:
            try:
                messages = summarization_prompt.format_messages(chunk=chunk)
                response = self.llm.invoke(messages)
                # Handle different response types
                if hasattr(response, 'content'):
                    content = response.content
                else:
                    content = str(response)
                summaries.append(content)
            except Exception as e:
                print(f"Error summarizing chunk: {e}")
                summaries.append(chunk[:500] + "...")  # Fallback truncation
        
        summarized_content = "\n\n".join(summaries)
        summarized_docs = DocumentationContext(
            content=summarized_content,
            token_count=self.doc_processor.count_tokens(summarized_content),
            summarized=True,
            original_docs=docs.original_docs
        )
        
        return {
            "existing_docs": summarized_docs
        }
    
    def scan_repository(self, state: PipelineState) -> Dict[str, Any]:
        """Scan the repository for code files."""
        print(f"Scanning repository: {state.request.repo_path}")
        
        code_files = self.code_analyzer.scan_repository(state.request.repo_path)
        print(f"Found {len(code_files)} code files to document")
        
        return {
            "code_files": code_files,
            "current_file_index": 0
        }
    
    def generate_documentation(self, state: PipelineState) -> Dict[str, Any]:
        """Generate documentation for the current code file."""
        if state.current_file_index >= len(state.code_files):
            return {"completed": True}
        
        current_file = state.code_files[state.current_file_index]
        print(f"Generating documentation for: {current_file.relative_path}")
        
        # Prepare context
        context = self.doc_processor.prepare_context(state.existing_docs)
        
        # Create documentation prompt
        doc_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=f"""You are a technical documentation generator. Create comprehensive documentation for the provided code file.

Use this existing project documentation as context:
{context}

Generate documentation that includes:
1. **Purpose**: What this file does and why it exists
2. **Functionality**: Detailed explanation of the main functions/classes
3. **Key Components**: Important classes, functions, variables, or modules
4. **Dependencies**: What this file depends on and what depends on it
5. **Usage Examples**: How this code would typically be used

Format the output as clean Markdown. Be thorough but concise.
File extension: {current_file.extension}
Relative path: {current_file.relative_path}"""),
            HumanMessage(content=f"Document this code file:\n\n```{current_file.extension[1:] if current_file.extension else 'text'}\n{current_file.content}\n```")
        ])
        
        try:
            messages = doc_prompt.format_messages()
            response = self.llm.invoke(messages)
            
            # Handle different response types
            if hasattr(response, 'content'):
                documentation = response.content
            else:
                documentation = str(response)
            
            result = DocumentationResult(
                file_path=current_file.path,
                documentation=documentation,
                success=True
            )
        except Exception as e:
            result = DocumentationResult(
                file_path=current_file.path,
                documentation="",
                success=False,
                error_message=str(e)
            )
            print(f"Error generating documentation for {current_file.relative_path}: {e}")
        
        # Update results and move to next file
        new_results = state.results + [result]
        new_index = state.current_file_index + 1
        
        return {
            "results": new_results,
            "current_file_index": new_index
        }
    
    def has_more_files(self, state: PipelineState) -> str:
        """Check if there are more files to process."""
        if state.current_file_index >= len(state.code_files):
            return "finish"
        return "continue"
    
    def save_results(self, state: PipelineState) -> Dict[str, Any]:
        """Save the generated documentation to files."""
        print(f"Saving documentation to: {state.request.output_path}")
        
        output_path = state.request.output_path
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save individual file documentation
        for result in state.results:
            if not result.success:
                continue
                
            # Create output filename
            relative_path = result.file_path.relative_to(state.request.repo_path)
            doc_filename = f"{relative_path.stem}_documentation.md"
            doc_path = output_path / relative_path.parent / doc_filename
            
            # Create directory if needed
            doc_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write documentation
            with open(doc_path, 'w', encoding='utf-8') as f:
                f.write(f"# Documentation for {relative_path}\n\n")
                f.write(result.documentation)
                
                if self.config.output.get("include_code", True):
                    f.write(f"\n\n## Original Code\n\n")
                    f.write(f"```{result.file_path.suffix[1:] if result.file_path.suffix else 'text'}\n")
                    with open(result.file_path, 'r', encoding='utf-8', errors='ignore') as code_file:
                        f.write(code_file.read())
                    f.write("\n```")
        
        # Generate summary report
        self._generate_summary_report(state)
        
        print(f"Documentation generation completed. {len([r for r in state.results if r.success])} files documented successfully.")
        
        return {"completed": True}
    
    def _generate_summary_report(self, state: PipelineState):
        """Generate a summary report of the documentation process."""
        successful = [r for r in state.results if r.success]
        failed = [r for r in state.results if not r.success]
        
        report_content = f"""# Documentation Generation Report

## Summary
- **Total files processed**: {len(state.results)}
- **Successfully documented**: {len(successful)}
- **Failed**: {len(failed)}

## Successfully Documented Files
"""
        
        for result in successful:
            relative_path = result.file_path.relative_to(state.request.repo_path)
            report_content += f"- {relative_path}\n"
        
        if failed:
            report_content += "\n## Failed Files\n"
            for result in failed:
                relative_path = result.file_path.relative_to(state.request.repo_path)
                report_content += f"- {relative_path}: {result.error_message}\n"
        
        # Add existing documentation info
        if state.existing_docs.content:
            report_content += f"\n## Existing Documentation Context\n"
            report_content += f"- **Token count**: {state.existing_docs.token_count}\n"
            report_content += f"- **Summarized**: {state.existing_docs.summarized}\n"
            report_content += f"- **Original documents**: {len(state.existing_docs.original_docs)}\n"
        
        # Save report
        report_path = state.request.output_path / "documentation_report.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
    
    def run(self, repo_path: Path, docs_path: Optional[Path] = None, output_path: Optional[Path] = None) -> PipelineState:
        """Run the complete documentation pipeline."""
        
        if output_path is None:
            output_path = repo_path / "documentation_output"
        
        request = DocumentationRequest(
            repo_path=repo_path,
            docs_path=docs_path,
            output_path=output_path,
            config=self.config
        )
        
        # Create initial state with empty existing_docs
        initial_docs = DocumentationContext(
            content="",
            token_count=0,
            summarized=False,
            original_docs=[]
        )
        
        initial_state = PipelineState(
            request=request,
            existing_docs=initial_docs
        )
        
        pipeline = self.create_pipeline()
        final_state = pipeline.invoke(initial_state)
        
        return final_state
