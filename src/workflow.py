from langgraph.graph import StateGraph

from agent.instruction_parser import parse_instruction
from agent.code_generator import generate_steps
from agent.assertion_engine import generate_assertions
from executor.runner import run_test
from reporting.report_manager import generate_report


class WorkflowState(dict):
    pass


def parse_node(state: WorkflowState):
    instruction = state.get("instruction", "")
    state["intent"] = parse_instruction(instruction)
    return state


def generate_node(state: WorkflowState):
    intent = state.get("intent")

    # SAFE GUARD (prevents KeyError)
    if not intent:
        state["steps"] = []
        state["assertions"] = []
        return state

    state["steps"] = generate_steps(intent)
    state["assertions"] = generate_assertions()
    return state


def execute_node(state: WorkflowState):
    steps = state.get("steps", [])
    assertions = state.get("assertions", [])
    state["results"] = run_test(steps, assertions)
    return state


def report_node(state: WorkflowState):
    results = state.get("results", [])
    state["report"] = generate_report(results)
    return state


# Build LangGraph
graph = StateGraph(WorkflowState)
graph.add_node("parse", parse_node)
graph.add_node("generate", generate_node)
graph.add_node("execute", execute_node)
graph.add_node("report", report_node)

graph.set_entry_point("parse")
graph.add_edge("parse", "generate")
graph.add_edge("generate", "execute")
graph.add_edge("execute", "report")

workflow_app = graph.compile()


def execute_workflow(instruction: str):
    initial_state = {"instruction": instruction}
    final_state = workflow_app.invoke(initial_state)

    return final_state.get("report", {
        "total": 0,
        "passed": 0,
        "failed": 1,
        "details": [{"action": "Workflow failed", "status": "FAIL"}]
    })
