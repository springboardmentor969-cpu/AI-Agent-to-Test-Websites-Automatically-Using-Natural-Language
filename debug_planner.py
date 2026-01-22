"""
Debug script to test the planner directly
"""
from agent.planner import plan_actions

instruction = "Navigate to http://127.0.0.1:5000/static/test_page.html and take a screenshot"

print("Testing planner with instruction:")
print(f"  {instruction}\n")

try:
    plan = plan_actions(instruction)
    print("✓ Planner succeeded!")
    print(f"\nGenerated plan with {len(plan.actions)} actions:")
    for i, action in enumerate(plan.actions, 1):
        print(f"  {i}. {action.type}")
        if action.selector:
            print(f"     Selector: {action.selector}")
        if action.value:
            print(f"     Value: {action.value}")
except Exception as e:
    print(f"✗ Planner failed with error:")
    print(f"  {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
