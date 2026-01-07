from langgraph.graph import StateGraph
from typing import TypedDict
from .parser import parse_instruction

class AgentState(TypedDict):
    user_input: str
    parsed_steps: list

def parser_node(state: AgentState):
    steps = parse_instruction(state["user_input"])
    return {"parsed_steps": steps}

graph = StateGraph(AgentState)
graph.add_node("parser", parser_node)
graph.set_entry_point("parser")
graph.set_finish_point("parser")

agent = graph.compile()

def run_agent(user_input):
    result = agent.invoke({"user_input": user_input})
    return result