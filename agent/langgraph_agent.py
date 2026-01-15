from langgraph.graph import StateGraph
from agent.parser import parse_instruction
from agent.playwright_generator import generate_playwright_code


def parser_node(state):
    instruction = state["instruction"]
    parsed_steps = parse_instruction(instruction)
    return {"parsed_steps": parsed_steps}


def playwright_node(state):
    parsed_steps = state["parsed_steps"]
    playwright_code = generate_playwright_code(parsed_steps)

    return {
        "parsed_steps": parsed_steps,
        "playwright_code": playwright_code
    }

def build_agent():
    graph = StateGraph(dict)

    graph.add_node("parser", parser_node)
    graph.add_node("playwright", playwright_node)

    graph.set_entry_point("parser")
    graph.add_edge("parser", "playwright")
    graph.set_finish_point("playwright")

    return graph.compile()
