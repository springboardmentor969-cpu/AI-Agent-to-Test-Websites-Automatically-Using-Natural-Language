# agent/graph.py

from langgraph.graph import StateGraph, END
from pydantic import BaseModel
from typing import Any

from .parser import InstructionParser
from .executor import Executor
from .reporter import Reporter


class SingleState(BaseModel):
    instruction: str = ""
    actions: Any = None
    exec_result: Any = None
    report: Any = None


def build_graph():

    workflow = StateGraph(state_schema=SingleState)

    parser = InstructionParser()
    executor = Executor()
    reporter = Reporter()

    workflow.add_node(
        "parse",
        lambda state: {"actions": parser.parse(state.instruction)}
    )

    # Use synchronous execution to avoid Windows asyncio subprocess issues
    workflow.add_node(
        "execute",
        lambda state: {"exec_result": executor.execute_actions(state.actions)}
    )

    workflow.add_node(
        "report",
        lambda state: {"report": reporter.generate_report(state.exec_result, test_id="single_test")}
    )

    workflow.set_entry_point("parse")
    workflow.add_edge("parse", "execute")
    workflow.add_edge("execute", "report")
    workflow.add_edge("report", END)

    return workflow
