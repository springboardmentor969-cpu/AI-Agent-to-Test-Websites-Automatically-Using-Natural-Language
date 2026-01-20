#!/usr/bin/env python3
"""
Demo script for AI Agent Natural Language Testing
"""

from src.agent import agent
from src.playwright_executor.playwright_executor import execute_actions
from src.reporting.report_generator import generate_report

def demo():
    print("🚀 AI Agent Demo - Natural Language Web Testing")
    print("=" * 50)

    # Test instruction
    instruction = "open login page, enter mahi in username, enter 1234 in password, click login"

    print(f"Instruction: {instruction}")
    print("\nProcessing...")

    # Run agent
    agent_result = agent.invoke({"instruction": instruction})

    print("Parsed Actions:")
    for action in agent_result["actions"]:
        print(f"  - {action}")

    print("\nGenerated Assertions:")
    for assertion in agent_result["assertions"]:
        print(f"  - {assertion}")

    print("\nExecuting test in browser...")
    # Note: This will open a browser window
    execution_result = execute_actions(agent_result["actions"], agent_result["assertions"])

    print(f"Execution Result: {execution_result}")

    # Generate report
    report = generate_report(agent_result["actions"], agent_result["assertions"], execution_result)
    print("\nTest Report Generated:")
    print(report)

if __name__ == "__main__":
    demo()