from typing import TypedDict
from langgraph.graph import StateGraph
from instruction_parser import parse_instruction
from playwright_generator import generate_actions
from playwright_executor import run_actions

class TestState(TypedDict):
    instruction: str
    action_plan: dict
    generated_code: list
    report: list

def planner_node(state: TestState):
    print("PLANNER:", state["instruction"])
    parsed = parse_instruction(state["instruction"])
    commands = parsed["commands"]
    # Human readable steps (for UI)
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
    # NEW ---- Code generation
    actions = generate_actions(commands)
    # NEW ---- Execute and validate
    report = run_actions(actions, commands)
    target = state["instruction"]
    return {
        "action_plan": {
            "intent": parsed["raw"],
            "steps": steps
        },
        "generated_code": actions,
        "report": report
    }
# ---- Build LangGraph ----
graph = StateGraph(TestState)
graph.add_node("planner", planner_node)
graph.set_entry_point("planner")
graph.set_finish_point("planner")
# ---- Compile LangGraph ----
langgraph_app = graph.compile()
