"""
Test the three main test cases to verify fixes
"""
from agent.workflow import create_workflow

def test_case(instruction):
    print(f"\n{'='*80}")
    print(f"Testing: {instruction}")
    print(f"{'='*80}\n")
    
    workflow = create_workflow()
    try:
        result = workflow.invoke({"instruction": instruction})
        report = result.get("report")
        
        print(f"\nStatus: {report.get('status')}")
        print(f"Total Steps: {report.get('total_steps')}")
        print(f"Passed: {report.get('passed')}")
        print(f"Failed: {report.get('failed')}")
        print(f"Execution Time: {report.get('execution_time_sec')}s")
        
        if report.get('status') == 'PASS':
            print("✅ TEST PASSED")
        else:
            print("❌ TEST FAILED")
            for step in report.get('steps', []):
                if not step.get('success'):
                    print(f"  Failed step: {step.get('action_type')} - {step.get('error')}")
        
        return report.get('status') == 'PASS'
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    test_cases = [
        "Navigate to http://127.0.0.1:5000/static/test_page.html, fill search input with 'AI testing', and click search button",
        "Navigate to http://127.0.0.1:5000/static/test_page.html, fill username with 'admin', password with 'secret', check remember me checkbox, and click login",
        "search machine learning"
    ]
    
    results = []
    for test in test_cases:
        passed = test_case(test)
        results.append(passed)
    
    print(f"\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}")
    print(f"Total: {len(results)}")
    print(f"Passed: {sum(results)}")
    print(f"Failed: {len(results) - sum(results)}")
    print(f"Success Rate: {sum(results)/len(results)*100:.1f}%")
