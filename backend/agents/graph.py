from langgraph.graph import StateGraph
from agents.parser import parse_instruction
from agents.executor import execute_test

def run_test(instruction):
    graph = StateGraph(dict)

    graph.add_node("parser", parse_instruction)
    graph.add_node("executor", execute_test)

    graph.set_entry_point("parser")
    graph.add_edge("parser", "executor")

    return graph.compile().invoke({"instruction": instruction})
