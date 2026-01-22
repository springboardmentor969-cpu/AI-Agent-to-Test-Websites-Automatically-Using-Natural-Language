"""
Test registration form to diagnose the checkbox issue
"""
from agent.planner import plan_actions

# Test registration instruction
instruction = "Navigate to http://127.0.0.1:5000/static/test_page.html, fill name with 'John Doe', fill email with 'john@test.com', select country 'United States', check terms checkbox, and click register"

print(f"Instruction: {instruction}\n")
plan = plan_actions(instruction)

print("Generated Plan:")
for i, action in enumerate(plan.actions, 1):
    print(f"{i}. Type: {action.type}")
    if action.selector:
        print(f"   Selector: {action.selector}")
    if action.value:
        print(f"   Value: {action.value}")
    print()
