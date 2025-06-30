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
    MCPDocumentationFile
)
from .prompts.mcp_file_relevance_prompt import (
    MCP_FILE_RELEVANCE_SYSTEM_PROMPT,
    MCP_FEATURE_DISCOVERY_SYSTEM_PROMPT,
    MCP_FEATURE_SYNTHESIS_SYSTEM_PROMPT
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
        workflow.add_node("discover_documentation_files", self.discover_documentation_files_node)
        workflow.add_node("load_documentation_file", self.load_documentation_file_node)
        workflow.add_node("synthesize_feature_understanding", self.synthesize_feature_understanding_node)
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
                "synthesize": "synthesize_feature_understanding"
            }
        )
        
        workflow.add_edge("synthesize_feature_understanding", "format_feature_results")
        workflow.add_edge("format_feature_results", END)
        
        return workflow.compile()

    def load_documentation_node(self, state: MCPState) -> Dict[str, Any]:
        """Load the documentation guide content."""
        try:
            documentation_guide_path = state.repo_path / "documentation_output" / "documentation_guide.md"
            
            if documentation_guide_path.exists():
                with open(documentation_guide_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                self.logger.info(f"Loaded documentation guide: {len(content)} characters")
                return {
                    "documentation_guide_content": content,
                    "documentation_loaded": True
                }
            else:
                self.logger.warning(f"Documentation guide not found at {documentation_guide_path}")
                return {
                    "documentation_guide_content": "",
                    "documentation_loaded": False,
                    "error_occurred": True,
                    "error_message": f"Documentation guide not found at {documentation_guide_path}"
                }
                
        except Exception as e:
            self.logger.error(f"Error loading documentation: {e}")
            return {
                "documentation_loaded": False,
                "error_occurred": True,
                "error_message": f"Error loading documentation: {str(e)}"
            }

    def analyze_file_relevance_node(self, state: MCPState) -> Dict[str, Any]:
        """Use LLM to analyze file relevance."""
        try:
            if not state.documentation_loaded:
                return {
                    "error_occurred": True,
                    "error_message": "Documentation not loaded, cannot analyze relevance"
                }
            
            # Prepare the prompt
            system_message = SystemMessage(content=MCP_FILE_RELEVANCE_SYSTEM_PROMPT)
            
            user_content = f"""DOCUMENTATION GUIDE:
{state.documentation_guide_content}

USER QUERY: {state.user_query}

Please analyze the documentation and identify the most relevant SOURCE CODE files (not documentation files) for this query. Return your response in the specified JSON format."""
            
            human_message = HumanMessage(content=user_content)
            
            # Get LLM response
            response = self.llm.invoke([system_message, human_message])
            response_content = response.content
            
            self.logger.info(f"LLM analysis complete: {len(response_content)} characters")
            
            # Parse JSON response
            try:
                result_data = json.loads(response_content)
                return {
                    "llm_analysis_complete": True,
                    "_raw_llm_response": result_data
                }
            except json.JSONDecodeError as e:
                self.logger.error(f"Failed to parse LLM JSON response: {e}")
                self.logger.error(f"Raw response: {response_content}")
                return {
                    "error_occurred": True,
                    "error_message": f"Failed to parse LLM response as JSON: {str(e)}"
                }
                
        except Exception as e:
            self.logger.error(f"Error in LLM analysis: {e}")
            return {
                "error_occurred": True,
                "error_message": f"Error in LLM analysis: {str(e)}"
            }

    def format_relevant_files_results_node(self, state: MCPState) -> Dict[str, Any]:
        """Format the results into the final response model."""
        try:
            if state.error_occurred:
                return {}  # Error already set, no need to modify state
            
            raw_response = getattr(state, '_raw_llm_response', {})
            
            # Convert to our response model
            file_results = []
            for file_data in raw_response.get('relevant_files', []):
                file_result = MCPFileResult(
                    file_path=file_data.get('file_path', ''),
                    summary=file_data.get('summary', ''),
                    relevance_score=file_data.get('relevance_score', 0.0),
                    reasoning=file_data.get('reasoning', '')
                )
                file_results.append(file_result)
            
            # Limit results to max_results
            if len(file_results) > state.max_results:
                file_results = file_results[:state.max_results]
            
            response = MCPRelevantFilesResponse(
                query_description=state.user_query,
                relevant_files=file_results,
                total_files_analyzed=raw_response.get('total_files_analyzed', len(file_results))
            )
            
            return {
                "relevant_files_result": response
            }
            
        except Exception as e:
            self.logger.error(f"Error formatting results: {e}")
            return {
                "error_occurred": True,
                "error_message": f"Error formatting results: {str(e)}"
            }

    def discover_documentation_files_node(self, state: MCPState) -> Dict[str, Any]:
        """Use LLM to discover relevant documentation files."""
        try:
            if not state.documentation_loaded:
                return {
                    "error_occurred": True,
                    "error_message": "Documentation not loaded, cannot discover files"
                }
            
            # Prepare the prompt for file discovery
            system_message = SystemMessage(content=MCP_FEATURE_DISCOVERY_SYSTEM_PROMPT)
            
            user_content = f"""DOCUMENTATION GUIDE:
{state.documentation_guide_content}

FEATURE TO UNDERSTAND: {state.user_query}

Please analyze the documentation guide and identify which documentation files contain information about this feature. Return your response in the specified JSON format."""
            
            human_message = HumanMessage(content=user_content)
            
            # Get LLM response
            response = self.llm.invoke([system_message, human_message])
            response_content = response.content
            
            self.logger.info(f"Documentation file discovery complete: {len(response_content)} characters")
            
            # Parse JSON response
            try:
                result_data = json.loads(response_content)
                discovered_files = result_data.get('relevant_documentation_files', [])
                
                return {
                    "discovered_documentation_files": discovered_files,
                    "files_discovery_complete": True,
                    "_discovery_reasoning": result_data.get('discovery_reasoning', '')
                }
            except json.JSONDecodeError as e:
                self.logger.error(f"Failed to parse file discovery JSON response: {e}")
                self.logger.error(f"Raw response: {response_content}")
                return {
                    "error_occurred": True,
                    "error_message": f"Failed to parse file discovery response as JSON: {str(e)}"
                }
                
        except Exception as e:
            self.logger.error(f"Error in file discovery: {e}")
            return {
                "error_occurred": True,
                "error_message": f"Error in file discovery: {str(e)}"
            }

    def load_documentation_file_node(self, state: MCPState) -> Dict[str, Any]:
        """Load the next documentation file."""
        try:
            if state.current_file_index >= len(state.discovered_documentation_files):
                return {
                    "all_files_loaded": True
                }
            
            file_path = state.discovered_documentation_files[state.current_file_index]
            full_file_path = state.repo_path / file_path
            
            self.logger.info(f"Loading documentation file: {file_path}")
            
            try:
                if full_file_path.exists():
                    with open(full_file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    doc_file = MCPDocumentationFile(
                        file_path=file_path,
                        content=content,
                        loaded_successfully=True
                    )
                    
                    self.logger.info(f"Successfully loaded {file_path}: {len(content)} characters")
                else:
                    doc_file = MCPDocumentationFile(
                        file_path=file_path,
                        content="",
                        loaded_successfully=False,
                        error_message=f"File not found: {full_file_path}"
                    )
                    
                    self.logger.warning(f"Documentation file not found: {full_file_path}")
                
                # Update state
                updated_files = state.loaded_documentation_files.copy()
                updated_files.append(doc_file)
                
                return {
                    "loaded_documentation_files": updated_files,
                    "current_file_index": state.current_file_index + 1
                }
                
            except Exception as file_error:
                doc_file = MCPDocumentationFile(
                    file_path=file_path,
                    content="",
                    loaded_successfully=False,
                    error_message=f"Error reading file: {str(file_error)}"
                )
                
                updated_files = state.loaded_documentation_files.copy()
                updated_files.append(doc_file)
                
                return {
                    "loaded_documentation_files": updated_files,
                    "current_file_index": state.current_file_index + 1
                }
                
        except Exception as e:
            self.logger.error(f"Error in load_documentation_file_node: {e}")
            return {
                "error_occurred": True,
                "error_message": f"Error loading documentation file: {str(e)}"
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
                    "error_message": "No documentation files were loaded successfully"
                }
            
            # Prepare content from all successfully loaded files
            documentation_content = ""
            successful_files = []
            
            for doc_file in state.loaded_documentation_files:
                if doc_file.loaded_successfully:
                    documentation_content += f"\n\n=== Content from {doc_file.file_path} ===\n"
                    documentation_content += doc_file.content
                    successful_files.append(doc_file.file_path)
                else:
                    self.logger.warning(f"Skipping failed file: {doc_file.file_path} - {doc_file.error_message}")
            
            if not documentation_content.strip():
                return {
                    "error_occurred": True,
                    "error_message": "No documentation content was successfully loaded"
                }
            
            # Prepare the synthesis prompt
            system_message = SystemMessage(content=MCP_FEATURE_SYNTHESIS_SYSTEM_PROMPT)
            
            user_content = f"""USER'S FEATURE QUESTION: {state.user_query}

DOCUMENTATION CONTENT FROM MULTIPLE FILES:
{documentation_content}

Please synthesize this information to provide a comprehensive understanding of the feature. Return your response in the specified JSON format."""
            
            human_message = HumanMessage(content=user_content)
            
            # Get LLM response
            response = self.llm.invoke([system_message, human_message])
            response_content = response.content
            
            self.logger.info(f"Feature synthesis complete: {len(response_content)} characters")
            
            # Parse JSON response
            try:
                result_data = json.loads(response_content)
                result_data["source_documentation_files"] = successful_files  # Ensure we include the source files
                
                return {
                    "llm_analysis_complete": True,
                    "_raw_synthesis_response": result_data
                }
            except json.JSONDecodeError as e:
                self.logger.error(f"Failed to parse synthesis JSON response: {e}")
                self.logger.error(f"Raw response: {response_content}")
                return {
                    "error_occurred": True,
                    "error_message": f"Failed to parse synthesis response as JSON: {str(e)}"
                }
                
        except Exception as e:
            self.logger.error(f"Error in feature synthesis: {e}")
            return {
                "error_occurred": True,
                "error_message": f"Error in feature synthesis: {str(e)}"
            }


    def format_feature_results_node(self, state: MCPState) -> Dict[str, Any]:
        """Format the feature analysis results."""
        try:
            if state.error_occurred:
                return {}  # Error already set
            
            raw_response = getattr(state, '_raw_synthesis_response', {})
            
            response = MCPFeatureResponse(
                feature_description=raw_response.get('feature_description', state.user_query),
                comprehensive_answer=raw_response.get('comprehensive_answer', ''),
                key_components=raw_response.get('key_components', []),
                implementation_details=raw_response.get('implementation_details', ''),
                usage_examples=raw_response.get('usage_examples', ''),
                related_concepts=raw_response.get('related_concepts', []),
                source_documentation_files=raw_response.get('source_documentation_files', [])
            )
            
            return {
                "feature_understanding_result": response
            }
            
        except Exception as e:
            self.logger.error(f"Error formatting feature results: {e}")
            return {
                "error_occurred": True,
                "error_message": f"Error formatting feature results: {str(e)}"
            }

    async def find_relevant_files(self, description: str, repo_path: Path, max_results: int = 10) -> MCPRelevantFilesResponse:
        """Find relevant files based on description."""
        start_time = time.time()
        
        # Create initial state
        initial_state = MCPState(
            request_type="relevant_files",
            user_query=description,
            repo_path=repo_path,
            max_results=max_results
        )
        
        # Create and run workflow
        workflow = self.create_relevant_files_workflow()
        
        try:
            final_state = workflow.invoke(initial_state)
            
            if final_state.error_occurred:
                # Return error response
                return MCPRelevantFilesResponse(
                    query_description=description,
                    relevant_files=[],
                    total_files_analyzed=0
                )
            
            result = final_state.relevant_files_result
            result.processing_time_seconds = time.time() - start_time
            
            return result
            
        except Exception as e:
            self.logger.error(f"Workflow execution error: {e}")
            return MCPRelevantFilesResponse(
                query_description=description,
                relevant_files=[],
                total_files_analyzed=0
            )

    async def understand_feature(self, feature_description: str, repo_path: Path) -> MCPFeatureResponse:
        """Understand a feature based on documentation."""
        # Create initial state
        initial_state = MCPState(
            request_type="understand_feature",
            user_query=feature_description,
            repo_path=repo_path
        )
        
        # Create and run workflow
        workflow = self.create_feature_understanding_workflow()
        
        try:
            final_state = workflow.invoke(initial_state)
            
            # Convert dict response to MCPState if needed
            if isinstance(final_state, dict):
                # Extract values from the dict response
                error_occurred = final_state.get('error_occurred', False)
                error_message = final_state.get('error_message', '')
                feature_understanding_result = final_state.get('feature_understanding_result')
            else:
                error_occurred = final_state.error_occurred
                error_message = final_state.error_message
                feature_understanding_result = final_state.feature_understanding_result
            
            if error_occurred:
                # Return error response
                return MCPFeatureResponse(
                    feature_description=feature_description,
                    comprehensive_answer=f"Error: {error_message}",
                    key_components=[],
                    implementation_details="",
                    usage_examples="",
                    related_concepts=[],
                    source_documentation_files=[]
                )

            return feature_understanding_result or MCPFeatureResponse(
                feature_description=feature_description,
                comprehensive_answer="No feature understanding result found",
                key_components=[],
                implementation_details="",
                usage_examples="",
                related_concepts=[],
                source_documentation_files=[]
            )
            
        except Exception as e:
            self.logger.error(f"Feature understanding workflow error: {e}")
            return MCPFeatureResponse(
                feature_description=feature_description,
                comprehensive_answer=f"Error: {str(e)}",
                key_components=[],
                implementation_details="",
                usage_examples="",
                related_concepts=[],
                source_documentation_files=[]
            )