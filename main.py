import argparse
import sys
from pathlib import Path
from src.pipeline import DocumentationPipeline
from src.config import ConfigManager
from src.code_analyzer import CodeAnalyzer
from src.document_processor import DocumentProcessor


def main():
    parser = argparse.ArgumentParser(
        description="Generate comprehensive documentation for code repositories",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic documentation generation
  python main.py --repo-path "C:\\path\\to\\repo"

  # With existing documentation as context
  python main.py --repo-path "C:\\path\\to\\repo" --docs-path "C:\\path\\to\\docs"

  # Generate design documentation too
  python main.py --repo-path "C:\\path\\to\\repo" --design-docs

  # Specify custom output location
  python main.py --repo-path "C:\\path\\to\\repo" --output-path "C:\\path\\to\\output"

  # Use custom configuration
  python main.py --repo-path "C:\\path\\to\\repo" --config "custom-config.yaml"

  # Utility commands
  python main.py analyze "C:\\path\\to\\repo"
  python main.py validate-config
        """,
    )

    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Main documentation generation command (default)
    doc_parser = subparsers.add_parser(
        "generate", help="Generate documentation (default)"
    )
    doc_parser.add_argument(
        "--repo-path",
        type=str,
        required=True,
        help="Path to the code repository to document",
    )
    doc_parser.add_argument(
        "--docs-path", type=str, help="Path to existing documentation (used as context)"
    )
    doc_parser.add_argument(
        "--output-path",
        type=str,
        help="Where to save generated documentation (default: repo-path/documentation_output)",
    )
    doc_parser.add_argument(
        "--config",
        type=str,
        default="config.yaml",
        help="Path to configuration file (default: config.yaml)",
    )
    doc_parser.add_argument(
        "--design-docs",
        action="store_true",
        help="Generate design documentation in addition to code documentation",
    )
    doc_parser.add_argument(
        "--design-docs-only",
        action="store_true",
        help="Generate only design documentation (requires existing individual documentation)",
    )
    doc_parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output"
    )

    # Analyze command
    analyze_parser = subparsers.add_parser(
        "analyze", help="Analyze repository structure"
    )
    analyze_parser.add_argument(
        "repo_path", type=str, help="Path to repository to analyze"
    )
    analyze_parser.add_argument(
        "--config", type=str, default="config.yaml", help="Configuration file"
    )

    # Validate config command
    validate_parser = subparsers.add_parser(
        "validate-config", help="Validate configuration"
    )
    validate_parser.add_argument(
        "--config",
        type=str,
        default="config.yaml",
        help="Configuration file to validate",
    )

    # If no command is specified, treat arguments as generate command
    args = parser.parse_args()

    # Handle case where no subcommand is used (backward compatibility)
    if args.command is None:
        # Re-parse with generate command arguments
        parser = argparse.ArgumentParser(
            description="Generate comprehensive documentation for code repositories"
        )
        parser.add_argument(
            "--repo-path",
            type=str,
            required=True,
            help="Path to the code repository to document",
        )
        parser.add_argument(
            "--docs-path",
            type=str,
            help="Path to existing documentation (used as context)",
        )
        parser.add_argument(
            "--output-path",
            type=str,
            help="Where to save generated documentation (default: repo-path/documentation_output)",
        )
        parser.add_argument(
            "--config",
            type=str,
            default="config.yaml",
            help="Path to configuration file (default: config.yaml)",
        )
        parser.add_argument(
            "--design-docs",
            action="store_true",
            help="Generate design documentation in addition to code documentation",
        )
        parser.add_argument(
            "--design-docs-only",
            action="store_true",
            help="Generate only design documentation (requires existing individual documentation)",
        )
        parser.add_argument(
            "--verbose", "-v", action="store_true", help="Enable verbose output"
        )

        args = parser.parse_args()
        args.command = "generate"

    try:
        if args.command == "generate":
            run_documentation_generation(args)
        elif args.command == "analyze":
            run_repository_analysis(args)
        elif args.command == "validate-config":
            run_config_validation(args)
        else:
            parser.print_help()

    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        if hasattr(args, "verbose") and args.verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


def run_documentation_generation(args):
    """Run the main documentation generation pipeline."""

    # Validate design-docs-only flag
    if args.design_docs_only and not args.design_docs:
        raise ValueError("--design-docs-only requires --design-docs flag")

    print("🚀 Starting Documentation Pipeline")
    print("=" * 50)

    # Validate paths
    repo_path = Path(args.repo_path)
    if not repo_path.exists():
        raise ValueError(f"Repository path does not exist: {repo_path}")

    docs_path = None
    if args.docs_path:
        docs_path = Path(args.docs_path)
        if not docs_path.exists():
            raise ValueError(f"Documentation path does not exist: {docs_path}")

    output_path = None
    if args.output_path:
        output_path = Path(args.output_path)

    # Initialize pipeline
    print(f"📁 Repository: {repo_path}")
    print(f"📚 Existing docs: {docs_path if docs_path else 'None'}")
    print(
        f"📤 Output: {output_path if output_path else repo_path / 'documentation_output'}"
    )
    print(f"🎨 Design docs: {'Yes' if args.design_docs else 'No'}")
    print(f"🎯 Design docs only: {'Yes' if args.design_docs_only else 'No'}")
    print(f"⚙️  Config: {args.config}")
    print()

    try:
        pipeline = DocumentationPipeline(args.config)

        final_state = pipeline.run(
            repo_path=repo_path,
            docs_path=docs_path,
            output_path=output_path,
            generate_design_docs=args.design_docs,
            design_docs_only=args.design_docs_only,
        )

        # Print summary
        successful = len(
            [
                r
                for r in final_state.results
                if r.success and r.documentation != "[SKIPPED - No changes detected]"
            ]
        )
        skipped = len(
            [
                r
                for r in final_state.results
                if r.success and r.documentation == "[SKIPPED - No changes detected]"
            ]
        )
        failed = len([r for r in final_state.results if not r.success])

        print("\n" + "=" * 50)
        print("✅ Documentation Pipeline Completed!")
        print(f"📊 Results: {successful} generated, {skipped} skipped, {failed} failed")

        if (
            args.design_docs
            and hasattr(final_state, "documentation_guide")
            and final_state.documentation_guide
        ):
            print(
                f"📋 Documentation guide created with {final_state.documentation_guide.total_files} entries"
            )

        if args.design_docs_only:
            print("🎯 Design documentation generated from existing files")
        elif args.design_docs:
            print("📝 Individual + design documentation completed")
        else:
            print("📝 Individual documentation completed")

        if failed > 0:
            print(
                "⚠️  Some files failed to process. Check the documentation report for details."
            )

    except Exception as e:
        print(f"❌ Pipeline failed: {e}")
        raise


def run_repository_analysis(args):
    """Analyze repository structure without generating documentation."""
    print("🔍 Analyzing Repository Structure")
    print("=" * 50)

    repo_path = Path(args.repo_path)
    if not repo_path.exists():
        raise ValueError(f"Repository path does not exist: {repo_path}")

    try:
        # Load configuration
        config_manager = ConfigManager(args.config)
        config = config_manager.load_config()

        # Analyze repository
        analyzer = CodeAnalyzer(config)
        code_files = analyzer.scan_repository(repo_path)
        structure = analyzer.analyze_file_structure(code_files)

        # Print results
        print(f"📁 Repository: {repo_path}")
        print(f"📊 Total files found: {structure['total_files']}")
        print()

        print("📋 Files by extension:")
        for ext, count in sorted(structure["by_extension"].items()):
            print(f"  {ext or '(no extension)'}: {count} files")
        print()

        print("📂 Files by directory:")
        for directory, count in sorted(structure["by_directory"].items()):
            print(f"  {directory}: {count} files")
        print()

        print("📏 Largest files:")
        for file_path, size in structure["largest_files"][:10]:
            print(f"  {file_path}: {size:,} characters")

        # Check processing limits
        max_files = config.processing.get("max_files")
        if max_files and max_files > 0:
            print(f"\n⚙️  Processing limit: {max_files} files (configured maximum)")
            if structure["total_files"] > max_files:
                print(f"   Only the first {max_files} files would be processed")

    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        raise


def run_config_validation(args):
    """Validate configuration file and API keys."""
    print("🔧 Validating Configuration")
    print("=" * 50)

    try:
        config_manager = ConfigManager(args.config)
        config = config_manager.load_config()

        print(f"✅ Configuration file loaded: {args.config}")

        # Validate model configuration
        model_config = config_manager.get_model_config()
        provider = model_config.get("provider", "openai")
        model_name = model_config.get("name", "unknown")

        print(f"🤖 AI Provider: {provider}")
        print(f"📝 Model: {model_name}")
        print(f"🌡️  Temperature: {model_config.get('temperature', 0.2)}")

        # Test API key
        try:
            api_key = config_manager.get_api_key(provider)
            masked_key = (
                api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "***"
            )
            print(f"🔑 API Key: {masked_key} ✅")
        except Exception as e:
            print(f"🔑 API Key: ❌ {e}")

        # Validate processing configuration
        processing_config = config.processing
        max_files = processing_config.get("max_files")
        save_incrementally = processing_config.get("save_incrementally", True)

        print(f"⚙️  Max files: {max_files if max_files else 'No limit'}")
        print(f"💾 Incremental saving: {save_incrementally}")

        # Validate file processing
        file_config = config.file_processing
        supported_extensions = file_config.get("supported_extensions", [])
        exclude_patterns = file_config.get("exclude_patterns", [])

        print(f"📁 Supported extensions: {len(supported_extensions)} configured")
        print(f"🚫 Exclude patterns: {len(exclude_patterns)} configured")

        # Validate design docs configuration
        design_config = config.design_docs
        if design_config:
            print(f"🎨 Design docs enabled: {design_config.get('enabled', False)}")

        print("\n✅ Configuration validation completed successfully!")

    except Exception as e:
        print(f"❌ Configuration validation failed: {e}")
        raise


if __name__ == "__main__":
    main()
