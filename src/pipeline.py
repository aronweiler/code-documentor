from datetime import datetime
import logging
from typing import Dict, Any, List, Optional
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from pathlib import Path

from .prompts.generate_file_documentation_system_message import (
    GENERATED_FILE_DOCUMENTATION_SYSTEM_MESSAGE,
)

from .guide_generator import GuideGenerator
from .design_document_generator import DesignDocumentGenerator
from .file_processor import FileProcessor
from .report_generator import ReportGenerator
from .context_manager import ContextManager
from .state_manager import StateManager
from .llm_manager import LLMManager

from .models import (
    PipelineState,
    DocumentationContext,
    DocumentationResult,
    CodeFile,
    DocumentationRequest,
)
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

        # Initialize LLM manager and get LLM instance
        self.llm_manager = LLMManager(self.config_manager)
        self.llm = self.llm_manager.initialize_llm()

        # Initialize all the specialized managers
        self.design_doc_generator = DesignDocumentGenerator(
            self.llm, self.config, self.doc_processor
        )
        self.guide_generator = GuideGenerator(
            llm=self.llm, config=self.config, doc_processor=self.doc_processor
        )
        self.file_processor = FileProcessor(self.config)
        self.report_generator = ReportGenerator(self.config)
        self.context_manager = ContextManager(self.config, self.doc_processor, self.llm)
        self.state_manager = StateManager(self.config)

        self._setup_logging()

    def _setup_logging(self):
        """Setup logging for the pipeline."""
        log_level = logging.INFO
        if hasattr(self.config, "logging") and self.config.logging.get("debug", False):
            log_level = logging.DEBUG

        logging.basicConfig(
            level=log_level,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler("documentation_pipeline.log"),
            ],
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("Documentation pipeline initialized")

    def create_pipeline(self):
        """Create the LangGraph pipeline."""
        workflow = StateGraph(PipelineState)

        # Add nodes
        workflow.add_node("load_existing_docs", self.load_existing_docs)
        workflow.add_node(
            "load_existing_documentation", self.load_existing_documentation
        )
        workflow.add_node("load_documentation_guide", self.load_documentation_guide)
        workflow.add_node("summarize_docs", self.summarize_docs)
        workflow.add_node("scan_repository", self.scan_repository)
        workflow.add_node("generate_documentation", self.generate_documentation)
        workflow.add_node(
            "generate_documentation_guide", self.generate_documentation_guide_node
        )  # NEW
        workflow.add_node("generate_design_docs", self.generate_design_documentation)
        workflow.add_node(
            "initialize_design_documents", self.initialize_design_documents
        )
        workflow.add_node("generate_design_section", self.generate_design_section)
        workflow.add_node("assemble_design_document", self.assemble_design_document)
        workflow.add_node("save_results", self.save_results)

        # Add edges
        workflow.set_entry_point("load_existing_docs")

        # First decision: design-docs-only or normal flow
        workflow.add_conditional_edges(
            "load_existing_docs",
            self.should_load_existing_docs,
            {
                "load_existing": "load_existing_documentation",
                "continue": "check_summarization",
            },
        )

        # Add a separate node for summarization check
        workflow.add_node("check_summarization", self.check_summarization_step)
        workflow.add_conditional_edges(
            "check_summarization",
            self.should_summarize,
            {"summarize": "summarize_docs", "continue": "check_file_generation"},
        )

        # Check if we should generate file documentation
        workflow.add_node("check_file_generation", self.check_file_generation_step)
        workflow.add_conditional_edges(
            "check_file_generation",
            self.should_generate_files,
            {
                "generate": "scan_repository",
                "skip": "check_guide_generation",
            },  # CHANGED
        )

        workflow.add_edge("summarize_docs", "check_file_generation")
        workflow.add_edge("scan_repository", "generate_documentation")
        workflow.add_conditional_edges(
            "generate_documentation",
            self.has_more_files,
            {
                "continue": "generate_documentation",
                "finish": "check_guide_generation",
            },  # CHANGED
        )

        # Guide generation check and flow
        workflow.add_node("check_guide_generation", self.check_guide_generation_step)
        workflow.add_conditional_edges(
            "check_guide_generation",
            self.should_generate_guide,
            {
                "generate": "generate_documentation_guide",
                "skip": "generate_design_docs",
            },
        )

        workflow.add_edge("generate_documentation_guide", "generate_design_docs")

        # Design-docs-only path
        workflow.add_edge("load_existing_documentation", "load_documentation_guide")
        workflow.add_edge("load_documentation_guide", "check_guide_generation")

        # Design docs workflow
        workflow.add_conditional_edges(
            "generate_design_docs",
            self.should_generate_design_docs,
            {"generate": "initialize_design_documents", "skip": "save_results"},
        )

        workflow.add_edge("initialize_design_documents", "generate_design_section")
        workflow.add_conditional_edges(
            "generate_design_section",
            self.has_more_sections,
            {
                "continue": "generate_design_section",
                "assemble": "assemble_design_document",
                "finish": "save_results",
            },
        )

        workflow.add_conditional_edges(
            "assemble_design_document",
            self.has_more_documents,
            {"continue": "initialize_design_documents", "finish": "save_results"},
        )

        workflow.add_edge("save_results", END)

        return workflow.compile()

    # Pipeline node methods - delegate to appropriate managers
    def load_existing_docs(self, state: PipelineState) -> Dict[str, Any]:
        """Load and process existing documentation."""
        print("Loading existing documentation...")

        # Handle optional docs_path
        docs_path = state.request.docs_path
        docs = self.doc_processor.load_existing_docs(docs_path)

        return {"existing_docs": docs}

    def load_existing_documentation(self, state: PipelineState) -> Dict[str, Any]:
        """Load existing documentation files instead of generating new ones."""
        return self.guide_generator.load_existing_documentation(state)

    def generate_documentation_guide_node(self, state: PipelineState) -> Dict[str, Any]:
        """Generate documentation guide as a separate workflow step."""
        if not state.request.guide:
            return {"completed": True}

        print("Generating documentation guide...")
        guide = self.guide_generator.generate_documentation_guide(state)
        self.guide_generator.save_documentation_guide(state, guide)

        # Add guide to existing docs context for design document generation
        if guide and guide.entries:
            enhanced_docs = self.context_manager.enhance_context_with_guide(
                state, guide
            )
            return {"documentation_guide": guide, "existing_docs": enhanced_docs}

        return {"documentation_guide": guide}

    def should_generate_guide(self, state: PipelineState) -> str:
        """Determine if documentation guide should be generated."""
        return "generate" if state.request.guide else "skip"

    def load_documentation_guide(self, state: PipelineState) -> Dict[str, Any]:
        """Load existing documentation guide if available."""
        return self.context_manager.load_documentation_guide(state)

    def summarize_docs(self, state: PipelineState) -> Dict[str, Any]:
        """Summarize existing documentation if it's too large."""
        return self.context_manager.summarize_docs(state)

    def scan_repository(self, state: PipelineState) -> Dict[str, Any]:
        """Scan the repository for code files."""
        print(f"Scanning repository: {state.request.repo_path}")

        code_files = self.code_analyzer.scan_repository(state.request.repo_path)

        # Apply max_files limit if configured
        max_files = state.request.config.processing.get("max_files")
        if max_files and max_files > 0:
            code_files = code_files[:max_files]
            print(f"Limited to {max_files} files (configured maximum)")

        print(f"Found {len(code_files)} code files to document")

        return {"code_files": code_files, "current_file_index": 0}

    def generate_documentation(self, state: PipelineState) -> Dict[str, Any]:
        """Generate documentation for the current code file with enhanced error handling."""
        if state.current_file_index >= len(state.code_files):
            return {"completed": True}

        current_file = state.code_files[state.current_file_index]
        total_files = len(state.code_files)
        current_index = state.current_file_index + 1

        self.logger.info(
            f"Processing file {current_index}/{total_files}: {current_file.relative_path}"
        )
        print(
            f"Processing file: {current_file.relative_path} ({current_index}/{total_files})"
        )

        # Check if we should generate documentation for this file
        if not self.file_processor.should_generate_documentation(
            state, current_file, self.guide_generator
        ):
            self.logger.info(f"Skipping unchanged file: {current_file.relative_path}")
            # Create a "skipped" result to track that we processed this file
            result = DocumentationResult(
                file_path=current_file.path,
                documentation="[SKIPPED - No changes detected]",
                success=True,
                error_message=None,
            )

            # Update results and move to next file
            new_results = state.results + [result]
            new_index = state.current_file_index + 1
            return {"results": new_results, "current_file_index": new_index}

        self.logger.info(f"Generating documentation for: {current_file.relative_path}")
        print(f"  → Generating documentation...")

        try:
            # Prepare context
            context = self.doc_processor.prepare_context(state.existing_docs)

            # Create documentation prompt
            doc_prompt = ChatPromptTemplate.from_messages(
                [
                    SystemMessage(
                        content=GENERATED_FILE_DOCUMENTATION_SYSTEM_MESSAGE.format(
                            context=context,
                            current_file_extension=current_file.extension or "text",
                            current_file_relative_path=current_file.relative_path,
                        )
                    ),
                    HumanMessage(
                        content=f"Document this code file:\n\n```{current_file.extension[1:] if current_file.extension else 'text'}\n{current_file.content}\n```"
                    ),
                ]
            )

            messages = doc_prompt.format_messages()
            response = self.llm.invoke(messages)

            # Handle different response types
            if hasattr(response, "content"):
                documentation = response.content
            else:
                documentation = str(response)

            result = DocumentationResult(
                file_path=current_file.path, documentation=documentation, success=True
            )

            # Save immediately if incremental saving is enabled
            save_incrementally = state.request.config.processing.get(
                "save_incrementally", True
            )
            if save_incrementally:
                try:
                    self.file_processor.save_single_result(state, result)
                    self.logger.info(
                        f"Successfully saved documentation for: {current_file.relative_path}"
                    )
                except Exception as save_error:
                    self.logger.error(
                        f"Failed to save documentation for {current_file.relative_path}: {save_error}"
                    )
                    result.success = False
                    result.error_message = f"Save failed: {str(save_error)}"

        except Exception as e:
            error_msg = f"Failed to generate documentation for {current_file.relative_path}: {str(e)}"
            self.logger.error(error_msg, exc_info=True)

            result = DocumentationResult(
                file_path=current_file.path,
                documentation="",
                success=False,
                error_message=str(e),
            )
            print(f"  → Error generating documentation: {e}")

        # Update results and move to next file
        new_results = state.results + [result]
        new_index = state.current_file_index + 1

        # Log progress
        successful_so_far = len([r for r in new_results if r.success])
        failed_so_far = len([r for r in new_results if not r.success])
        self.logger.info(
            f"Progress: {current_index}/{total_files} processed, {successful_so_far} successful, {failed_so_far} failed"
        )

        return {"results": new_results, "current_file_index": new_index}

    def generate_design_documentation(self, state: PipelineState) -> Dict[str, Any]:
        """Generate design documentation from the individual file documentation."""
        if not state.request.design_docs:
            return {"completed": True}

        print("Starting design documentation generation...")

        # Try to load existing documentation guide from well-known location
        # (only if guide wasn't generated in a previous step)
        if not hasattr(state, "documentation_guide") or not state.documentation_guide:
            guide_content = self.context_manager.load_existing_guide_from_file(state)
            if guide_content:
                # Add to existing docs context
                current_content = state.existing_docs.content
                enhanced_content = (
                    f"{current_content}\n\n## Documentation Guide\n{guide_content}"
                )

                enhanced_docs = DocumentationContext(
                    content=enhanced_content,
                    token_count=self.doc_processor.count_tokens(enhanced_content),
                    summarized=state.existing_docs.summarized,
                    original_docs=state.existing_docs.original_docs + [guide_content],
                )

                # Update state with enhanced docs
                state.existing_docs = enhanced_docs

        return {"completed": True}

    def check_guide_generation_step(self, state: PipelineState) -> Dict[str, Any]:
        """Pass-through step for guide generation check."""
        return {}  # No state changes, just a decision point

    def initialize_design_documents(self, state: PipelineState) -> Dict[str, Any]:
        """Initialize the design documentation state with configured documents."""
        return self.design_doc_generator.initialize_design_documents(state)

    def generate_design_section(self, state: PipelineState) -> Dict[str, Any]:
        """Generate a single section of a design document."""
        return self.design_doc_generator.generate_design_section(state)

    def assemble_design_document(self, state: PipelineState) -> Dict[str, Any]:
        """Assemble all sections of a design document into a coherent whole."""
        return self.design_doc_generator.assemble_design_document(state)

    def save_results(self, state: PipelineState) -> Dict[str, Any]:
        """Save the summary report and handle any remaining non-incremental saves."""
        return self.report_generator.save_results(state, self.file_processor)

    # State management methods - delegate to StateManager
    def should_load_existing_docs(self, state: PipelineState) -> str:
        """Determine whether to load existing docs or generate new ones."""
        return self.state_manager.should_load_existing_docs(state)

    def should_summarize(self, state: PipelineState) -> str:
        """Determine if documentation needs summarization."""
        return self.state_manager.should_summarize(state, self.doc_processor)

    def should_generate_files(self, state: PipelineState) -> str:
        """Determine if file documentation should be generated."""
        return self.state_manager.should_generate_files(state)

    def should_generate_design_docs(self, state: PipelineState) -> str:
        """Determine if design documentation should be generated."""
        return self.state_manager.should_generate_design_docs(state)

    def has_more_files(self, state: PipelineState) -> str:
        """Check if there are more files to process."""
        return self.state_manager.has_more_files(state)

    def has_more_sections(self, state: PipelineState) -> str:
        """Check if there are more sections to process in the current document."""
        return self.state_manager.has_more_sections(state)

    def has_more_documents(self, state: PipelineState) -> str:
        """Check if there are more documents to process."""
        return self.state_manager.has_more_documents(state)

    def check_summarization_step(self, state: PipelineState) -> Dict[str, Any]:
        """Pass-through step for summarization check."""
        return self.state_manager.check_summarization_step(state)

    def check_file_generation_step(self, state: PipelineState) -> Dict[str, Any]:
        """Pass-through step for file generation check."""
        return self.state_manager.check_file_generation_step(state)

    def run(
        self,
        repo_path: Path,
        docs_path: Optional[Path] = None,
        output_path: Optional[Path] = None,
        file_docs: bool = False,
        design_docs: bool = False,
        guide: bool = False,
    ) -> PipelineState:
        """Run the complete documentation pipeline."""

        if output_path is None:
            output_path = repo_path / "documentation_output"

        # Validate that at least one action is specified
        if not (file_docs or design_docs or guide):
            raise ValueError(
                "Must specify at least one of --file-docs, --design-docs, or --guide"
            )

        request = DocumentationRequest(
            repo_path=repo_path,
            docs_path=docs_path,
            output_path=output_path,
            config=self.config,
            file_docs=file_docs,
            design_docs=design_docs,
            guide=guide,
        )

        # Create initial state with empty existing_docs
        initial_docs = DocumentationContext(
            content="", token_count=0, summarized=False, original_docs=[]
        )

        initial_state = PipelineState(request=request, existing_docs=initial_docs)

        pipeline = self.create_pipeline()
        model_config = self.config_manager.get_model_config()
        final_state = pipeline.invoke(
            initial_state,
            config={"recursion_limit": model_config.get("recursion_limit", 50)},
        )

        return final_state
