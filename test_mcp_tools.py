#!/usr/bin/env python3
"""
Test script for MCP tools to validate implementation.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path to import our modules
sys.path.append(str(Path(__file__).parent / "src"))

from mcp_manager import MCPManager


async def test_relevant_files():
    """Test the get_relevant_files functionality."""
    print("Testing get_relevant_files tool...")
    
    try:
        # Initialize MCP manager
        mcp_manager = MCPManager()
        
        # Test query
        description = "files related to user authentication and login functionality"
        repo_path = Path(".")
        
        print(f"Query: {description}")
        print("Processing...")
        
        # Run the test
        result = await mcp_manager.find_relevant_files(
            description=description,
            repo_path=repo_path,
            max_results=5
        )
        
        print(f"\nResults:")
        print(f"  Query: {result.query_description}")
        print(f"  Files found: {len(result.relevant_files)}")
        print(f"  Processing time: {result.processing_time_seconds:.2f}s")
        
        for i, file_result in enumerate(result.relevant_files, 1):
            print(f"\n  {i}. {file_result.file_path}")
            print(f"     Score: {file_result.relevance_score}")
            print(f"     Summary: {file_result.summary}")
            if file_result.reasoning:
                print(f"     Reasoning: {file_result.reasoning}")
        
        return True
        
    except Exception as e:
        print(f"Error testing get_relevant_files: {e}")
        return False


async def test_understand_feature():
    """Test the understand_feature functionality."""
    print("\n" + "="*50)
    print("Testing understand_feature tool...")
    
    try:
        # Initialize MCP manager
        mcp_manager = MCPManager()
        
        # Test query
        feature_description = "documentation generation pipeline workflow"
        repo_path = Path(".")
        
        print(f"Feature: {feature_description}")
        print("Processing...")
        
        # Run the test
        result = await mcp_manager.understand_feature(
            feature_description=feature_description,
            repo_path=repo_path
        )
        
        print(f"\nResults:")
        print(f"  Feature: {result.feature_description}")
        print(f"  Source files used: {len(result.source_documentation_files)}")
        print(f"  Key components: {len(result.key_components)}")
        
        if result.comprehensive_answer:
            print(f"\n  Comprehensive Answer:")
            # Show first 300 characters of the answer
            answer_preview = result.comprehensive_answer[:300] + "..." if len(result.comprehensive_answer) > 300 else result.comprehensive_answer
            print(f"    {answer_preview}")
        
        if result.key_components:
            print(f"\n  Key Components:")
            for i, component in enumerate(result.key_components[:3], 1):  # Show first 3
                print(f"    {i}. {component}")
        
        if result.implementation_details:
            print(f"\n  Implementation Details:")
            details_preview = result.implementation_details[:200] + "..." if len(result.implementation_details) > 200 else result.implementation_details
            print(f"    {details_preview}")
        
        if result.source_documentation_files:
            print(f"\n  Source Documentation Files:")
            for file_path in result.source_documentation_files:
                print(f"    - {file_path}")
        
        return True
        
    except Exception as e:
        print(f"Error testing understand_feature: {e}")
        return False


async def main():
    """Run all tests."""
    print("MCP Tools Test Suite")
    print("="*50)
    
    # Check if documentation guide exists
    doc_guide_path = Path("documentation_output/documentation_guide.md")
    if not doc_guide_path.exists():
        print(f"Warning: Documentation guide not found at {doc_guide_path}")
        print("Please run the documentation generator first:")
        print("  python main.py generate --repo-path . --guide")
        return
    
    # Run tests
    test1_passed = await test_relevant_files()
    test2_passed = await test_understand_feature()
    
    # Summary
    print("\n" + "="*50)
    print("Test Summary:")
    print(f"  get_relevant_files: {'PASSED' if test1_passed else 'FAILED'}")
    print(f"  understand_feature: {'PASSED' if test2_passed else 'FAILED'}")
    
    if test1_passed and test2_passed:
        print("\nAll tests passed! MCP tools are working correctly.")
    else:
        print("\nSome tests failed. Check the error messages above.")


if __name__ == "__main__":
    asyncio.run(main())