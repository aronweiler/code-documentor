from typing import Dict, Any

from .models import PipelineState


class StateManager:
    """Handles pipeline state transitions and conditional logic."""

    def __init__(self, config):
        self.config = config

    def should_load_existing_docs(self, state: PipelineState) -> str:
        """Determine whether to load existing docs or generate new ones."""
        # If we're only generating guides or design docs (not file docs), 
        # we need to load existing documentation
        if not state.request.file_docs and (state.request.guide or state.request.design_docs):
            return "load_existing"
        return "continue"

    def should_summarize(self, state: PipelineState, doc_processor) -> str:
        """Determine if documentation needs summarization."""
        if doc_processor.needs_summarization(state.existing_docs):
            return "summarize"
        return "continue"

    def should_generate_files(self, state: PipelineState) -> str:
        """Determine if file documentation should be generated."""
        if state.request.file_docs:
            return "generate"
        return "skip"

    def should_generate_design_docs(self, state: PipelineState) -> str:
        """Determine if design documentation should be generated."""
        if state.request.design_docs:
            return "generate"
        return "skip"

    def has_more_files(self, state: PipelineState) -> str:
        """Check if there are more files to process."""
        if state.current_file_index >= len(state.code_files):
            return "finish"
        return "continue"

    def has_more_sections(self, state: PipelineState) -> str:
        """Check if there are more sections to process in the current document."""
        design_state = state.design_documentation_state
        if not design_state:
            return "finish"

        current_doc = design_state.documents[design_state.current_document_index]

        # Check if current section is complete
        if design_state.current_section_index < len(current_doc.sections):
            return "continue"

        # Current document sections are complete, check if we need to assemble
        if not current_doc.assembled_content:
            return "assemble"

        # Document is complete, check if there are more documents
        if design_state.current_document_index + 1 < len(design_state.documents):
            return "next_document"

        return "finish"

    def has_more_documents(self, state: PipelineState) -> str:
        """Check if there are more documents to process."""
        design_state = state.design_documentation_state
        if not design_state:
            return "finish"

        if design_state.current_document_index + 1 < len(design_state.documents):
            return "continue"

        return "finish"

    def check_summarization_step(self, state: PipelineState) -> Dict[str, Any]:
        """Pass-through step for summarization check."""
        return {}

    def check_file_generation_step(self, state: PipelineState) -> Dict[str, Any]:
        """Pass-through step for file generation check."""
        return {}