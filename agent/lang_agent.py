from langgraph.graph import StateGraph
from typing import TypedDict

from .parser import parse_instruction
from .playwright_generator import generate_playwright_steps
from .assertion_generator import generate_assertions
from .executor import execute_test


class AgentState(TypedDict):
    user_input: str
    parsed_steps: list
    result: str
    execution_log: list


def agent_node(state: AgentState):
    steps = parse_instruction(state["user_input"])
    playwright_steps = generate_playwright_steps(steps)
    assertions = generate_assertions()

    result, execution_log = execute_test(playwright_steps, assertions)

    return {
        "parsed_steps": steps,
        "result": result,
        "execution_log": execution_log
    }


graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.set_entry_point("agent")
graph.set_finish_point("agent")

agent = graph.compile()


def run_agent(user_input):
    return agent.invoke({"user_input": user_input})
