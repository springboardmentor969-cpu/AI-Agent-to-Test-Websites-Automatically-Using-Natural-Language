"""
Test DeepLearning.AI with automatic selector discovery
"""
from agent.workflow import create_workflow

instruction = "go to deeplearning.ai and click start learning and enter email id as deepshika0408@gmail.com and password as hello"

print(f"\n{'='*80}")
print(f"Testing: {instruction}")
print(f"{'='*80}\n")

workflow = create_workflow()
try:
    result = workflow.invoke({"instruction": instruction})
    report = result.get("report")
    
    print(f"\n{'='*80}")
    print("RESULT")
    print(f"{'='*80}")
    print(f"Status: {report.get('status')}")
    print(f"Total Steps: {report.get('total_steps')}")
    print(f"Passed: {report.get('passed')}")
    print(f"Failed: {report.get('failed')}")
    print(f"Execution Time: {report.get('execution_time_sec')}s")
    
    if report.get('status') == 'PASS':
        print("\n✅ TEST PASSED - Automatic selector discovery works!")
    else:
        print("\n❌ TEST FAILED")
        print("\nFailed steps:")
        for step in report.get('steps', []):
            if not step.get('success'):
                print(f"  Step {step.get('step_number')}: {step.get('action_type')}")
                print(f"    Selector: {step.get('selector')}")
                print(f"    Error: {step.get('error')}")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
