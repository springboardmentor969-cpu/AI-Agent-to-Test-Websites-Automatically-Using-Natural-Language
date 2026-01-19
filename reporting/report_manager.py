def generate_report(results):
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = sum(1 for r in results if r["status"] == "FAIL")
    success_rate = (passed / len(results) * 100) if results else 0

    return {
        "total_tests": len(results),
        "passed": passed,
        "failed": failed,
        "success_rate": f"{success_rate:.1f}%",
        "details": results
    }
