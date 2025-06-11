from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate

from .utilities.token_manager import TokenCounter

from .prompts.continue_truncated_content_system_prompt import (
    CONTINUE_TRUNCATED_CONTENT_SYSTEM_PROMPT,
)
from .prompts.section_prompt_system_message import SECTION_PROMPT_SYSTEM_MESSAGE

from .tools.lc_tools.lc_file_tools import create_file_tools


from .models import (
    PipelineState,
    DesignDocument,
    DesignDocumentSection,
    DesignDocumentationState,
    DocumentationContext,
)

class DesignDocumentGenerator:
    """Handles generation of comprehensive design documentation."""

    def __init__(self, llm, config, doc_processor):
        self.llm = llm
        self.config = config
        self.doc_processor = doc_processor
        self.token_counter = TokenCounter()

    def initialize_design_documents(self, state: PipelineState) -> Dict[str, Any]:
        """Initialize the design documentation state with configured documents."""
        print("Initializing design documentation generation...")

        design_config = self.config.design_docs.get("documents", {})
        documents = []

        for doc_name, doc_config in design_config.items():
            # Check if the document type is enabled
            if not doc_config.get("enabled", True):
                print(f"Skipping disabled document type: {doc_name}")
                continue

            sections = []

            for section_config in doc_config.get("sections", []):
                if section_config.get("enabled", True):
                    section = DesignDocumentSection(
                        name=section_config["name"],
                        enabled=section_config["enabled"],
                        max_tokens=section_config["max_tokens"],
                        template=section_config["template"],
                    )
                    sections.append(section)

            if sections:  # Only add document if it has enabled sections
                document = DesignDocument(name=doc_name, sections=sections)
                documents.append(document)
                print(
                    f"Enabled document type: {doc_name} with {len(sections)} sections"
                )
            else:
                print(f"Skipping document type {doc_name}: no enabled sections")

        design_state = DesignDocumentationState(
            documents=documents,
            current_document_index=0,
            current_section_index=0,
            accumulated_context="",
        )

        print(f"Initialized {len(documents)} design documents for generation")
        return {"design_documentation_state": design_state}

    def generate_design_section(self, state: PipelineState) -> Dict[str, Any]:
        """Generate a single section of a design document."""
        design_state = state.design_documentation_state
        if not design_state or design_state.current_document_index >= len(
            design_state.documents
        ):
            return {"design_documentation_state": design_state}

        current_doc = design_state.documents[design_state.current_document_index]
        current_section = current_doc.sections[design_state.current_section_index]

        print(
            f"Generating section '{current_section.name}' for document '{current_doc.name}'..."
        )

        # Prepare context for section generation
        context = self._prepare_section_context(state, current_doc, current_section)

        # Generate the section content
        section_content = self._generate_section_content(
            state, current_doc, current_section, context
        )

        # Update section with generated content
        current_section.content = section_content
        current_section.success = True

        # Move to next section
        design_state.current_section_index += 1

        return {"design_documentation_state": design_state}

    def _prepare_section_context(
        self,
        state: PipelineState,
        document: DesignDocument,
        section: DesignDocumentSection,
    ) -> str:
        """Prepare context for section generation including previous sections and documents."""
        context_parts = []

        # Add existing documentation context
        if state.existing_docs.content:
            context_parts.append("## Existing Project Documentation")
            context_parts.append(state.existing_docs.content)

        # Add accumulated context from previous documents
        if state.design_documentation_state.accumulated_context:
            context_parts.append("## Previously Generated Design Documents")
            context_parts.append(state.design_documentation_state.accumulated_context)

        # Add previous sections from current document
        previous_sections = []
        for i in range(state.design_documentation_state.current_section_index):
            prev_section = document.sections[i]
            if prev_section.content:
                previous_sections.append(f"### {prev_section.name}")
                previous_sections.append(prev_section.content)

        if previous_sections:
            context_parts.append(f"## Previous Sections from {document.name}")
            context_parts.extend(previous_sections)

        return "\n\n".join(context_parts)

    def _generate_section_content(
        self,
        state: PipelineState,
        document: DesignDocument,
        section: DesignDocumentSection,
        context: str,
    ) -> str:
        """Generate content for a specific section with retry logic."""
        max_retries = self.config.design_docs.get("retry_count", 3)

        for attempt in range(max_retries + 1):
            try:
                # Create tools for the AI to use
                tools = self._create_langchain_tools(state.request.repo_path)

                # Bind tools to the LLM
                llm_with_tools = self.llm.bind_tools(tools)

                # Create the generation prompt
                prompt = self._create_section_prompt(document, section, context)

                # Generate content
                response = llm_with_tools.invoke(prompt, max_tokens=section.max_tokens)

                if hasattr(response, "content"):
                    content = response.content
                else:
                    content = str(response)

                # Check if content was truncated
                if self._is_content_truncated(content, section.max_tokens):
                    retry_config = self.config.design_docs.get("retry", {})
                    if retry_config.get("retry_on_truncation", True):
                        print(
                            f"  → Content truncated, retrying with continuation (attempt {attempt + 1})"
                        )
                        content = self._continue_truncated_content(
                            content, document, section, context, tools, retry_config
                        )

                section.retry_count = attempt
                return content

            except Exception as e:
                section.retry_count = attempt
                print(f"  → Error generating section (attempt {attempt + 1}): {e}")

                if attempt == max_retries:
                    section.success = False
                    section.error_message = str(e)
                    return f"[GENERATION FAILED: {str(e)}]"

        return "[GENERATION FAILED: Maximum retries exceeded]"

    def _create_langchain_tools(self, repo_path: Path):
        """Create LangChain tools for the AI to use."""
        return create_file_tools(repo_path)

    def _create_section_prompt(
        self, document: DesignDocument, section: DesignDocumentSection, context: str
    ) -> List:
        """Create the prompt for section generation."""
        system_message = SECTION_PROMPT_SYSTEM_MESSAGE.format(
            document_name=document.name,
            section_name=section.name,
            section_template=section.template,
            context=context,
        )

        return [
            SystemMessage(content=system_message),
            HumanMessage(
                content=f"Generate the '{section.name}' section for the {document.name} document."
            ),
        ]

    def _is_content_truncated(self, content: str, max_tokens: int) -> bool:
        """Check if content appears to be truncated."""
        # Simple heuristic: if content ends abruptly without proper conclusion
        content = content.strip()

        # Check if content ends mid-sentence or without proper punctuation
        if not content:
            return True

        last_char = content[-1]
        if last_char not in ".!?":
            return True

        # Check token count (approximate, not using model-specific tokenization)
        estimated_tokens = self.token_counter.count_tokens(content)
        if (
            estimated_tokens >= max_tokens * 0.95
        ):  # If using 95% of tokens, likely truncated
            return True

        return False

    def _continue_truncated_content(
        self,
        partial_content: str,
        document: DesignDocument,
        section: DesignDocumentSection,
        context: str,
        tools,
        retry_config: Dict,
    ) -> str:
        """Continue generation from truncated content."""
        continuation_prompt_template = retry_config.get(
            "continuation_prompt",
            "The previous generation was truncated. Please continue exactly where it left off: {previous_content}",
        )

        continuation_prompt = continuation_prompt_template.format(
            previous_content=partial_content
        )

        # Include full context in the continuation system message
        system_message = CONTINUE_TRUNCATED_CONTENT_SYSTEM_PROMPT.format(
            document_name=document.name,
            section_name=section.name,
            context=context,
            section_template=section.template,
            continuation_prompt=continuation_prompt,
        )

        prompt = [
            SystemMessage(content=system_message),
            HumanMessage(content="Continue and complete the section."),
        ]

        try:
            # Bind tools to LLM for continuation as well
            llm_with_tools = self.llm.bind_tools(tools)
            response = llm_with_tools.invoke(prompt, max_tokens=section.max_tokens // 2)

            if hasattr(response, "content"):
                continuation = response.content
            else:
                continuation = str(response)

            return partial_content + "\n" + continuation

        except Exception as e:
            print(f"  → Error continuing truncated content: {e}")
            return partial_content + f"\n\n[CONTINUATION FAILED: {str(e)}]"

    def assemble_design_document(self, state: PipelineState) -> Dict[str, Any]:
        """Assemble all sections of a design document into a coherent whole."""
        design_state = state.design_documentation_state
        current_doc = design_state.documents[design_state.current_document_index]

        print(f"Assembling design document: {current_doc.name}")

        # Collect all successful sections
        sections_content = []
        for section in current_doc.sections:
            if section.success and section.content:
                sections_content.append(f"## {section.name.replace('_', ' ').title()}")
                sections_content.append(section.content)
            elif not section.success:
                sections_content.append(f"## {section.name.replace('_', ' ').title()}")
                sections_content.append(
                    f"[Section generation failed: {section.error_message}]"
                )

        # Use AI to assemble and ensure coherence
        assembled_content = self._ai_assemble_document(current_doc, sections_content)

        # Save the document
        self._save_design_document(state, current_doc, assembled_content)

        # Add to accumulated context for next documents
        design_state.accumulated_context += (
            f"\n\n## {current_doc.name}\n{assembled_content}"
        )
        design_state.completed_documents.append(current_doc.name)

        # Move to next document
        design_state.current_document_index += 1
        design_state.current_section_index = 0

        current_doc.assembled_content = assembled_content
        current_doc.success = True

        return {"design_documentation_state": design_state}

    def _ai_assemble_document(
        self, document: DesignDocument, sections_content: List[str]
    ) -> str:
        """Use AI to assemble sections into a coherent document."""
        combined_sections = "\n\n".join(sections_content)

        assembly_prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content=f"""You are assembling a {document.name} document from individual sections.

Your task is to:
1. Create a coherent document title and introduction
2. Ensure smooth transitions between sections
3. Add any necessary connecting text
4. Maintain consistency in tone and style
5. Add a conclusion if appropriate

The document should read as a unified whole, not just concatenated sections."""
                ),
                HumanMessage(
                    content=f"Assemble this {document.name} document from these sections:\n\n{combined_sections}"
                ),
            ]
        )

        try:
            response = self.llm.invoke(assembly_prompt.format_messages())

            if hasattr(response, "content"):
                return response.content
            else:
                return str(response)

        except Exception as e:
            print(f"  → Error assembling document, using basic concatenation: {e}")
            # Fallback to basic assembly
            title = document.name.replace("_", " ").title()
            return f"# {title}\n\n{combined_sections}"

    def _save_design_document(
        self, state: PipelineState, document: DesignDocument, content: str
    ):
        """Save a design document to file."""
        design_docs_path = state.request.output_path / "design_documentation"
        design_docs_path.mkdir(parents=True, exist_ok=True)

        filename = f"{document.name}.md"
        file_path = design_docs_path / filename

        # Add metadata header
        header = f"""<!-- AUTO-GENERATED DESIGN DOCUMENT -->
<!-- Generated on: {datetime.now().isoformat()} -->
<!-- Document: {document.name} -->

"""

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(header + content)

        document.file_path = file_path
        print(f"  ✓ Saved design document: {file_path}")
