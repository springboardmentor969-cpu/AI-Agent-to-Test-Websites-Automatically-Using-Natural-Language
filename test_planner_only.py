"""
Test just the planner
"""
from dotenv import load_dotenv
load_dotenv()

from agent.planner import plan_actions

instruction = "Navigate to http://127.0.0.1:5000/static/test_page.html"

print(f"Testing planner with: {instruction}\n")

try:
    plan = plan_actions(instruction)
    print(f"✓ Success!")
    print(f"Generated {len(plan.actions)} actions:")
    for i, action in enumerate(plan.actions, 1):
        print(f"  {i}. {action.type}: {action.selector or action.value}")
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
