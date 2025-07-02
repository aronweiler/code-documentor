"""
MCP Manager for handling Model Context Protocol operations using LangGraph.
Integrates with existing ConfigManager and LLMManager infrastructure.
"""

import json
import logging
import time
from pathlib import Path
from typing import Dict, Any, List
from langgraph.graph import StateGraph, END
from langchain_core.messages import SystemMessage, HumanMessage

from .config import ConfigManager
from .llm_manager import LLMManager
from .mcp_models import (
    MCPState,
    MCPRelevantFilesResponse,
    MCPFileResult,
    MCPFeatureResponse,
    MCPDocumentationFile,
)
from .prompts.mcp_file_relevance_prompt import (
    MCP_FILE_RELEVANCE_SYSTEM_PROMPT,
    MCP_FEATURE_DISCOVERY_SYSTEM_PROMPT,
    MCP_FEATURE_SYNTHESIS_SYSTEM_PROMPT,
)


class MCPManager:
    """Manager for MCP operations using LangGraph workflow."""

    def __init__(self, config_path: str = "config.yaml"):
        self.config_manager = ConfigManager(config_path)
        self.config = self.config_manager.load_config()

        # Initialize LLM
        self.llm_manager = LLMManager(self.config_manager)
        self.llm = self.llm_manager.initialize_llm()

        self.logger = logging.getLogger(__name__)
        self.logger.info("MCP Manager initialized")

    def create_relevant_files_workflow(self):
        """Create LangGraph workflow for finding relevant files."""
        workflow = StateGraph(MCPState)

        # Add nodes
        workflow.add_node("load_documentation", self.load_documentation_node)
        workflow.add_node("analyze_relevance", self.analyze_file_relevance_node)
        workflow.add_node("format_results", self.format_relevant_files_results_node)

        # Add edges
        workflow.set_entry_point("load_documentation")
        workflow.add_edge("load_documentation", "analyze_relevance")
        workflow.add_edge("analyze_relevance", "format_results")
        workflow.add_edge("format_results", END)

        return workflow.compile()

    def create_feature_understanding_workflow(self):
        """Create LangGraph workflow for understanding features."""
        workflow = StateGraph(MCPState)

        # Add nodes
        workflow.add_node("load_documentation", self.load_documentation_node)
        workflow.add_node(
            "discover_documentation_files", self.discover_documentation_files_node
        )
        workflow.add_node("load_documentation_file", self.load_documentation_file_node)
        workflow.add_node(
            "synthesize_feature_understanding",
            self.synthesize_feature_understanding_node,
        )
        workflow.add_node("format_feature_results", self.format_feature_results_node)

        # Add conditional edges
        workflow.set_entry_point("load_documentation")
        workflow.add_edge("load_documentation", "discover_documentation_files")
        workflow.add_edge("discover_documentation_files", "load_documentation_file")

        # Loop for loading multiple files
        workflow.add_conditional_edges(
            "load_documentation_file",
            self.should_load_more_files,
            {
                "load_more": "load_documentation_file",
                "synthesize": "synthesize_feature_understanding",
            },
        )

        workflow.add_edge("synthesize_feature_understanding", "format_feature_results")
        workflow.add_edge("format_feature_results", END)

        return workflow.compile()

    def load_documentation_node(self, state: MCPState) -> Dict[str, Any]:
        """Load the documentation guide content."""
        try:
            documentation_guide_path = (
                state.repo_path / "documentation_output" / "documentation_guide.md"
            )

            # Debug logging
            debug_log_path = Path("/tmp/mcp_debug.log")
            with open(debug_log_path, "a") as f:
                f.write(
                    f"MCPManager: Looking for doc guide at: {documentation_guide_path}\n"
                )
                f.write(
                    f"MCPManager: File exists: {documentation_guide_path.exists()}\n"
                )
                f.write(f"MCPManager: State repo_path: {state.repo_path}\n")
                f.write(f"MCPManager: State repo_path type: {type(state.repo_path)}\n")

            if documentation_guide_path.exists():
                with open(documentation_guide_path, "r", encoding="utf-8") as f:
                    content = f.read()

                with open(debug_log_path, "a") as f:
                    f.write(
                        f"MCPManager: Successfully loaded {len(content)} characters\n"
                    )

                self.logger.info(
                    f"Loaded documentation guide: {len(content)} characters"
                )
                return {
                    "documentation_guide_content": content,
                    "documentation_loaded": True,
                }
            else:
                with open(debug_log_path, "a") as f:
                    f.write(f"MCPManager: Documentation guide NOT FOUND\n")

                self.logger.warning(
                    f"Documentation guide not found at {documentation_guide_path}"
                )
                return {
                    "documentation_guide_content": "",
                    "documentation_loaded": False,
                    "error_occurred": True,
                    "error_message": f"Documentation guide not found at {documentation_guide_path}",
                }

        except Exception as e:
            with open(debug_log_path, "a") as f:
                f.write(f"MCPManager: Exception in load_documentation_node: {str(e)}\n")

            self.logger.error(f"Error loading documentation: {e}")
            return {
                "documentation_loaded": False,
                "error_occurred": True,
                "error_message": f"Error loading documentation: {str(e)}",
            }

    def analyze_file_relevance_node(self, state: MCPState) -> Dict[str, Any]:
        """Use LLM to analyze file relevance."""
        try:
            # Debug logging
            debug_log_path = Path("/tmp/mcp_debug.log")
            with open(debug_log_path, "a") as f:
                f.write(f"MCPManager: analyze_file_relevance_node called\n")
                f.write(
                    f"MCPManager: documentation_loaded = {state.documentation_loaded}\n"
                )
                if hasattr(state, "documentation_guide_content"):
                    f.write(
                        f"MCPManager: doc content length = {len(state.documentation_guide_content)}\n"
                    )
                else:
                    f.write(f"MCPManager: No documentation_guide_content attribute\n")
                f.write(f"MCPManager: user_query = {state.user_query}\n")

            if not state.documentation_loaded:
                with open(debug_log_path, "a") as f:
                    f.write(f"MCPManager: ERROR - Documentation not loaded\n")
                return {
                    "error_occurred": True,
                    "error_message": "Documentation not loaded, cannot analyze relevance",
                }

            # Debug: Check LLM initialization
            debug_log_path = Path("/tmp/mcp_debug.log")
            with open(debug_log_path, "a") as f:
                f.write(f"MCPManager: LLM object: {self.llm}\n")
                f.write(f"MCPManager: LLM type: {type(self.llm)}\n")

            # Prepare the prompt
            system_message = SystemMessage(content=MCP_FILE_RELEVANCE_SYSTEM_PROMPT)

            user_content = f"""DOCUMENTATION GUIDE:
{state.documentation_guide_content}

USER QUERY: {state.user_query}

Please analyze the documentation and identify the most relevant SOURCE CODE files (not documentation files) for this query. Return your response in the specified JSON format."""

            human_message = HumanMessage(content=user_content)

            with open(debug_log_path, "a") as f:
                f.write(
                    f"MCPManager: About to call LLM with {len(user_content)} characters\n"
                )
                f.write(
                    f"MCPManager: System prompt length: {len(MCP_FILE_RELEVANCE_SYSTEM_PROMPT)}\n"
                )

            # Get LLM response
            try:
                with open(debug_log_path, "a") as f:
                    f.write(f"MCPManager: Calling self.llm.invoke()...\n")

                response = self.llm.invoke([system_message, human_message])

                with open(debug_log_path, "a") as f:
                    f.write(f"MCPManager: LLM invoke completed\n")
                    f.write(f"MCPManager: Response type: {type(response)}\n")
                    f.write(f"MCPManager: Response: {response}\n")

                response_content = response.content

                with open(debug_log_path, "a") as f:
                    f.write(
                        f"MCPManager: Response content type: {type(response_content)}\n"
                    )
                    f.write(
                        f"MCPManager: Response content length: {len(response_content) if response_content else 'None'}\n"
                    )

            except Exception as llm_error:
                with open(debug_log_path, "a") as f:
                    f.write(f"MCPManager: LLM invoke FAILED: {str(llm_error)}\n")
                    f.write(f"MCPManager: LLM error type: {type(llm_error)}\n")
                raise llm_error

            self.logger.info(
                f"LLM analysis complete: {len(response_content)} characters"
            )

            # Parse JSON response
            try:
                # Debug logging - log the raw LLM response
                debug_log_path = Path("/tmp/mcp_debug.log")
                with open(debug_log_path, "a") as f:
                    f.write(f"MCPManager: Raw LLM response: {response_content}\n")

                result_data = json.loads(response_content)

                with open(debug_log_path, "a") as f:
                    f.write(f"MCPManager: Parsed LLM response: {result_data}\n")

                return {
                    "llm_analysis_complete": True,
                    "raw_llm_response": result_data,  # Remove underscore prefix
                }
            except json.JSONDecodeError as e:
                self.logger.error(f"Failed to parse LLM JSON response: {e}")
                self.logger.error(f"Raw response: {response_content}")

                debug_log_path = Path("/tmp/mcp_debug.log")
                with open(debug_log_path, "a") as f:
                    f.write(f"MCPManager: JSON parse error: {str(e)}\n")
                    f.write(f"MCPManager: Raw response: {response_content}\n")

                return {
                    "error_occurred": True,
                    "error_message": f"Failed to parse LLM response as JSON: {str(e)}",
                }

        except Exception as e:
            self.logger.error(f"Error in LLM analysis: {e}")
            return {
                "error_occurred": True,
                "error_message": f"Error in LLM analysis: {str(e)}",
            }

    def format_relevant_files_results_node(self, state: MCPState) -> Dict[str, Any]:
        """Format the results into the final response model."""
        try:
            debug_log_path = Path("/tmp/mcp_debug.log")
            with open(debug_log_path, "a") as f:
                f.write(f"MCPManager: format_relevant_files_results_node called\n")
                f.write(f"MCPManager: state.error_occurred = {state.error_occurred}\n")
                f.write(
                    f"MCPManager: hasattr raw_llm_response = {hasattr(state, 'raw_llm_response')}\n"
                )
                f.write(f"MCPManager: state attributes = {dir(state)}\n")

            if state.error_occurred:
                with open(debug_log_path, "a") as f:
                    f.write(f"MCPManager: Returning early due to error\n")
                return {}  # Error already set, no need to modify state

            raw_response = getattr(state, "raw_llm_response", {})

            with open(debug_log_path, "a") as f:
                f.write(f"MCPManager: raw_response = {raw_response}\n")
                f.write(f"MCPManager: raw_response type = {type(raw_response)}\n")
                f.write(
                    f"MCPManager: relevant_files in raw_response = {'relevant_files' in raw_response}\n"
                )
                if "relevant_files" in raw_response:
                    f.write(
                        f"MCPManager: len(relevant_files) = {len(raw_response['relevant_files'])}\n"
                    )

            # Convert to our response model
            file_results = []
            for file_data in raw_response.get("relevant_files", []):
                file_result = MCPFileResult(
                    file_path=file_data.get("file_path", ""),
                    summary=file_data.get("summary", ""),
                    relevance_score=file_data.get("relevance_score", 0.0),
                    reasoning=file_data.get("reasoning", ""),
                )
                file_results.append(file_result)

            with open(debug_log_path, "a") as f:
                f.write(f"MCPManager: Created {len(file_results)} file_results\n")

            # Limit results to max_results
            if len(file_results) > state.max_results:
                file_results = file_results[: state.max_results]

            response = MCPRelevantFilesResponse(
                query_description=state.user_query,
                relevant_files=file_results,
                total_files_analyzed=raw_response.get(
                    "total_files_analyzed", len(file_results)
                ),
            )

            return {"relevant_files_result": response}

        except Exception as e:
            self.logger.error(f"Error formatting results: {e}")
            return {
                "error_occurred": True,
                "error_message": f"Error formatting results: {str(e)}",
            }

    def discover_documentation_files_node(self, state: MCPState) -> Dict[str, Any]:
        """Use LLM to discover relevant documentation files."""
        try:
            # Debug logging
            debug_log_path = Path("/tmp/mcp_debug.log")
            with open(debug_log_path, "a") as f:
                f.write(f"MCPManager: discover_documentation_files_node called\n")
                f.write(f"MCPManager: documentation_loaded = {state.documentation_loaded}\n")
                f.write(f"MCPManager: LLM object: {self.llm}\n")
                
            if not state.documentation_loaded:
                with open(debug_log_path, "a") as f:
                    f.write(f"MCPManager: ERROR - Documentation not loaded\n")
                return {
                    "error_occurred": True,
                    "error_message": "Documentation not loaded, cannot discover files",
                }

            # Prepare the prompt for file discovery
            system_message = SystemMessage(content=MCP_FEATURE_DISCOVERY_SYSTEM_PROMPT)

            user_content = f"""DOCUMENTATION GUIDE:
{state.documentation_guide_content}

FEATURE TO UNDERSTAND: {state.user_query}

Please analyze the documentation guide and identify which documentation files contain information about this feature. Return your response in the specified JSON format."""

            human_message = HumanMessage(content=user_content)

            with open(debug_log_path, "a") as f:
                f.write(f"MCPManager: About to call LLM for file discovery\n")
                f.write(f"MCPManager: User content length: {len(user_content)}\n")

            # Get LLM response with intelligent retry logic
            max_retries = 3
            retry_count = 0
            messages = [system_message, human_message]
            
            while retry_count < max_retries:
                try:
                    with open(debug_log_path, "a") as f:
                        f.write(f"MCPManager: LLM call attempt {retry_count + 1}/{max_retries}\n")
                    
                    response = self.llm.invoke(messages)
                    response_content = response.content
                    
                    with open(debug_log_path, "a") as f:
                        f.write(f"MCPManager: LLM response received, validating format...\n")
                    
                    # Validate JSON format before cleaning
                    try:
                        # Test if it's valid JSON first
                        json.loads(response_content)
                        # If successful, no need to clean
                        cleaned_response = response_content
                    except json.JSONDecodeError:
                        # Try cleaning backslashes and test again
                        cleaned_response = response_content.replace("\\", "/")
                        try:
                            json.loads(cleaned_response)
                        except json.JSONDecodeError as json_error:
                            # JSON is still invalid, ask LLM to fix it
                            retry_count += 1
                            with open(debug_log_path, "a") as f:
                                f.write(f"MCPManager: JSON validation failed: {str(json_error)}\n")
                                f.write(f"MCPManager: Invalid response: {response_content}\n")
                            
                            if retry_count >= max_retries:
                                raise json_error
                            
                            # Create correction message for LLM
                            correction_message = HumanMessage(content=f"""Your previous response had a JSON formatting error: {str(json_error)}

Your response was:
{response_content}

Please fix the JSON formatting error and provide a valid JSON response that matches the required schema:
{{
  "feature_description": "The user's original feature request",
  "relevant_documentation_files": [
    "documentation_output/path/to/file_documentation.md"
  ],
  "discovery_reasoning": "Explanation text"
}}

IMPORTANT: 
- Ensure all file paths use forward slashes (/) not backslashes (\\)
- All paths must start with "documentation_output/"
- Make sure all JSON strings are properly escaped
- Only include .md documentation files, not .py source files""")
                            
                            messages.append(HumanMessage(content=response_content))
                            messages.append(correction_message)
                            continue
                    
                    # If we get here, JSON is valid
                    with open(debug_log_path, "a") as f:
                        f.write(f"MCPManager: JSON validation successful on attempt {retry_count + 1}\n")
                    response_content = cleaned_response
                    break
                    
                except Exception as llm_error:
                    retry_count += 1
                    with open(debug_log_path, "a") as f:
                        f.write(f"MCPManager: LLM call failed on attempt {retry_count}: {str(llm_error)}\n")
                    
                    if retry_count >= max_retries:
                        with open(debug_log_path, "a") as f:
                            f.write(f"MCPManager: All LLM retry attempts failed\n")
                        raise llm_error
                    
                    # Wait before retry for non-JSON errors
                    import time
                    time.sleep(1)

            with open(debug_log_path, "a") as f:
                f.write(f"MCPManager: LLM discovery response received\n")
                f.write(f"MCPManager: Response length: {len(response_content)}\n")

            self.logger.info(
                f"Documentation file discovery complete: {len(response_content)} characters"
            )

            # Parse JSON response
            try:
                with open(debug_log_path, "a") as f:
                    f.write(f"MCPManager: Raw LLM response for discovery: {response_content}\n")
                
                # Clean up backslashes in file paths that cause JSON parsing issues
                cleaned_response = response_content.replace("\\", "/")
                    
                result_data = json.loads(cleaned_response)
                discovered_files = result_data.get("relevant_documentation_files", [])

                with open(debug_log_path, "a") as f:
                    f.write(f"MCPManager: Parsed discovery result: {result_data}\n")
                    f.write(f"MCPManager: Discovered files: {discovered_files}\n")

                return {
                    "discovered_documentation_files": discovered_files,
                    "files_discovery_complete": True,
                    "_discovery_reasoning": result_data.get("discovery_reasoning", ""),
                }
            except json.JSONDecodeError as e:
                self.logger.error(f"Failed to parse file discovery JSON response: {e}")
                self.logger.error(f"Raw response: {response_content}")
                with open(debug_log_path, "a") as f:
                    f.write(f"MCPManager: JSON PARSE ERROR: {str(e)}\n")
                    f.write(f"MCPManager: Raw response causing error: {response_content}\n")
                return {
                    "error_occurred": True,
                    "error_message": f"Failed to parse file discovery response as JSON: {str(e)}",
                }

        except Exception as e:
            self.logger.error(f"Error in file discovery: {e}")
            return {
                "error_occurred": True,
                "error_message": f"Error in file discovery: {str(e)}",
            }

    def load_documentation_file_node(self, state: MCPState) -> Dict[str, Any]:
        """Load the next documentation file."""
        try:
            if state.current_file_index >= len(state.discovered_documentation_files):
                return {"all_files_loaded": True}

            file_path = state.discovered_documentation_files[state.current_file_index]
            full_file_path = state.repo_path / file_path

            self.logger.info(f"Loading documentation file: {file_path}")

            try:
                if full_file_path.exists():
                    with open(full_file_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    doc_file = MCPDocumentationFile(
                        file_path=file_path, content=content, loaded_successfully=True
                    )

                    self.logger.info(
                        f"Successfully loaded {file_path}: {len(content)} characters"
                    )
                else:
                    doc_file = MCPDocumentationFile(
                        file_path=file_path,
                        content="",
                        loaded_successfully=False,
                        error_message=f"File not found: {full_file_path}",
                    )

                    self.logger.warning(
                        f"Documentation file not found: {full_file_path}"
                    )

                # Update state
                updated_files = state.loaded_documentation_files.copy()
                updated_files.append(doc_file)

                return {
                    "loaded_documentation_files": updated_files,
                    "current_file_index": state.current_file_index + 1,
                }

            except Exception as file_error:
                doc_file = MCPDocumentationFile(
                    file_path=file_path,
                    content="",
                    loaded_successfully=False,
                    error_message=f"Error reading file: {str(file_error)}",
                )

                updated_files = state.loaded_documentation_files.copy()
                updated_files.append(doc_file)

                return {
                    "loaded_documentation_files": updated_files,
                    "current_file_index": state.current_file_index + 1,
                }

        except Exception as e:
            self.logger.error(f"Error in load_documentation_file_node: {e}")
            return {
                "error_occurred": True,
                "error_message": f"Error loading documentation file: {str(e)}",
            }

    def should_load_more_files(self, state: MCPState) -> str:
        """Decide whether to load more files or proceed to synthesis."""
        if state.error_occurred:
            return "synthesize"  # Skip to synthesis even with errors

        if state.current_file_index >= len(state.discovered_documentation_files):
            return "synthesize"

        return "load_more"

    def synthesize_feature_understanding_node(self, state: MCPState) -> Dict[str, Any]:
        """Synthesize information from loaded documentation files."""
        try:
            if not state.loaded_documentation_files:
                return {
                    "error_occurred": True,
                    "error_message": "No documentation files were loaded successfully",
                }

            # Prepare content from all successfully loaded files
            documentation_content = ""
            successful_files = []

            for doc_file in state.loaded_documentation_files:
                if doc_file.loaded_successfully:
                    documentation_content += (
                        f"\n\n=== Content from {doc_file.file_path} ===\n"
                    )
                    documentation_content += doc_file.content
                    successful_files.append(doc_file.file_path)
                else:
                    self.logger.warning(
                        f"Skipping failed file: {doc_file.file_path} - {doc_file.error_message}"
                    )

            if not documentation_content.strip():
                return {
                    "error_occurred": True,
                    "error_message": "No documentation content was successfully loaded",
                }

            # Prepare the synthesis prompt
            system_message = SystemMessage(content=MCP_FEATURE_SYNTHESIS_SYSTEM_PROMPT)

            user_content = f"""USER'S FEATURE QUESTION: {state.user_query}

DOCUMENTATION CONTENT FROM MULTIPLE FILES:
{documentation_content}

Please synthesize this information to provide a comprehensive understanding of the feature. Return your response in the specified JSON format."""

            human_message = HumanMessage(content=user_content)

            # Get LLM response with intelligent retry logic
            debug_log_path = Path("/tmp/mcp_debug.log")
            max_retries = 3
            retry_count = 0
            messages = [system_message, human_message]
            
            while retry_count < max_retries:
                try:
                    with open(debug_log_path, "a") as f:
                        f.write(f"MCPManager: Synthesis LLM call attempt {retry_count + 1}/{max_retries}\n")
                    
                    response = self.llm.invoke(messages)
                    response_content = response.content
                    
                    with open(debug_log_path, "a") as f:
                        f.write(f"MCPManager: Synthesis response received, validating format...\n")
                    
                    # Validate JSON format
                    try:
                        result_data = json.loads(response_content)
                        
                        # Validate required fields for synthesis response
                        required_fields = ["feature_description", "comprehensive_answer", "key_components", 
                                         "implementation_details", "usage_examples", "related_concepts"]
                        missing_fields = [field for field in required_fields if field not in result_data]
                        
                        if missing_fields:
                            retry_count += 1
                            with open(debug_log_path, "a") as f:
                                f.write(f"MCPManager: Missing required fields: {missing_fields}\n")
                            
                            if retry_count >= max_retries:
                                raise ValueError(f"Missing required fields: {missing_fields}")
                            
                            # Ask LLM to fix missing fields
                            correction_message = HumanMessage(content=f"""Your previous response was missing required fields: {', '.join(missing_fields)}

Your response was:
{response_content}

Please provide a complete JSON response with ALL required fields:
{{
  "feature_description": "The user's original feature request",
  "comprehensive_answer": "Detailed explanation of the feature",
  "key_components": ["Component 1", "Component 2"],
  "implementation_details": "How the feature is implemented",
  "usage_examples": "Examples of how to use the feature",
  "related_concepts": ["Concept 1", "Concept 2"],
  "source_documentation_files": ["file1.md", "file2.md"]
}}

Make sure your response includes ALL the required fields with meaningful content.""")
                            
                            messages.append(HumanMessage(content=response_content))
                            messages.append(correction_message)
                            continue
                        
                        # Add source files to response
                        result_data["source_documentation_files"] = successful_files
                        
                        with open(debug_log_path, "a") as f:
                            f.write(f"MCPManager: Synthesis JSON validation successful on attempt {retry_count + 1}\n")
                        break
                        
                    except json.JSONDecodeError as json_error:
                        retry_count += 1
                        with open(debug_log_path, "a") as f:
                            f.write(f"MCPManager: Synthesis JSON validation failed: {str(json_error)}\n")
                        
                        if retry_count >= max_retries:
                            raise json_error
                        
                        # Ask LLM to fix JSON format
                        correction_message = HumanMessage(content=f"""Your previous response had a JSON formatting error: {str(json_error)}

Your response was:
{response_content}

Please fix the JSON formatting and provide a valid JSON response that matches the synthesis schema. Make sure all JSON strings are properly escaped and the format is valid.""")
                        
                        messages.append(HumanMessage(content=response_content))
                        messages.append(correction_message)
                        continue
                        
                except Exception as llm_error:
                    retry_count += 1
                    with open(debug_log_path, "a") as f:
                        f.write(f"MCPManager: Synthesis LLM call failed: {str(llm_error)}\n")
                    
                    if retry_count >= max_retries:
                        raise llm_error
                    
                    import time
                    time.sleep(1)

            self.logger.info(
                f"Feature synthesis complete: {len(response_content)} characters"
            )

            return {
                "llm_analysis_complete": True,
                "raw_synthesis_response": result_data,
            }

        except Exception as e:
            self.logger.error(f"Error in feature synthesis: {e}")
            return {
                "error_occurred": True,
                "error_message": f"Error in feature synthesis: {str(e)}",
            }

    def format_feature_results_node(self, state: MCPState) -> Dict[str, Any]:
        """Format the feature analysis results."""
        try:
            if state.error_occurred:
                return {}  # Error already set

            # Access raw_synthesis_response from the state
            if hasattr(state, "raw_synthesis_response"):
                raw_response = state.raw_synthesis_response
            else:
                raw_response = {}

            # Debug logging
            debug_log_path = Path("/tmp/mcp_debug.log")
            with open(debug_log_path, "a") as f:
                f.write(
                    f"format_feature_results_node: " f"raw_response = {raw_response}\n"
                )
                has_attr = hasattr(state, "raw_synthesis_response")
                f.write(
                    f"format_feature_results_node: "
                    f"state has raw_synthesis_response = {has_attr}\n"
                )

            response = MCPFeatureResponse(
                feature_description=raw_response.get(
                    "feature_description", state.user_query
                ),
                comprehensive_answer=raw_response.get("comprehensive_answer", ""),
                key_components=raw_response.get("key_components", []),
                implementation_details=raw_response.get("implementation_details", ""),
                usage_examples=raw_response.get("usage_examples", ""),
                related_concepts=raw_response.get("related_concepts", []),
                source_documentation_files=raw_response.get(
                    "source_documentation_files", []
                ),
            )

            with open(debug_log_path, "a") as f:
                f.write(
                    f"format_feature_results_node: "
                    f"created response = {response.dict()}\n"
                )

            return {"feature_understanding_result": response}

        except Exception as e:
            self.logger.error(f"Error formatting feature results: {e}")
            return {
                "error_occurred": True,
                "error_message": f"Error formatting feature results: {str(e)}",
            }

    async def find_relevant_files(
        self, description: str, repo_path: Path, max_results: int = 10
    ) -> MCPRelevantFilesResponse:
        """Find relevant files based on description."""
        start_time = time.time()

        # Create initial state
        initial_state = MCPState(
            request_type="relevant_files",
            user_query=description,
            repo_path=repo_path,
            max_results=max_results,
        )

        # Create and run workflow
        debug_log_path = Path("/tmp/mcp_debug.log")
        try:
            with open(debug_log_path, "a") as f:
                f.write(f"MCPManager: Creating workflow...\n")
            workflow = self.create_relevant_files_workflow()
            with open(debug_log_path, "a") as f:
                f.write(f"MCPManager: Workflow created successfully\n")
        except Exception as e:
            with open(debug_log_path, "a") as f:
                f.write(f"MCPManager: ERROR creating workflow: {str(e)}\n")
            return MCPRelevantFilesResponse(
                query_description=description, relevant_files=[], total_files_analyzed=0
            )

        try:
            # Debug logging
            debug_log_path = Path("/tmp/mcp_debug.log")
            with open(debug_log_path, "a") as f:
                f.write(
                    f"MCPManager: Starting workflow with initial_state: {initial_state.dict()}\n"
                )

            final_state = workflow.invoke(
                initial_state,
                config={
                    "recursion_limit": self.config.model.get("recursion_limit", 50)
                },
            )

            with open(debug_log_path, "a") as f:
                f.write(
                    f"MCPManager: Workflow completed with final_state type: {type(final_state)}\n"
                )
                if hasattr(final_state, "dict"):
                    f.write(f"MCPManager: Final state dict: {final_state.dict()}\n")
                else:
                    f.write(f"MCPManager: Final state: {final_state}\n")

            # Handle both dict and MCPState final_state
            if isinstance(final_state, dict):
                error_occurred = final_state.get("error_occurred", False)
                relevant_files_result = final_state.get("relevant_files_result")
            else:
                error_occurred = final_state.error_occurred
                relevant_files_result = final_state.relevant_files_result

            with open(debug_log_path, "a") as f:
                f.write(f"MCPManager: error_occurred = {error_occurred}\n")
                f.write(
                    f"MCPManager: relevant_files_result = {relevant_files_result}\n"
                )
                f.write(
                    f"MCPManager: relevant_files_result type = {type(relevant_files_result)}\n"
                )

            if error_occurred:
                # Return error response
                return MCPRelevantFilesResponse(
                    query_description=description,
                    relevant_files=[],
                    total_files_analyzed=0,
                )

            if relevant_files_result is None:
                with open(debug_log_path, "a") as f:
                    f.write(f"MCPManager: ERROR - relevant_files_result is None\n")
                return MCPRelevantFilesResponse(
                    query_description=description,
                    relevant_files=[],
                    total_files_analyzed=0,
                )

            result = relevant_files_result
            result.processing_time_seconds = time.time() - start_time

            return result

        except Exception as e:
            self.logger.error(f"Workflow execution error: {e}")
            return MCPRelevantFilesResponse(
                query_description=description, relevant_files=[], total_files_analyzed=0
            )

    async def understand_feature(
        self, feature_description: str, repo_path: Path
    ) -> MCPFeatureResponse:
        """Understand a feature based on documentation."""
        import time

        start_time = time.time()
        # Create initial state
        initial_state = MCPState(
            request_type="understand_feature",
            user_query=feature_description,
            repo_path=repo_path,
        )

        debug_log_path = Path("/tmp/mcp_debug.log")
        try:
            with open(debug_log_path, "a") as f:
                f.write(f"MCPManager: Creating feature understanding workflow...\n")
            workflow = self.create_feature_understanding_workflow()
            with open(debug_log_path, "a") as f:
                f.write(f"MCPManager: Feature workflow created successfully\n")
        except Exception as e:
            with open(debug_log_path, "a") as f:
                f.write(f"MCPManager: ERROR creating feature workflow: {str(e)}\n")
            return MCPFeatureResponse(
                feature_description=feature_description,
                comprehensive_answer=f"Error: {str(e)}",
                key_components=[],
                implementation_details="",
                usage_examples="",
                related_concepts=[],
                source_documentation_files=[],
            )

        try:
            with open(debug_log_path, "a") as f:
                f.write(
                    f"MCPManager: Starting feature workflow with initial_state: {initial_state.dict()}\n"
                )

            final_state = workflow.invoke(
                initial_state,
                config={
                    "recursion_limit": self.config.model.get("recursion_limit", 50)
                },
            )

            with open(debug_log_path, "a") as f:
                f.write(
                    f"MCPManager: Feature workflow completed with final_state type: {type(final_state)}\n"
                )
                if hasattr(final_state, "dict"):
                    f.write(
                        f"MCPManager: Feature final state dict: {final_state.dict()}\n"
                    )
                else:
                    f.write(f"MCPManager: Feature final state: {final_state}\n")

            # Handle both dict and MCPState final_state
            if isinstance(final_state, dict):
                error_occurred = final_state.get("error_occurred", False)
                error_message = final_state.get("error_message", "")
                feature_understanding_result = final_state.get(
                    "feature_understanding_result"
                )
                discovered_files = final_state.get("discovered_documentation_files", [])
                files_discovery_complete = final_state.get("files_discovery_complete", False)
            else:
                error_occurred = getattr(final_state, "error_occurred", False)
                error_message = getattr(final_state, "error_message", "")
                feature_understanding_result = getattr(
                    final_state, "feature_understanding_result", None
                )
                discovered_files = getattr(final_state, "discovered_documentation_files", [])
                files_discovery_complete = getattr(final_state, "files_discovery_complete", False)

            with open(debug_log_path, "a") as f:
                f.write(f"MCPManager: feature_error_occurred = {error_occurred}\n")
                f.write(
                    f"MCPManager: feature_understanding_result = {feature_understanding_result}\n"
                )
                f.write(
                    f"MCPManager: feature_understanding_result type = {type(feature_understanding_result)}\n"
                )
                f.write(f"MCPManager: discovered_files = {discovered_files}\n")
                f.write(f"MCPManager: files_discovery_complete = {files_discovery_complete}\n")

            if error_occurred:
                return MCPFeatureResponse(
                    feature_description=feature_description,
                    comprehensive_answer=f"Error: {error_message}",
                    key_components=[],
                    implementation_details="",
                    usage_examples="",
                    related_concepts=[],
                    source_documentation_files=[],
                )

            if feature_understanding_result is None:
                with open(debug_log_path, "a") as f:
                    f.write(
                        f"MCPManager: ERROR - feature_understanding_result is None\n"
                    )
                return MCPFeatureResponse(
                    feature_description=feature_description,
                    comprehensive_answer="No feature understanding result found",
                    key_components=[],
                    implementation_details="",
                    usage_examples="",
                    related_concepts=[],
                    source_documentation_files=[],
                )

            # Optionally add processing time if needed
            if hasattr(feature_understanding_result, "processing_time_seconds"):
                feature_understanding_result.processing_time_seconds = (
                    time.time() - start_time
                )

            return feature_understanding_result

        except Exception as e:
            self.logger.error(f"Feature understanding workflow error: {e}")
            with open(debug_log_path, "a") as f:
                f.write(f"MCPManager: Feature workflow execution error: {str(e)}\n")
            return MCPFeatureResponse(
                feature_description=feature_description,
                comprehensive_answer=f"Error: {str(e)}",
                key_components=[],
                implementation_details="",
                usage_examples="",
                related_concepts=[],
                source_documentation_files=[],
            )
