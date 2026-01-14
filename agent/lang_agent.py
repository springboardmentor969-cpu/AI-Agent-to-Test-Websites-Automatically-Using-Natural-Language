from langgraph.graph import StateGraph
from typing import TypedDict
from datetime import datetime
import json
import os

from .parser import parse_instruction
from .playwright_generator import generate_playwright_steps
from .assertion_generator import generate_assertions
from .executor import execute_test


class AgentState(TypedDict):
    user_input: str
    parsed_steps: list
    result: str
    execution_log: list
    screenshot: str


def agent_node(state: AgentState):
    steps = parse_instruction(state["user_input"])
    playwright_steps = generate_playwright_steps(steps)
    assertions = generate_assertions()

    result, execution_log, screenshot = execute_test(playwright_steps, assertions)

    os.makedirs("reports", exist_ok=True)
    report_path = "reports/reports.json"

    report_entry = {
        "timestamp": str(datetime.now()),
        "user_input": state["user_input"],
        "parsed_steps": steps,
        "result": result,
        "execution_log": execution_log,
        "screenshot": screenshot
    }

    if os.path.exists(report_path):
        with open(report_path, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(report_entry)

    with open(report_path, "w") as f:
        json.dump(data, f, indent=2)

    return report_entry


graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.set_entry_point("agent")
graph.set_finish_point("agent")

agent = graph.compile()

def run_agent(user_input):
    return agent.invoke({"user_input": user_input})
