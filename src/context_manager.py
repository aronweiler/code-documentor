import logging
from typing import Dict, Any, List
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate

from .models import PipelineState, DocumentationContext, DocumentationGuide


class ContextManager:
    """Handles documentation context management, summarization, and guide loading."""

    def __init__(self, config, doc_processor, llm):
        self.config = config
        self.doc_processor = doc_processor
        self.llm = llm
        self.logger = logging.getLogger(__name__)

    def load_documentation_guide(self, state: PipelineState) -> Dict[str, Any]:
        """Load existing documentation guide if available."""
        if not state.request.guide:
            # Check if we should load existing guide for design docs generation
            if state.request.design_docs:
                guide_path = state.request.output_path / "documentation_guide.md"
                if guide_path.exists():
                    try:
                        with open(guide_path, "r", encoding="utf-8") as f:
                            guide_content = f.read()
                        print(
                            f"✓ Loaded existing documentation guide for design docs context"
                        )

                        # Add guide content to existing docs context
                        current_content = state.existing_docs.content
                        enhanced_content = f"{current_content}\n\n## Documentation Guide\n{guide_content}"

                        enhanced_docs = DocumentationContext(
                            content=enhanced_content,
                            token_count=self.doc_processor.count_tokens(
                                enhanced_content
                            ),
                            summarized=state.existing_docs.summarized,
                            original_docs=state.existing_docs.original_docs
                            + [guide_content],
                        )

                        return {"existing_docs": enhanced_docs}

                    except Exception as e:
                        print(
                            f"Warning: Could not load documentation guide from {guide_path}: {e}"
                        )
            return {}

        # Original logic for when guide generation is requested
        guide_path = state.request.output_path / "documentation_guide.md"

        if guide_path.exists():
            try:
                with open(guide_path, "r", encoding="utf-8") as f:
                    guide_content = f.read()
                print(f"✓ Loaded existing documentation guide from {guide_path}")

                # Add guide content to existing docs context
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

                return {"existing_docs": enhanced_docs}

            except Exception as e:
                print(
                    f"Warning: Could not load documentation guide from {guide_path}: {e}"
                )

        return {}

    def summarize_docs(self, state: PipelineState) -> Dict[str, Any]:
        """Summarize existing documentation if it's too large with error handling."""
        self.logger.info("Starting documentation summarization...")
        print("Summarizing existing documentation...")

        docs = state.existing_docs
        chunks = self.doc_processor.create_chunks(docs.content)

        self.logger.info(f"Created {len(chunks)} chunks for summarization")

        summarization_prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content="""You are a technical documentation summarizer. 
Summarize the following documentation chunk while preserving:
1. Key technical concepts and terminology
2. Important architectural decisions
3. Critical implementation details
4. Dependencies and relationships

Keep the summary concise but comprehensive."""
                ),
                HumanMessage(content="Summarize this documentation:\n\n{chunk}"),
            ]
        )

        summaries = []
        failed_chunks = 0

        for i, chunk in enumerate(chunks):
            try:
                self.logger.debug(f"Summarizing chunk {i+1}/{len(chunks)}")
                messages = summarization_prompt.format_messages(chunk=chunk)
                response = self.llm.invoke(messages)

                # Handle different response types
                if hasattr(response, "content"):
                    content = response.content
                else:
                    content = str(response)
                summaries.append(content)

            except Exception as e:
                error_msg = f"Error summarizing chunk {i+1}: {e}"
                self.logger.error(error_msg, exc_info=True)
                print(f"Error summarizing chunk: {e}")
                summaries.append(chunk[:500] + "...")  # Fallback truncation
                failed_chunks += 1

        if failed_chunks > 0:
            self.logger.warning(
                f"{failed_chunks}/{len(chunks)} chunks failed summarization, using fallback truncation"
            )

        summarized_content = "\n\n".join(summaries)
        summarized_docs = DocumentationContext(
            content=summarized_content,
            token_count=self.doc_processor.count_tokens(summarized_content),
            summarized=True,
            original_docs=docs.original_docs,
        )

        self.logger.info(
            f"Summarization complete. Original: {docs.token_count} tokens, Summarized: {summarized_docs.token_count} tokens"
        )
        return {"existing_docs": summarized_docs}

    def format_guide_for_context(self, guide: DocumentationGuide) -> str:
        """Format documentation guide for use as context in design document generation."""
        guide_content = f"""Generated on: {guide.generation_date}
Total documented files: {guide.total_files}

File Documentation Summary:
"""

        for entry in guide.entries:
            guide_content += f"\n### {entry.original_file_path}\n"
            guide_content += f"Documentation: {entry.doc_file_path}\n"
            guide_content += f"Summary: {entry.summary}\n"

        return guide_content

    def enhance_context_with_guide(
        self, state: PipelineState, guide: DocumentationGuide
    ) -> DocumentationContext:
        """Enhance existing documentation context with guide content."""
        if guide and guide.entries:
            guide_content = self.format_guide_for_context(guide)
            current_content = state.existing_docs.content
            enhanced_content = (
                f"{current_content}\n\n## Documentation Guide\n{guide_content}"
            )

            return DocumentationContext(
                content=enhanced_content,
                token_count=self.doc_processor.count_tokens(enhanced_content),
                summarized=state.existing_docs.summarized,
                original_docs=state.existing_docs.original_docs + [guide_content],
            )
        return state.existing_docs

    def load_existing_guide_from_file(self, state: PipelineState) -> str:
        """Load existing documentation guide from well-known location."""
        guide_path = state.request.output_path / "documentation_guide.md"
        if guide_path.exists():
            try:
                with open(guide_path, "r", encoding="utf-8") as f:
                    guide_content = f.read()
                print(f"✓ Loaded existing documentation guide from {guide_path}")
                return guide_content
            except Exception as e:
                print(
                    f"Warning: Could not load documentation guide from {guide_path}: {e}"
                )
        return ""