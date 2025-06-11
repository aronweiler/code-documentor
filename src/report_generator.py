import logging
from pathlib import Path

from .models import PipelineState


class ReportGenerator:
    """Handles generation of summary reports and status reporting."""

    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)

    def save_results(self, state: PipelineState, file_processor) -> dict:
        """Save the summary report and handle any remaining non-incremental saves."""
        print(f"Finalizing documentation in: {state.request.output_path}")

        output_path = state.request.output_path
        output_path.mkdir(parents=True, exist_ok=True)

        # Create design documentation directory if design docs were generated
        if state.request.design_docs and state.design_documentation_state:
            design_docs_path = output_path / "design_documentation"
            design_docs_path.mkdir(parents=True, exist_ok=True)

        # Only save individual files if incremental saving was disabled
        save_incrementally = state.request.config.processing.get(
            "save_incrementally", True
        )
        if not save_incrementally:
            print("Saving all documentation files...")
            # Save individual file documentation
            for result in state.results:
                if result.success:
                    file_processor.save_single_result(state, result)

        # Generate summary report
        self.generate_summary_report(state)

        successful_count = len([r for r in state.results if r.success])
        failed_count = len([r for r in state.results if not r.success])

        print(f"Documentation generation completed!")
        print(f"✓ {successful_count} files documented successfully")
        if failed_count > 0:
            print(f"✗ {failed_count} files failed")

        # Report on design documentation if generated
        if state.design_documentation_state:
            self.report_design_documentation_status(state)

        return {"completed": True}

    def report_design_documentation_status(self, state: PipelineState):
        """Report on the status of design documentation generation."""
        design_state = state.design_documentation_state
        if not design_state:
            return

        # Get total configured document types for comparison
        design_config = self.config.design_docs.get("documents", {})
        total_configured = len(design_config)
        enabled_configured = len(
            [doc for doc in design_config.values() if doc.get("enabled", True)]
        )
        disabled_configured = total_configured - enabled_configured

        successful_docs = len([doc for doc in design_state.documents if doc.success])
        failed_docs = len([doc for doc in design_state.documents if not doc.success])
        total_docs = len(design_state.documents)

        print(f"\n🎨 Design Documentation Status:")
        print(
            f"   📋 {total_configured} document types configured, {enabled_configured} enabled, {disabled_configured} disabled"
        )
        print(
            f"   ✓ {successful_docs}/{total_docs} enabled documents generated successfully"
        )

        if failed_docs > 0:
            print(f"   ✗ {failed_docs} documents failed")
            for doc in design_state.documents:
                if not doc.success:
                    print(f"     - {doc.name}: {doc.error_message}")

        # Report section-level details
        total_sections = sum(len(doc.sections) for doc in design_state.documents)
        successful_sections = sum(
            len([s for s in doc.sections if s.success])
            for doc in design_state.documents
        )
        failed_sections = total_sections - successful_sections

        print(f"   📝 {successful_sections}/{total_sections} sections generated")
        if failed_sections > 0:
            print(f"   ⚠️  {failed_sections} sections failed")

    def generate_summary_report(self, state: PipelineState):
        """Generate a summary report of the documentation process."""
        successful = [
            r
            for r in state.results
            if r.success and r.documentation != "[SKIPPED - No changes detected]"
        ]
        skipped = [
            r
            for r in state.results
            if r.success and r.documentation == "[SKIPPED - No changes detected]"
        ]
        failed = [r for r in state.results if not r.success]

        report_content = f"""# Documentation Generation Report

## Summary
- **Total files processed**: {len(state.results)}
- **Successfully documented**: {len(successful)}
- **Skipped (unchanged)**: {len(skipped)}
- **Failed**: {len(failed)}

## Successfully Documented Files
"""

        for result in successful:
            relative_path = result.file_path.relative_to(state.request.repo_path)
            report_content += f"- {relative_path}\n"

        if skipped:
            report_content += "\n## Skipped Files (No Changes)\n"
            for result in skipped:
                relative_path = result.file_path.relative_to(state.request.repo_path)
                report_content += f"- {relative_path}\n"

        if failed:
            report_content += "\n## Failed Files\n"
            for result in failed:
                relative_path = result.file_path.relative_to(state.request.repo_path)
                report_content += f"- {relative_path}: {result.error_message}\n"

        # Add design documentation report
        if state.design_documentation_state:
            report_content += self.generate_design_docs_report_section(state)

        # Add existing documentation info
        if state.existing_docs.content:
            report_content += f"\n## Existing Documentation Context\n"
            report_content += f"- **Token count**: {state.existing_docs.token_count}\n"
            report_content += f"- **Summarized**: {state.existing_docs.summarized}\n"
            report_content += (
                f"- **Original documents**: {len(state.existing_docs.original_docs)}\n"
            )

        # Add processing configuration info
        max_files = state.request.config.processing.get("max_files")
        save_incrementally = state.request.config.processing.get(
            "save_incrementally", True
        )

        report_content += f"\n## Processing Configuration\n"
        report_content += (
            f"- **Max files limit**: {max_files if max_files else 'No limit'}\n"
        )
        report_content += f"- **Incremental saving**: {save_incrementally}\n"
        report_content += f"- **File documentation**: {state.request.file_docs}\n"
        report_content += f"- **Design docs**: {state.request.design_docs}\n"
        report_content += f"- **Documentation guide**: {state.request.guide}\n"

        # Save report
        report_path = state.request.output_path / "documentation_report.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report_content)

        print(f"✓ Summary report saved: {report_path}")

    def generate_design_docs_report_section(self, state: PipelineState) -> str:
        """Generate the design documentation section of the summary report."""
        design_state = state.design_documentation_state
        if not design_state:
            return ""

        # Get configuration info
        design_config = self.config.design_docs.get("documents", {})
        total_configured = len(design_config)
        enabled_configured = len(
            [doc for doc in design_config.values() if doc.get("enabled", True)]
        )
        disabled_configured = total_configured - enabled_configured

        report_section = "\n## Design Documentation\n"

        successful_docs = [doc for doc in design_state.documents if doc.success]
        failed_docs = [doc for doc in design_state.documents if not doc.success]

        report_section += f"- **Total document types configured**: {total_configured}\n"
        report_section += f"- **Enabled document types**: {enabled_configured}\n"
        report_section += f"- **Disabled document types**: {disabled_configured}\n"
        report_section += f"- **Successfully generated**: {len(successful_docs)}\n"
        report_section += f"- **Failed**: {len(failed_docs)}\n"

        # List disabled document types
        if disabled_configured > 0:
            disabled_docs = [
                name
                for name, config in design_config.items()
                if not config.get("enabled", True)
            ]
            report_section += f"\n### Disabled Document Types\n"
            for doc_name in disabled_docs:
                report_section += f"- {doc_name}\n"

        if successful_docs:
            report_section += "\n### Successfully Generated Design Documents\n"
            for doc in successful_docs:
                successful_sections = len([s for s in doc.sections if s.success])
                total_sections = len(doc.sections)
                report_section += f"- **{doc.name}**: {successful_sections}/{total_sections} sections\n"
                if doc.file_path:
                    relative_path = doc.file_path.relative_to(state.request.output_path)
                    report_section += f"  - File: {relative_path}\n"

        if failed_docs:
            report_section += "\n### Failed Design Documents\n"
            for doc in failed_docs:
                report_section += f"- **{doc.name}**: {doc.error_message}\n"

                # Report failed sections
                failed_sections = [s for s in doc.sections if not s.success]
                if failed_sections:
                    report_section += "  - Failed sections:\n"
                    for section in failed_sections:
                        report_section += (
                            f"    - {section.name}: {section.error_message}\n"
                        )

        # Add section-level statistics
        total_sections = sum(len(doc.sections) for doc in design_state.documents)
        successful_sections = sum(
            len([s for s in doc.sections if s.success])
            for doc in design_state.documents
        )

        report_section += f"\n### Section Statistics\n"
        report_section += f"- **Total sections**: {total_sections}\n"
        report_section += f"- **Successful sections**: {successful_sections}\n"
        report_section += (
            f"- **Failed sections**: {total_sections - successful_sections}\n"
        )

        return report_section