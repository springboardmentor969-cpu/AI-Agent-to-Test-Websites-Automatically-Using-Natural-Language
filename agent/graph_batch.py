from langgraph.graph import StateGraph, END
from pydantic import BaseModel
from typing import List, Any

from .parser import InstructionParser
from .parallel_executor import ParallelExecutor
from .reporter import Reporter

class BatchState(BaseModel):
    instructions: List[str] = []
    settings: Any = None
    parsed_sets: List[Any] = []
    exec_results: List[Any] = []
    reports: List[Any] = []

def build_batch_graph():
    workflow = StateGraph(state_schema=BatchState)

    parser = InstructionParser()
    executor = ParallelExecutor()
    reporter = Reporter()

    workflow.add_node(
        "parse_batch",
        lambda state: {
            "parsed_sets": [parser.parse(test) for test in state.instructions]
        }
    )

    workflow.add_node(
        "execute_all",
        lambda state: {
            "exec_results": executor.run_parallel(state.parsed_sets, settings=state.settings)
        }
    )

    def generate_reports_node(state: BatchState):
        reports = []
        for i, result in enumerate(state.exec_results):
            simple_id = f"ID-{i+1:03}"
            html, js, pdf = reporter.generate_report(result, test_id=simple_id)
            reports.append({
                "html_report": html,
                "json_report": js,
                "pdf_report": pdf
            })
        return {"reports": reports}

    workflow.add_node("generate_reports", generate_reports_node)

    workflow.set_entry_point("parse_batch")
    workflow.add_edge("parse_batch", "execute_all")
    workflow.add_edge("execute_all", "generate_reports")
    workflow.add_edge("generate_reports", END)

    return workflow
