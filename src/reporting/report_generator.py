import json
import os
from datetime import datetime

def generate_report(actions, assertions, result):
    # Convert relative paths to web-accessible paths
    screenshots = []
    if result.get("screenshots"):
        for screenshot in result["screenshots"]:
            # Convert absolute path to web-accessible relative path
            if os.path.isabs(screenshot):
                # Extract just the filename from the path
                filename = os.path.basename(screenshot)
                web_path = f"screenshots/{filename}"
            else:
                # Handle relative paths (legacy)
                web_path = screenshot.replace("\\", "/").replace("tests/", "")
            screenshots.append(web_path)

    report = {
        "timestamp": str(datetime.now()),
        "actions": actions,
        "assertions": assertions,
        "result": {
            "success": result.get("success", False),
            "message": result.get("message", ""),
            "logs": result.get("logs", []),
            "screenshots": screenshots,
            "video": result.get("video", ""),
            "error": result.get("error", "")
        }
    }

    with open("test_report.json", "w") as f:
        json.dump(report, f, indent=4)

    return report
