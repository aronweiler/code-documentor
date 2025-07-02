import argparse
import sys
from pathlib import Path
from src.pipeline import DocumentationPipeline
from src.config import ConfigManager
from src.code_analyzer import CodeAnalyzer


def main():
    # Check if the first argument looks like a subcommand
    if len(sys.argv) > 1 and sys.argv[1] in ["generate", "analyze", "validate-config"]:
        # Use subcommand parsing
        parser = create_subcommand_parser()
        args = parser.parse_args()
    else:
        # Use direct argument parsing (backward compatibility)
        parser = create_direct_parser()
        args = parser.parse_args()
        args.command = "generate"  # Set default command

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


def add_generate_arguments(parser):
    """Add common generate command arguments to a parser."""
    parser.add_argument(
        "--repo-path",
        "-r",
        type=str,
        required=True,
        help="Path to the code repository to document",
    )
    parser.add_argument(
        "--docs-path",
        "-d",
        type=str,
        help="Path to existing documentation (used as context)",
    )
    parser.add_argument(
        "--output-path",
        "-o",
        type=str,
        help="Where to save generated documentation (default: repo-path/documentation_output)",
    )
    parser.add_argument(
        "--config",
        "-c",
        type=str,
        default="config.yaml",
        help="Path to configuration file (default: config.yaml)",
    )
    parser.add_argument(
        "--file-docs",
        "-f",
        action="store_true",
        help="Generate individual file documentation",
    )
    parser.add_argument(
        "--design-docs", "-D", action="store_true", help="Generate design documentation"
    )
    parser.add_argument(
        "--guide", "-g", action="store_true", help="Generate documentation guide"
    )
    parser.add_argument(
        "--force-full-guide", action="store_true", help="Force full guide regeneration (disable incremental updates)"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output"
    )
    parser.add_argument(
        "--cleanup",
        action="store_true",
        help="Clean up orphaned documentation files for deleted source files"
    )


def create_subcommand_parser():
    """Create parser with subcommands."""
    parser = argparse.ArgumentParser(
        description="Generate comprehensive documentation for code repositories",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # File docs only
  python main.py generate -r path/to/repo -f

  # Design docs only
  python main.py generate -r path/to/repo -D

  # Both
  python main.py generate -r path/to/repo -f -D

  # Guide only
  python main.py generate -r path/to/repo -g

  # All
  python main.py generate -r path/to/repo -f -D -g

  # Cleanup orphaned documentation
  python main.py generate -r path/to/repo --cleanup

  # Utility commands
  python main.py analyze path/to/repo
  python main.py validate-config
        """,
    )

    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Generate command
    doc_parser = subparsers.add_parser("generate", help="Generate documentation")
    add_generate_arguments(doc_parser)

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

    return parser


def create_direct_parser():
    """Create parser for direct arguments (backward compatibility)."""
    parser = argparse.ArgumentParser(
        description="Generate comprehensive documentation for code repositories",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # File docs only
  python main.py -r path/to/repo -f

  # Design docs only
  python main.py -r path/to/repo -D

  # Both
  python main.py -r path/to/repo -f -D

  # Guide only
  python main.py -r path/to/repo -g

  # All
  python main.py -r path/to/repo -f -D -g

  # Cleanup orphaned documentation
  python main.py -r path/to/repo --cleanup
        """,
    )

    add_generate_arguments(parser)
    return parser


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


