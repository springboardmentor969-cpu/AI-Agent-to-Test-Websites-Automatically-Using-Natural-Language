from datetime import datetime

def generate_report(state: dict):
    execution = state.get("execution_result", {})

    status = "PASSED" if execution.get("result") == "PASSED" else "FAILED"

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "instruction": state.get("instruction"),
        "target_url": state.get("target_url"),
        "status": status,
        "screenshot": execution.get("screenshot"),
        "error": execution.get("error"),
    }
