"""
Quick test to verify planner generates correct selectors
"""
from dotenv import load_dotenv
load_dotenv()

from agent.planner import plan_actions

# Test the exact instruction from the user
instruction = "Navigate to http://127.0.0.1:5000/static/test_page.html, fill name with 'John Doe', fill email with 'john@example.com', select country 'USA', check the terms checkbox, and click register"

print("Testing planner with instruction:")
print(f"  {instruction}\n")

plan = plan_actions(instruction)

print("Generated plan:")
for i, action in enumerate(plan.actions, 1):
    print(f"  {i}. {action.type}")
    if action.selector:
        print(f"     Selector: {action.selector}")
    if action.value:
        print(f"     Value: {action.value}")
    print()

print("✓ Planner test complete!")
