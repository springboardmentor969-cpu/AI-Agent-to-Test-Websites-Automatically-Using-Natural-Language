"""Test the workflow with a simple instruction"""
from agent.workflow import create_workflow

workflow = create_workflow()

instruction = "Navigate to http://127.0.0.1:5000/static/test_page.html, fill #username with 'admin', fill #password with 'secret', check #remember, click #login-btn"

print(f"Testing instruction: {instruction}\n")

try:
    result = workflow.invoke({"instruction": instruction})
    print("SUCCESS!")
    print(f"Report status: {result['report']['status']}")
    print(f"Steps: {result['report']['total_steps']}")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
