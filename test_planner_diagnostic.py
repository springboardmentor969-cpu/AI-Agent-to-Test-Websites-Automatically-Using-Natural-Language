"""
Diagnostic script to see what the planner generates
"""
from agent.planner import plan_actions

# Test the problematic instruction
instruction = "Navigate to http://127.0.0.1:5000/static/test_page.html, fill username with 'admin', password with 'secret', check remember me checkbox, and click login"

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