def run_cleanup(args):
    """Run cleanup operation to remove orphaned documentation files."""
    print("🧹 Starting Documentation Cleanup")
    print("=" * 50)

    # Validate paths
    repo_path = Path(args.repo_path)
    if not repo_path.exists():
        raise ValueError(f"Repository path does not exist: {repo_path}")

    output_path = None
    if args.output_path:
        output_path = Path(args.output_path)
    else:
        output_path = repo_path / "documentation_output"

    if not output_path.exists():
        print(f"📁 No documentation output directory found: {output_path}")
        print("✅ Nothing to clean up!")
        return

    print(f"📁 Repository: {repo_path}")
    print(f"📤 Documentation output: {output_path}")
    print()

    try:
        # Load configuration
        from src.config import ConfigManager
        config_manager = ConfigManager(args.config)
        config = config_manager.load_config()

        # Scan repository for existing source files
        print("🔍 Scanning repository for source files...")
        analyzer = CodeAnalyzer(config)
        code_files = analyzer.scan_repository(repo_path)
        
        # Create set of expected documentation file paths
        expected_docs = set()
        for code_file in code_files:
            relative_path = code_file.path.relative_to(repo_path)
            doc_filename = f"{relative_path.stem}_documentation.md"
            expected_doc_path = output_path / relative_path.parent / doc_filename
            expected_docs.add(expected_doc_path)
        
        print(f"✓ Found {len(code_files)} source files")
        print(f"✓ Expecting {len(expected_docs)} documentation files")
        
        # Find all existing documentation files
        print("\n🔍 Scanning documentation directory...")
        existing_docs = set()
        orphaned_docs = []
        
        # Scan for individual file documentation (excluding design docs)
        for doc_file in output_path.rglob("*_documentation.md"):
            # Skip design documentation directory
            if "design_documentation" in str(doc_file.relative_to(output_path)):
                continue
            existing_docs.add(doc_file)
            if doc_file not in expected_docs:
                orphaned_docs.append(doc_file)
        
        print(f"✓ Found {len(existing_docs)} existing documentation files")
        print(f"✓ Found {len(orphaned_docs)} orphaned documentation files")
        
        if not orphaned_docs:
            print("\n✅ No orphaned documentation files found!")
            print("🎉 Documentation directory is clean!")
            return
        
        # Show orphaned files
        print("\n📋 Orphaned documentation files to be removed:")
        for doc_file in orphaned_docs:
            relative_doc_path = doc_file.relative_to(output_path)
            print(f"  🗑️  {relative_doc_path}")
        
        # Remove orphaned files
        print(f"\n🗑️  Removing {len(orphaned_docs)} orphaned files...")
        removed_count = 0
        for doc_file in orphaned_docs:
            try:
                doc_file.unlink()
                print(f"  ✓ Removed: {doc_file.relative_to(output_path)}")
                removed_count += 1
            except Exception as e:
                print(f"  ❌ Failed to remove {doc_file.relative_to(output_path)}: {e}")
        
        # Clean up empty directories
        print("\n🧹 Cleaning up empty directories...")
        empty_dirs_removed = 0
        for parent_dir in output_path.rglob("*"):
            if parent_dir.is_dir() and parent_dir != output_path:
                try:
                    # Skip design_documentation directory
                    if parent_dir.name == "design_documentation":
                        continue
                    if not any(parent_dir.iterdir()):
                        parent_dir.rmdir()
                        print(f"  ✓ Removed empty directory: {parent_dir.relative_to(output_path)}")
                        empty_dirs_removed += 1
                except OSError:
                    # Directory not empty or other error
                    pass
        
        # Update documentation guide if it exists
        guide_path = output_path / "documentation_guide.md"
        if guide_path.exists():
            print("\n📝 Updating documentation guide...")
            try:
                # We'll need to regenerate the guide to remove orphaned entries
                from src.guide_generator import GuideGenerator
                from src.document_processor import DocumentProcessor
                from src.llm_manager import LLMManager
                
                # Initialize components needed for guide regeneration
                llm_manager = LLMManager(config_manager)
                llm = llm_manager.initialize_llm()
                doc_processor = DocumentProcessor(config)
                guide_generator = GuideGenerator(llm, config, doc_processor)
                
                # Load remaining documentation files and regenerate guide
                remaining_results = []
                for doc_file in existing_docs:
                    if doc_file not in orphaned_docs:
                        # Create a mock DocumentationResult for the guide
                        # Extract original file path from metadata if possible
                        try:
                            metadata = guide_generator.extract_metadata_from_doc(doc_file)
                            if metadata and 'relative_path' in metadata:
                                original_path = repo_path / metadata['relative_path']
                            else:
                                # Fallback: guess from doc filename
                                doc_name = doc_file.stem.replace('_documentation', '')
                                original_path = repo_path / doc_file.parent.relative_to(output_path) / f"{doc_name}{doc_file.suffix}"
                            
                            from src.models import DocumentationResult
                            with open(doc_file, 'r', encoding='utf-8') as f:
                                content = f.read()
                            
                            result = DocumentationResult(
                                file_path=original_path,
                                documentation=content,
                                success=True
                            )
                            remaining_results.append(result)
                        except Exception as e:
                            print(f"  ⚠️  Warning: Could not process {doc_file.relative_to(output_path)}: {e}")
                
                # Generate updated guide
                if remaining_results:
                    from src.models import (
                        PipelineState,
                        DocumentationRequest,
                        DocumentationContext
                    )
                    
                    request = DocumentationRequest(
                        repo_path=repo_path,
                        output_path=output_path,
                        config=config,
                        guide=True
                    )
                    state = PipelineState(
                        request=request,
                        existing_docs=DocumentationContext(
                            content="", token_count=0
                        ),
                        results=remaining_results
                    )
                    
                    guide_generator.generate_documentation_guide(state)
                    print("  ✓ Documentation guide updated")
                else:
                    # No remaining files, remove the guide
                    guide_path.unlink()
                    print("  ✓ Documentation guide removed (no remaining files)")
                    
            except Exception as e:
                print(f"  ⚠️  Warning: Could not update documentation guide: {e}")
        
        print("\n" + "=" * 50)
        print("✅ Cleanup completed!")
        print(f"🗑️  Removed {removed_count} orphaned documentation files")
        if empty_dirs_removed > 0:
            print(f"📁 Removed {empty_dirs_removed} empty directories")
        print("🎉 Documentation directory is now clean!")

    except Exception as e:
        print(f"❌ Cleanup failed: {e}")
        raise


