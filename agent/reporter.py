def generate_report(steps, step_results, error):
    return {
        "summary": "Test executed successfully" if not error else "Test failed",
        "total_steps": len(steps),
        "passed": len([r for r in step_results if r["status"] == "PASS"]),
        "failed": 0 if not error else 1,
        "error": error
    }
