from typing import List, Dict
from agent.schemas import ExecutionStepResult
import json
import os
from datetime import datetime

def build_report(results: List[ExecutionStepResult]) -> dict:
    """Build a detailed test execution report"""
    total_steps = len(results)
    passed = sum(1 for r in results if r.success)
    failed = total_steps - passed
    total_time = sum(r.execution_time_ms for r in results)
    
    # Format steps for display
    formatted_steps = []
    for i, result in enumerate(results, 1):
        step_data = {
            "step_number": i,
            "action_type": result.action.type,
            "selector": result.action.selector,
            "value": result.action.value,
            "success": result.success,
            "error": result.error,
            "screenshot": result.screenshot_path,
            "timestamp": result.timestamp,
            "execution_time_ms": result.execution_time_ms
        }
        formatted_steps.append(step_data)
    
    report = {
        "status": "PASS" if failed == 0 else "FAIL",
        "total_steps": total_steps,
        "passed": passed,
        "failed": failed,
        "execution_time_ms": total_time,
        "execution_time_sec": round(total_time / 1000, 2),
        "steps": formatted_steps,
        "screenshots": [r.screenshot_path for r in results if r.screenshot_path]
    }
    
    # Auto-save report to reports folder
    try:
        reports_dir = "reports"
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        status = report["status"].lower()
        filename = f"test_report_{status}_{timestamp}.json"
        filepath = os.path.join(reports_dir, filename)
        
        # Create detailed JSON report
        detailed_report = {
            "timestamp": datetime.now().isoformat(),
            "status": report["status"],
            "statistics": {
                "total_steps": total_steps,
                "passed": passed,
                "failed": failed,
                "execution_time_sec": report["execution_time_sec"]
            },
            "execution_steps": formatted_steps
        }
        
        with open(filepath, 'w') as f:
            json.dump(detailed_report, f, indent=2)
        
        print(f"\n✓ Report auto-saved to: {filepath}")
    except Exception as e:
        print(f"\n✗ Failed to auto-save report: {e}")
    
    return report

