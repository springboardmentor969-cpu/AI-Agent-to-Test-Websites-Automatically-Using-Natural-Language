"""
Direct test to see what's happening with the workflow
"""
from dotenv import load_dotenv
load_dotenv()

from agent.workflow import create_workflow

# Test instruction
instruction = "Navigate to http://127.0.0.1:5000/static/test_page.html, fill username with 'admin', fill password with 'secret', check remember me checkbox, and click login button"

print("="*80)
print("Testing workflow with instruction:")
print(instruction)
print("="*80)

workflow = create_workflow()
result = workflow.invoke({"instruction": instruction})

print("\n" + "="*80)
print("RESULTS:")
print("="*80)

report = result.get("report", {})
print(f"\nStatus: {report.get('status')}")
print(f"Total Steps: {report.get('total_steps')}")
print(f"Passed: {report.get('passed')}")
print(f"Failed: {report.get('failed')}")
print(f"Execution Time: {report.get('execution_time_sec')}s")

print("\n" + "="*80)
print("STEP DETAILS:")
print("="*80)

for step in report.get('steps', []):
    print(f"\nStep {step.get('step_number')}: {step.get('action_type')}")
    print(f"  Success: {step.get('success')}")
    if step.get('selector'):
        print(f"  Selector: {step.get('selector')}")
    if step.get('value'):
        print(f"  Value: {step.get('value')}")
    if step.get('error'):
        print(f"  ERROR: {step.get('error')}")
    if step.get('screenshot'):
        print(f"  Screenshot: {step.get('screenshot')}")

print("\n" + "="*80)
print("PLAN GENERATED:")
print("="*80)
plan = result.get('plan')
if plan:
    for i, action in enumerate(plan.actions, 1):
        print(f"{i}. {action.type}: selector='{action.selector}', value='{action.value}'")
