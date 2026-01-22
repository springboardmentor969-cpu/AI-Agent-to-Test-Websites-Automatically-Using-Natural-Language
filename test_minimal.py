"""
Minimal test to see full error
"""
import sys
import traceback
from dotenv import load_dotenv
load_dotenv()

try:
    print("Step 1: Importing workflow...")
    from agent.workflow import create_workflow
    
    print("Step 2: Creating workflow...")
    workflow = create_workflow()
    
    print("Step 3: Invoking workflow...")
    result = workflow.invoke({"instruction": "test"})
    
    print(f"Step 4: Success! Result: {result}")
    
except Exception as e:
    print(f"\n{'='*70}")
    print(f"ERROR: {type(e).__name__}")
    print(f"Message: {str(e)}")
    print(f"{'='*70}\n")
    
    print("Full traceback:")
    traceback.print_exc(file=sys.stdout)
    
    print(f"\n{'='*70}")
    print("Exception details:")
    print(f"  Type: {type(e)}")
    print(f"  Args: {e.args}")
    if hasattr(e, '__dict__'):
        print(f"  Dict: {e.__dict__}")
