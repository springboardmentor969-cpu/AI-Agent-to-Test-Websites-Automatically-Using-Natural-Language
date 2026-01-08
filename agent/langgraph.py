"""
langgraph.py
Defines LangGraph workflow for processing
natural language test instructions.
"""

from typing import Dict, List
from langgraph.graph import StateGraph
from .parser import parse_instruction, generate_commands


class AgentState(dict):
    """
    Shared state passed between LangGraph nodes
    """
    instruction: str
    parsed_data: Dict
    commands: List


def parser_node(state: AgentState) -> AgentState:
    state["parsed_data"] = parse_instruction(state["instruction"])
    return state


def command_generator_node(state: AgentState) -> AgentState:
    state["commands"] = generate_commands(state["parsed_data"])
    return state


workflow = StateGraph(AgentState)

workflow.add_node("parser", parser_node)
workflow.add_node("command_generator", command_generator_node)

workflow.set_entry_point("parser")
workflow.add_edge("parser", "command_generator")

graph = workflow.compile()


def handle_instruction(instruction: str):
    initial_state = {
        "instruction": instruction
    }

    final_state = graph.invoke(initial_state)

    return {
        "parsed_data": final_state.get("parsed_data"),
        "structured_commands": final_state.get("commands")
    }
