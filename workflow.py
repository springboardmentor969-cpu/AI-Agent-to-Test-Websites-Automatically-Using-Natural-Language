from typing import TypedDict
from langgraph.graph import StateGraph
from parser import parse_instruction

class AgentState(TypedDict):
    instruction: str
    parsed_command: dict
    structured_command: dict

def parser_node(state: AgentState):
    parsed = parse_instruction(state["instruction"])
    return {"parsed_command": parsed}

def command_builder_node(state: AgentState):
    parsed = state["parsed_command"]

    structured = {
        "action": parsed.get("action"),
        "selector_type": "id",
        "selector_value": parsed.get("target"),
        "value": parsed.get("value")
    }

    return {"structured_command": structured}

graph = StateGraph(AgentState)

graph.add_node("parser", parser_node)
graph.add_node("command_builder", command_builder_node)

graph.set_entry_point("parser")
graph.add_edge("parser", "command_builder")

agent_workflow = graph.compile()
