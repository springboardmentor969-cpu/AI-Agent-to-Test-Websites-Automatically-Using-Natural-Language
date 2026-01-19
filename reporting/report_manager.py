def generate_report(results):
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = sum(1 for r in results if r["status"] == "FAIL")

    return {
        "total_tests": len(results),
        "passed": passed,
        "failed": failed,
        "details": results
    }
