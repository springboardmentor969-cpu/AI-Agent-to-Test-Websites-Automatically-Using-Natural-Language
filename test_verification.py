"""
Simple test script to verify the AI Testing Agent functionality
"""
from dotenv import load_dotenv
load_dotenv()  # Load environment variables first

from agent.workflow import create_workflow

def test_basic_navigation():
    """Test basic navigation and screenshot"""
    print("=" * 60)
    print("TEST 1: Basic Navigation and Screenshot")
    print("=" * 60)
    
    workflow = create_workflow()
    instruction = "Navigate to http://127.0.0.1:5000/static/test_page.html and take a screenshot"
    
    try:
        result = workflow.invoke({"instruction": instruction})
        report = result.get("report")
        
        print(f"\nStatus: {report['status']}")
        print(f"Total Steps: {report['total_steps']}")
        print(f"Passed: {report['passed']}")
        print(f"Failed: {report['failed']}")
        print(f"Execution Time: {report['execution_time_sec']}s")
        
        print("\nSteps:")
        for step in report['steps']:
            status_icon = "✓" if step['success'] else "✗"
            print(f"  {status_icon} Step {step['step_number']}: {step['action_type']}")
            if step.get('error'):
                print(f"    Error: {step['error']}")
            if step.get('screenshot'):
                print(f"    Screenshot: {step['screenshot']}")
        
        return report['status'] == 'PASS'
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_form_filling():
    """Test form filling"""
    print("\n" + "=" * 60)
    print("TEST 2: Form Filling")
    print("=" * 60)
    
    workflow = create_workflow()
    instruction = "Navigate to http://127.0.0.1:5000/static/test_page.html, fill username with 'testuser', fill password with 'testpass', and click the login button"
    
    try:
        result = workflow.invoke({"instruction": instruction})
        report = result.get("report")
        
        print(f"\nStatus: {report['status']}")
        print(f"Total Steps: {report['total_steps']}")
        print(f"Passed: {report['passed']}")
        print(f"Failed: {report['failed']}")
        
        print("\nSteps:")
        for step in report['steps']:
            status_icon = "✓" if step['success'] else "✗"
            print(f"  {status_icon} Step {step['step_number']}: {step['action_type']}")
            if step.get('selector'):
                print(f"    Selector: {step['selector']}")
            if step.get('value'):
                print(f"    Value: {step['value']}")
        
        return report['status'] == 'PASS'
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n🤖 AI Website Testing Agent - Verification Tests\n")
    
    results = []
    
    # Test 1
    results.append(("Basic Navigation", test_basic_navigation()))
    
    # Test 2
    results.append(("Form Filling", test_form_filling()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    total_passed = sum(1 for _, passed in results if passed)
    print(f"\nTotal: {total_passed}/{len(results)} tests passed")
