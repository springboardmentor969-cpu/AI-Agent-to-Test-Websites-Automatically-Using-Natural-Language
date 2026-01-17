from langgraph.graph import StateGraph
from agent.nl_parser import parse_instruction
from agent.playwright_generator import generate_steps
from agent.assertion_engine import generate_assertions
from executor.runner import run_test

def workflow_runner(instruction):
    intent = parse_instruction(instruction)
    steps = generate_steps(intent)
    assertions = generate_assertions(intent)
    return run_test(steps, assertions)
