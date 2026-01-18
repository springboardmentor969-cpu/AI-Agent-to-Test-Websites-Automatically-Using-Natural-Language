from typing import TypedDict
from langgraph.graph import StateGraph
from instruction_parser import parse_instruction

class TestState(TypedDict):
    instruction: str
    action_plan: dict

def planner_node(state: TestState):
    parsed = parse_instruction(state["instruction"])
    commands = parsed["commands"]

    steps = []

    if "login" in commands:
        steps = [
            "Open browser",
            "Navigate to login page",
            "Enter credentials",
            "Submit form",
            "Validate result"
        ]

    elif "search" in commands:
        steps = [
            "Open browser",
            "Navigate to search page",
            "Enter search term",
            "Submit search",
            "Validate results"
        ]

    else:
        steps = ["Unsupported instruction"]

    return {
        "action_plan": {
            "intent": parsed["raw"],
            "steps": steps
        }
    }

graph = StateGraph(TestState)
graph.add_node("planner", planner_node)
graph.set_entry_point("planner")
graph.set_finish_point("planner")

langgraph_app = graph.compile()
