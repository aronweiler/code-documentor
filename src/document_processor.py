import tiktoken
from typing import List, Tuple, Optional
from pathlib import Path
from .models import DocumentationContext, PipelineConfig
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document


class DocumentProcessor:
    """Handles processing and summarization of existing documentation."""
    
    def __init__(self, config: PipelineConfig):
        self.config = config
        self.encoding = tiktoken.get_encoding("cl100k_base")  # GPT-4 encoding
        
    def count_tokens(self, text: str) -> int:
        """Count the number of tokens in a text string."""
        return len(self.encoding.encode(text))
    
    def load_existing_docs(self, docs_path: Optional[Path]) -> DocumentationContext:
        """Load and process existing documentation files."""
        if not docs_path or not docs_path.exists():
            return DocumentationContext(content="", token_count=0, original_docs=[])
        
        all_docs = []
        supported_formats = ['.md', '.txt', '.rst', '.doc', '.docx']
        
        # Recursively find documentation files
        for file_path in docs_path.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in supported_formats:
                try:
                    content = self._read_file_content(file_path)
                    if content.strip():
                        all_docs.append(content)
                except Exception as e:
                    print(f"Warning: Could not read {file_path}: {e}")
        
        # Combine all documentation
        combined_content = "\n\n".join(all_docs)
        token_count = self.count_tokens(combined_content)
        
        return DocumentationContext(
            content=combined_content,
            token_count=token_count,
            original_docs=all_docs
        )
    
    def _read_file_content(self, file_path: Path) -> str:
        """Read content from a file, handling different encodings."""
        encodings = ['utf-8', 'utf-16', 'cp1252', 'iso-8859-1']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
        
        # If all encodings fail, try binary mode and decode with errors='ignore'
        with open(file_path, 'rb') as f:
            return f.read().decode('utf-8', errors='ignore')
    
    def needs_summarization(self, docs: DocumentationContext) -> bool:
        """Check if documentation needs summarization based on token count."""
        threshold = self.config.token_limits.get("summarization_threshold", 6000)
        return docs.token_count > threshold
    
    def create_chunks(self, text: str) -> List[str]:
        """Split text into chunks for processing."""
        chunk_size = self.config.token_limits.get("chunk_size", 2000)
        
        # Convert token count to approximate character count (1 token ≈ 4 characters)
        char_chunk_size = chunk_size * 4
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=char_chunk_size,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        
        return text_splitter.split_text(text)
    
    def prepare_context(self, docs: DocumentationContext) -> str:
        """Prepare documentation context for use in the pipeline."""
        if not docs.content:
            return "No existing documentation available."
        
        if not self.needs_summarization(docs):
            return docs.content
        
        # If summarization is needed, return a truncated version for now
        # The actual summarization will be handled by the LangGraph pipeline
        max_tokens = self.config.token_limits.get("max_context_tokens", 8000)
        max_chars = max_tokens * 4  # Approximate conversion
        
        if len(docs.content) > max_chars:
            return docs.content[:max_chars] + "\n\n[Content truncated - full summarization available in pipeline]"
        
        return docs.content
