#!/usr/bin/env python3
"""
Example usage of the Documentation Pipeline
"""

from pathlib import Path
import sys

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from pipeline import DocumentationPipeline


def example_basic_usage():
    """Example of basic pipeline usage."""
    print("📝 Example: Basic Documentation Generation")
    print("=" * 50)
    
    # Initialize pipeline
    pipeline = DocumentationPipeline("config.yaml")
    
    # Define paths (adjust these to your actual paths)
    repo_path = Path("./example_repo")  # Path to your code repository
    docs_path = Path("./example_docs")  # Path to existing documentation (optional)
    output_path = Path("./generated_docs")  # Where to save generated documentation
    
    print(f"Repository: {repo_path}")
    print(f"Existing docs: {docs_path}")
    print(f"Output: {output_path}")
    
    # Check if paths exist
    if not repo_path.exists():
        print(f"❌ Repository path does not exist: {repo_path}")
        print("   Please create a sample repository or update the path")
        return
    
    try:
        # Run the pipeline
        print("\n🚀 Running documentation pipeline...")
        final_state = pipeline.run(
            repo_path=repo_path,
            docs_path=docs_path if docs_path.exists() else None,
            output_path=output_path
        )
        
        # Show results
        successful = len([r for r in final_state.results if r.success])
        total = len(final_state.results)
        
        print(f"\n✨ Generation completed!")
        print(f"📊 Results: {successful}/{total} files documented")
        print(f"📁 Output saved to: {output_path}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def example_analyze_repository():
    """Example of repository analysis."""
    print("\n🔍 Example: Repository Analysis")
    print("=" * 40)
    
    from src.code_analyzer import CodeAnalyzer
    from src.config import ConfigManager
    
    # Load configuration
    config_manager = ConfigManager("config.yaml")
    config = config_manager.load_config()
    
    # Initialize analyzer
    analyzer = CodeAnalyzer(config)
    
    # Analyze a repository (adjust path as needed)
    repo_path = Path("./src")  # Analyze our own source code
    
    if not repo_path.exists():
        print(f"❌ Path does not exist: {repo_path}")
        return
    
    try:
        print(f"Analyzing: {repo_path}")
        code_files = analyzer.scan_repository(repo_path)
        structure = analyzer.analyze_file_structure(code_files)
        
        print(f"\n📊 Analysis Results:")
        print(f"Total files: {structure['total_files']}")
        
        print(f"\nBy extension:")
        for ext, count in structure['by_extension'].items():
            print(f"  {ext}: {count}")
        
        print(f"\nLargest files:")
        for file_path, size in structure['largest_files'][:3]:
            print(f"  {file_path}: {size:,} characters")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def example_document_processing():
    """Example of document processing."""
    print("\n📚 Example: Document Processing")
    print("=" * 40)
    
    from src.document_processor import DocumentProcessor
    from src.config import ConfigManager
    
    # Load configuration
    config_manager = ConfigManager("config.yaml")
    config = config_manager.load_config()
    
    # Initialize processor
    processor = DocumentProcessor(config)
    
    # Example text
    sample_text = """
    # Sample Documentation
    
    This is a sample documentation file that demonstrates the token counting
    and processing capabilities of the documentation processor.
    
    ## Features
    - Token counting using tiktoken
    - Text chunking for large documents
    - Support for multiple file formats
    
    ## Usage
    The processor can handle various documentation formats and prepare them
    for use as context in the AI-powered documentation generation pipeline.
    """
    
    # Count tokens
    token_count = processor.count_tokens(sample_text)
    print(f"Sample text token count: {token_count}")
    
    # Create chunks
    chunks = processor.create_chunks(sample_text)
    print(f"Number of chunks: {len(chunks)}")
    
    for i, chunk in enumerate(chunks):
        chunk_tokens = processor.count_tokens(chunk)
        print(f"  Chunk {i+1}: {chunk_tokens} tokens")


def main():
    """Run all examples."""
    print("🚀 Documentation Pipeline Examples")
    print("=" * 60)
    
    try:
        # Check configuration
        from src.config import ConfigManager
        config_manager = ConfigManager("config.yaml")
        config = config_manager.load_config()
        print("✅ Configuration loaded successfully")
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        print("Please make sure config.yaml exists and is properly formatted.")
        return
    
    # Run examples
    example_analyze_repository()
    example_document_processing()
    
    # Note about basic usage
    print(f"\n💡 To run the full documentation generation:")
    print(f"   python main.py --repo-path /path/to/your/repository")
    print(f"   python main.py --help  # for more options")


if __name__ == "__main__":
    main()
