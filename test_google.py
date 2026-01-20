#!/usr/bin/env python3

from src.instruction_parser.instruction_parser import InstructionParser
from src.assertion_generator.assertion_generator import AssertionGenerator
from src.playwright_executor.playwright_executor import execute_actions

def test_google_search():
    # Parse the instruction
    parser = InstructionParser()
    actions = parser.parse("open google, enter 'hello world' in search, click search")

    print("Parsed actions:")
    for action in actions:
        print(f"  {action}")

    # Generate assertions
    assertion_gen = AssertionGenerator()
    assertions = assertion_gen.generate(actions)

    print("\nGenerated assertions:")
    for assertion in assertions:
        print(f"  {assertion}")

    # Execute the actions
    print("\nExecuting actions...")
    result = execute_actions(actions, assertions)

    print(f"\nResult: {result}")

if __name__ == "__main__":
    test_google_search()