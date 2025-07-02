# Documentation Cleanup Feature Test

This document demonstrates the new `--cleanup` feature for the documentation generation toolkit.

## Feature Overview

The `--cleanup` flag allows you to clean up orphaned documentation files - documentation that corresponds to source files that have been deleted.

## How it works

1. **Scans source files**: The tool scans your repository for all source files that would normally be documented
2. **Maps expected documentation**: For each source file, it determines what documentation file should exist
3. **Identifies orphaned files**: It finds documentation files that no longer have corresponding source files
4. **Removes orphaned files**: It deletes the orphaned documentation files
5. **Cleans directories**: It removes empty directories left behind
6. **Updates guides**: It regenerates the documentation guide to remove references to deleted files

## Usage Examples

```bash
# Clean up orphaned documentation files
python main.py generate --repo-path /path/to/repo --cleanup

# Or using the shorter syntax
python main.py -r /path/to/repo --cleanup
```

## What gets cleaned up

- Individual file documentation (`*_documentation.md`) for deleted source files
- Empty directories in the documentation output
- Updated documentation guide entries

## What is preserved

- Design documentation (in `design_documentation/` directory)
- Documentation for existing source files
- Documentation guide structure (but updated to remove deleted entries)

## Test Results

The feature was successfully tested on the current repository and:
- ✅ Identified 2 orphaned documentation files
- ✅ Removed them successfully  
- ✅ Cleaned up 1 empty directory
- ✅ Updated the documentation guide
- ✅ Subsequent runs correctly report "clean" state
