from langgraph.graph import StateGraph
from agent.parser import parse_instruction

def instruction_node(state):
    instruction = state["instruction"]
    parsed_steps = parse_instruction(instruction)
    return {"steps": parsed_steps}

def build_agent():
    graph = StateGraph(dict)
    graph.add_node("parser", instruction_node)
    graph.set_entry_point("parser")
    graph.set_finish_point("parser")
    return graph.compile()
