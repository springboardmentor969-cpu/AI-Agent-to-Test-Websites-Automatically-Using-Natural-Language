"""
Test the workflow directly to see the exact error
"""
from dotenv import load_dotenv
load_dotenv()

from agent.workflow import create_workflow

print("Creating workflow...")
workflow = create_workflow()

print("Testing workflow with instruction...")
instruction = "Navigate to http://127.0.0.1:5000/static/test_page.html"

try:
    print(f"Input: {{'instruction': '{instruction}'}}")
    result = workflow.invoke({"instruction": instruction})
    print(f"\n✓ Success!")
    print(f"Result keys: {result.keys()}")
    print(f"Report: {result.get('report')}")
except Exception as e:
    print(f"\n✗ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
