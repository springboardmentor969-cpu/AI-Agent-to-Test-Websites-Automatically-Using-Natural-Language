from langgraph.graph import StateGraph

from llm_parser import parse_instruction_llm
from parser import parse_instruction
from codegenerator import generate_playwright_code
from executor import execute_test
from reporter import generate_report




def parser_node(state: dict):
    """
    1. Try Grok AI parser
    2. If empty / fails → fallback rule-based parser
    """
    parsed = parse_instruction_llm(state["instruction"])

    if not parsed:
        parsed = parse_instruction(state["instruction"])

    state["parsed_command"] = parsed
    return state


def codegen_node(state: dict):
    """
    Convert parsed commands into Playwright code
    """
    action_block, full_script = generate_playwright_code(
        state["parsed_command"],
        state["target_url"]
    )

    state["playwright_code"] = action_block
    state["full_playwright_script"] = full_script
    return state


def executor_node(state: dict):
    """
    Execute Playwright actions and capture screenshot
    """
    execution_result = execute_test(state["playwright_code"])
    state["execution_result"] = execution_result
    return state


def reporter_node(state: dict):
    """
    Generate final report
    """
    report = generate_report(state)
    state["report"] = report
    return state




graph = StateGraph(dict)

graph.add_node("parser", parser_node)
graph.add_node("codegen", codegen_node)
graph.add_node("executor", executor_node)
graph.add_node("reporter", reporter_node)

graph.set_entry_point("parser")

graph.add_edge("parser", "codegen")
graph.add_edge("codegen", "executor")
graph.add_edge("executor", "reporter")

graph.set_finish_point("reporter")

agent_workflow = graph.compile()