def run_documentation_generation(args):
    """Run the main documentation generation pipeline."""

    # Validate flag combinations
    if args.cleanup:
        # Cleanup mode - doesn't require other flags
        pass
    elif not (args.file_docs or args.design_docs or args.guide):
        raise ValueError(
            "Must specify at least one of --file-docs, --design-docs, "
            "--guide, or --cleanup"
        )

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
    print(f"📝 File docs: {'Yes' if args.file_docs else 'No'}")
    print(f"🎨 Design docs: {'Yes' if args.design_docs else 'No'}")
    print(f"🎯 Documentation guide: {'Yes' if args.guide else 'No'}")
    print(f"🔄 Force full guide regeneration: {'Yes' if args.force_full_guide else 'No'}")
    print(f"🧹 Cleanup mode: {'Yes' if args.cleanup else 'No'}")
    print(f"⚙️ Config: {args.config}")
    print()

    try:
        if args.cleanup:
            run_cleanup(args)
            # Continue with normal generation if other flags are specified
            if not (args.file_docs or args.design_docs or args.guide):
                return

        pipeline = DocumentationPipeline(args.config)

        final_state = pipeline.run(
            repo_path=repo_path,
            docs_path=docs_path,
            output_path=output_path,
            file_docs=args.file_docs,
            design_docs=args.design_docs,
            guide=args.guide,
            force_full_guide=args.force_full_guide,
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
            args.guide
            and hasattr(final_state, "documentation_guide")
            and final_state.documentation_guide
        ):
            print(
                f"📋 Documentation guide created with {final_state.documentation_guide.total_files} entries"
            )
        if args.design_docs and args.file_docs:
            print("📝 Individual + design documentation completed")
        elif args.design_docs:
            print("🎨 Design documentation completed")
        elif args.file_docs:
            print("📝 Individual documentation completed")

        if failed > 0:
            print(
                "⚠️  Some files failed to process. Check the documentation report for details."
            )

    except Exception as e:
        print(f"❌ Pipeline failed: {e}")
        raise


if __name__ == "__main__":
    main()
