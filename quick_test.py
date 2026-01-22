"""
Quick Test Script - Run this to verify the system works
"""
from agent.workflow import create_workflow

# Create workflow
workflow = create_workflow()

# Simple test
print("Testing workflow...")
try:
    result = workflow.invoke({
        "instruction": "Navigate to http://127.0.0.1:5000/static/test_page.html and take a screenshot"
    })
    print("✅ SUCCESS! Workflow is working")
    print(f"Results: {len(result['results'])} steps executed")
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
