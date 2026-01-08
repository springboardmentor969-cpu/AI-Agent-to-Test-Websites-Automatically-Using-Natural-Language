"""
LangGraph Agent Configuration
Milestone 1: Baseline agent with simple workflow

This module defines the LangGraph agent that processes test instructions
through a 3-node workflow: receive → validate → parse
"""

from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional
from langchain_anthropic import ChatAnthropic
from .parser import parse_instruction
import os


# Define the state structure for our agent workflow
class TestAgentState(TypedDict):
    """
    State that gets passed through the agent workflow.
    Each node can read from and write to this state.
    
    Attributes:
        instruction: Natural language test instruction from user
        url: Target URL to test
        parsed_actions: List of parsed structured actions
        validation_result: Validation results (valid: bool, errors: list)
        error: Any errors encountered during processing
        status: Current status of the workflow
    """
    instruction: str
    url: str
    parsed_actions: list
    validation_result: dict
    error: Optional[str]
    status: str


def receive_instruction_node(state: TestAgentState) -> TestAgentState:
    """
    Node 1: Entry point - receives and logs the test instruction
    
    This node marks the beginning of the workflow and initializes
    the state with default values.
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with initialized values
    """
    print(f"\n[RECEIVE] Processing instruction: {state['instruction'][:50]}...")
    print(f"[RECEIVE] Target URL: {state['url']}")
    
    return {
        **state,
        'status': 'received',
        'parsed_actions': [],
        'error': None,
        'validation_result': {}
    }


def validate_input_node(state: TestAgentState) -> TestAgentState:
    """
    Node 2: Validates that the instruction and URL are properly formatted
    
    Performs basic validation checks:
    - Instruction is not empty
    - Instruction has minimum length (5 characters)
    - URL is properly formatted (starts with http:// or https://)
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with validation results
    """
    instruction = state.get('instruction', '').strip()
    url = state.get('url', '').strip()
    
    # Initialize validation result
    validation_result = {
        'valid': True,
        'errors': []
    }
    
    # Validate instruction
    if not instruction:
        validation_result['valid'] = False
        validation_result['errors'].append('Instruction cannot be empty')
    elif len(instruction) < 5:
        validation_result['valid'] = False
        validation_result['errors'].append('Instruction too short (minimum 5 characters)')
    
    # Validate URL
    if not url:
        validation_result['valid'] = False
        validation_result['errors'].append('URL cannot be empty')
    elif not (url.startswith('http://') or url.startswith('https://')):
        validation_result['valid'] = False
        validation_result['errors'].append('URL must start with http:// or https://')
    
    # Log validation result
    status_msg = " VALID" if validation_result['valid'] else "❌ INVALID"
    print(f"[VALIDATE] {status_msg}")
    
    if not validation_result['valid']:
        print(f"[VALIDATE] Errors: {', '.join(validation_result['errors'])}")
    
    return {
        **state,
        'validation_result': validation_result,
        'status': 'validated' if validation_result['valid'] else 'validation_failed',
        'error': None if validation_result['valid'] else '; '.join(validation_result['errors'])
    }


def parse_instruction_node(state: TestAgentState) -> TestAgentState:
    """
    Node 3: Parses natural language instruction into structured actions
    
    For Milestone 1, this uses basic keyword matching from the parser module.
    In Milestone 2, this will be enhanced with LLM-powered parsing using Claude.
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with parsed actions
    """
    instruction = state['instruction']
    
    print(f"[PARSE] Analyzing instruction...")
    
    # Use the parser module to extract actions
    # Currently uses keyword matching, will be enhanced in Milestone 2
    parsed_actions = parse_instruction(instruction)
    
    # Log parsed actions
    print(f"[PARSE] Found {len(parsed_actions)} action(s)")
    for idx, action in enumerate(parsed_actions, 1):
        print(f"[PARSE]   {idx}. {action['action']} (confidence: {action['confidence']})")
    
    return {
        **state,
        'parsed_actions': parsed_actions,
        'status': 'parsed'
    }


def create_test_agent():
    """
    Creates and compiles the LangGraph agent workflow.
    
    Workflow for Milestone 1:
    1. receive_instruction - Entry point, initializes state
    2. validate_input - Checks instruction and URL validity
    3. parse_instruction - Converts natural language to structured actions
    
    The workflow uses conditional edges to skip parsing if validation fails.
    
    Returns:
        Compiled LangGraph agent ready to process test instructions
    """
    
    # Initialize the LLM (Claude Sonnet 4)
    # Note: This is prepared for Milestone 2 when we'll use it for advanced parsing
    llm = ChatAnthropic(
        model="claude-sonnet-4-20250514",
        api_key=os.environ.get('ANTHROPIC_API_KEY'),
        temperature=0  # Deterministic output for consistent test generation
    )
    
    # Create the state graph
    workflow = StateGraph(TestAgentState)
    
    # Add nodes to the workflow
    print(" Building LangGraph workflow...")
    workflow.add_node("receive_instruction", receive_instruction_node)
    workflow.add_node("validate_input", validate_input_node)
    workflow.add_node("parse_instruction", parse_instruction_node)
    print("    Added 3 nodes: receive , validate , parse")
    
    # Define the workflow edges (the execution path)
    
    # Set entry point
    workflow.set_entry_point("receive_instruction")
    
    # receive_instruction always goes to validate_input
    workflow.add_edge("receive_instruction", "validate_input")
    
    # Conditional edge: proceed to parse only if validation passes
    def should_continue_to_parse(state: TestAgentState) -> str:
        """
        Determine if we should continue to parsing or end the workflow.
        
        Args:
            state: Current agent state
            
        Returns:
            "parse" if validation passed, "end" otherwise
        """
        if state.get("validation_result", {}).get("valid", False):
            return "parse"
        return "end"
    
    workflow.add_conditional_edges(
        "validate_input",
        should_continue_to_parse,
        {
            "parse": "parse_instruction",
            "end": END
        }
    )
    
    # parse_instruction always ends the workflow
    workflow.add_edge("parse_instruction", END)
    
    print("   Configured workflow edges with validation gate")
    
    # Compile the graph into an executable agent
    agent = workflow.compile()
    print("    Agent compiled successfully!")
    
    return agent