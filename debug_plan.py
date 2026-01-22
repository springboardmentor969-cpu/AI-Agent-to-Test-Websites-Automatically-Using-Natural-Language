"""
Test the exact instruction to see what the planner generates
"""
from agent.planner import plan_actions

instruction = "Navigate to http://127.0.0.1:5000/static/test_page.html, fill #username with 'admin', fill #password with 'secret', check #remember, click #login-btn"

print(f"Testing instruction: {instruction}\n")

plan = plan_actions(instruction)

print("Generated plan:")
for i, action in enumerate(plan.actions, 1):
    print(f"{i}. {action.type}")
    if action.selector:
        print(f"   Selector: {action.selector}")
    if action.value:
        print(f"   Value: {action.value}")
    print()
