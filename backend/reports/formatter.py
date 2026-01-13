from datetime import datetime

def format_report(details):
    return {
        "metadata": {
            "executed_at": datetime.utcnow().isoformat() + "Z",
            "engine": "Infy-2005 AI Test Engine",
            "mode": "headless"
        },
        "summary": {
            "total": len(details),
            "passed": sum(1 for d in details if d["status"] == "PASS"),
            "failed": sum(1 for d in details if d["status"] == "FAIL")
        },
        "steps": details
    }
