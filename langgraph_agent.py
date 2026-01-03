from typing import TypedDict
from langgraph.graph import StateGraph

# 1. Define state
class TestState(TypedDict):
    instruction: str
    action_plan: dict

# 2. Define node
def planner_node(state: TestState):
    instruction = state["instruction"]

    # Placeholder action plan (mentor-friendly)
    action_plan = {
        "intent": instruction,
        "steps": [
            "Open browser",
            "Navigate to login page",
            "Enter credentials",
            "Submit form",
            "Validate result"
        ]
    }

    return {"action_plan": action_plan}

# 3. Build graph
graph = StateGraph(TestState)
graph.add_node("planner", planner_node)
graph.set_entry_point("planner")
graph.set_finish_point("planner")

# 4. Compile graph
langgraph_app = graph.compile()
