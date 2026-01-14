import json
from datetime import datetime
import os

def save_report(user_input, parsed_steps, result, execution_log, screenshot_path=None):
    os.makedirs("reports", exist_ok=True)
    report_path = "reports/reports.json"

    entry = {
        "timestamp": str(datetime.now()),
        "user_input": user_input,
        "parsed_steps": parsed_steps,
        "result": result,
        "execution_log": execution_log
    }

    if screenshot_path:
        entry["screenshot"] = screenshot_path

    if os.path.exists(report_path):
        with open(report_path, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(entry)

    with open(report_path, "w") as f:
        json.dump(data, f, indent=2)
