from langgraph.graph.state import StateGraph
from langgraph.graph import END

from agent.instruction_parser import parse_instruction
from agent.code_generator import generate_steps
from agent.assertion_engine import generate_assertions
from executor.runner import run_test
from reporting.report_manager import generate_report


def execute_workflow(instruction: str):
    # Initial state
    state = {
        "instruction": instruction,
        "intent": None,
        "steps": None,
        "assertions": None,
        "results": None,
        "report": None
    }

    graph = StateGraph(dict)

    # ---------- Nodes ----------
    def parse_node(state):
        state["intent"] = parse_instruction(state["instruction"])
        return state

    def generate_node(state):
        state["steps"] = generate_steps(state["intent"])
        state["assertions"] = generate_assertions()
        return state

    def execute_node(state):
        state["results"] = run_test(
            state["steps"],
            state["assertions"]
        )
        return state

    def report_node(state):
        state["report"] = generate_report(state["results"])
        return state

    # ---------- Graph ----------
    graph.add_node("parse", parse_node)
    graph.add_node("generate", generate_node)
    graph.add_node("execute", execute_node)
    graph.add_node("report", report_node)

    graph.set_entry_point("parse")
    graph.add_edge("parse", "generate")
    graph.add_edge("generate", "execute")
    graph.add_edge("execute", "report")
    graph.add_edge("report", END)

    app = graph.compile()

    final_state = app.invoke(state)
    return final_state["report"]
