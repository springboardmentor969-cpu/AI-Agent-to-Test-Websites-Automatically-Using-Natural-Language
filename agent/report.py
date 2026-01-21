from datetime import datetime
import json
import os

REPORT_DIR = "reports"
os.makedirs(REPORT_DIR, exist_ok=True)


def generate_report(instruction, execution):
    return {
        "instruction": instruction,
        "status": execution["status"],
        "timestamp": execution["timestamp"],
        "steps": execution["details"],
        "execution_time": execution.get("execution_time", "N/A"),
        "browser": "Chromium (Headless)"
    }

# 1️⃣ JSON REPORT
def save_json(report):
    filename = f"{REPORT_DIR}/report_{int(datetime.now().timestamp())}.json"
    with open(filename, "w") as f:
        json.dump(report, f, indent=2)
    return filename


# 2️⃣ HTML REPORT
def save_html(report):
    filename = f"{REPORT_DIR}/report_{int(datetime.now().timestamp())}.html"

    html = f"""
    <html>
    <head>
        <title>Test Report</title>
        <style>
            body {{ font-family: Arial; padding: 20px; }}
            .pass {{ color: green; }}
            .fail {{ color: red; }}
        </style>
    </head>
    <body>
        <h2>Automation Test Report</h2>
        <p><b>Instruction:</b> {report['instruction']}</p>
        <p><b>Status:</b>
            <span class="{report['status'].lower()}">
                {report['status']}
            </span>
        </p>
        <p><b>Timestamp:</b> {report['timestamp']}</p>

        <h3>Execution Steps</h3>
        <ul>
            {''.join(f"<li>{step}</li>" for step in report['steps'])}
        </ul>
    </body>
    </html>
    """

    with open(filename, "w") as f:
        f.write(html)

    return filename
