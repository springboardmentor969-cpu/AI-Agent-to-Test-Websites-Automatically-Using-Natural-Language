"""
Test registration form with the fixed selectors
"""
from agent.workflow import create_workflow

instruction = "Navigate to http://127.0.0.1:5000/static/test_page.html, fill name with 'John Doe', email with 'john@test.com', select country 'United States', check terms checkbox, and click register"

print(f"Testing: {instruction}\n")

workflow = create_workflow()
result = workflow.invoke({"instruction": instruction})
report = result.get("report")

print(f"\nStatus: {report.get('status')}")
print(f"Total Steps: {report.get('total_steps')}")
print(f"Passed: {report.get('passed')}")
print(f"Failed: {report.get('failed')}")

if report.get('status') == 'PASS':
    print("✅ TEST PASSED")
else:
    print("❌ TEST FAILED")
    for step in report.get('steps', []):
        if not step.get('success'):
            print(f"  Failed step: {step.get('action_type')} - {step.get('error')}")
