#!/usr/bin/env python3
"""
Documentation Pipeline - Main Entry Point

A LangGraph-based pipeline for automatically generating comprehensive documentation
for code repositories using AI models.
"""

import click
from pathlib import Path
import sys
import os

# Add src to path for imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

try:
    from src.pipeline import DocumentationPipeline
    from src.config import ConfigManager
except ImportError:
    # Fallback for direct execution
    from pipeline import DocumentationPipeline
    from config import ConfigManager


@click.command()
@click.option('--repo-path', required=True, type=click.Path(exists=True, path_type=Path),
              help='Path to the code repository to document')
@click.option('--docs-path', type=click.Path(exists=True, path_type=Path),
              help='Path to existing documentation (optional)')
@click.option('--output-path', type=click.Path(path_type=Path),
              help='Path where documentation will be saved (default: repo-path/documentation_output)')
@click.option('--config', default='config.yaml', type=click.Path(exists=True),
              help='Path to configuration file (default: config.yaml)')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
def main(repo_path: Path, docs_path: Path, output_path: Path, config: str, verbose: bool):
    """
    Generate comprehensive documentation for a code repository using AI.
    
    This tool analyzes a code repository and generates detailed documentation
    for each code file, using existing documentation as context when available.
    """
    
    if verbose:
        click.echo("🚀 Starting Documentation Pipeline")
        click.echo(f"📁 Repository: {repo_path}")
        if docs_path:
            click.echo(f"📚 Existing docs: {docs_path}")
        if output_path:
            click.echo(f"💾 Output: {output_path}")
        else:
            click.echo(f"💾 Output: {repo_path / 'documentation_output'}")
        click.echo(f"⚙️  Config: {config}")
        click.echo()
    
    try:
        # Validate configuration
        config_manager = ConfigManager(config)
        pipeline_config = config_manager.load_config()
        
        if verbose:
            click.echo("✅ Configuration loaded successfully")
            click.echo(f"🤖 Model: {pipeline_config.model.get('provider', 'openai')} - {pipeline_config.model.get('name', 'gpt-4o')}")
        
        # Initialize pipeline
        pipeline = DocumentationPipeline(config)
        
        if verbose:
            click.echo("🔧 Pipeline initialized")
        
        # Run the pipeline
        click.echo("📝 Starting documentation generation...")
        final_state = pipeline.run(
            repo_path=repo_path,
            docs_path=docs_path,
            output_path=output_path
        )
        
        # Show results
        successful = len([r for r in final_state['results'] if r.success])
        total = len(final_state['results'])
        failed = total - successful
        
        click.echo()
        click.echo("✨ Documentation generation completed!")
        click.echo(f"📊 Results: {successful}/{total} files documented successfully")
        
        if failed > 0:
            click.echo(f"⚠️  {failed} files failed to generate documentation")
        
        output_dir = output_path or (repo_path / "documentation_output")
        click.echo(f"📁 Documentation saved to: {output_dir}")
        click.echo(f"📋 See {output_dir / 'documentation_report.md'} for detailed results")
        
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        if verbose:
            import traceback
            click.echo(traceback.format_exc(), err=True)
        sys.exit(1)


@click.group()
def cli():
    """Documentation Pipeline CLI"""
    pass


@cli.command()
@click.option('--config', default='config.yaml', type=click.Path(),
              help='Path to configuration file to validate')
def validate_config(config: str):
    """Validate the configuration file."""
    try:
        config_manager = ConfigManager(config)
        pipeline_config = config_manager.load_config()
        
        click.echo("✅ Configuration file is valid")
        click.echo(f"🤖 Model: {pipeline_config.model.get('provider', 'openai')} - {pipeline_config.model.get('name', 'gpt-4o')}")
        click.echo(f"🎯 Max context tokens: {pipeline_config.token_limits.get('max_context_tokens', 8000)}")
        click.echo(f"📄 Supported extensions: {len(pipeline_config.file_processing.get('supported_extensions', []))}")
        
        # Check API keys
        try:
            provider = pipeline_config.model.get('provider', 'openai')
            api_key = config_manager.get_api_key(provider)
            click.echo(f"🔑 API key for {provider}: {'✅ Found' if api_key else '❌ Missing'}")
        except Exception as e:
            click.echo(f"🔑 API key check: ❌ {str(e)}")
        
    except Exception as e:
        click.echo(f"❌ Configuration error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('repo_path', type=click.Path(exists=True, path_type=Path))
def analyze(repo_path: Path):
    """Analyze a repository without generating documentation."""
    from src.code_analyzer import CodeAnalyzer
    from src.config import ConfigManager
    
    try:
        config_manager = ConfigManager()
        config = config_manager.load_config()
        analyzer = CodeAnalyzer(config)
        
        click.echo(f"🔍 Analyzing repository: {repo_path}")
        
        code_files = analyzer.scan_repository(repo_path)
        structure = analyzer.analyze_file_structure(code_files)
        
        click.echo(f"\n📊 Analysis Results:")
        click.echo(f"📁 Total files: {structure['total_files']}")
        
        click.echo(f"\n📄 By extension:")
        for ext, count in sorted(structure['by_extension'].items()):
            click.echo(f"  {ext}: {count} files")
        
        click.echo(f"\n📂 By directory:")
        for dir_path, count in sorted(structure['by_directory'].items()):
            if dir_path == '.':
                dir_path = '(root)'
            click.echo(f"  {dir_path}: {count} files")
        
        click.echo(f"\n📏 Largest files:")
        for file_path, size in structure['largest_files'][:5]:
            click.echo(f"  {file_path}: {size:,} characters")
        
    except Exception as e:
        click.echo(f"❌ Analysis error: {str(e)}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    # If called with arguments, use the main command
    if len(sys.argv) > 1 and not sys.argv[1] in ['validate-config', 'analyze']:
        main()
    else:
        cli()
