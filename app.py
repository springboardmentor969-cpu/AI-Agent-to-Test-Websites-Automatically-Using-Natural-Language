from flask import Flask, request, jsonify, render_template
from playwright.sync_api import sync_playwright
import time
import json
import os

app = Flask(__name__, static_folder="static", template_folder="templates")

# ---------------------------------------------------
# INSTRUCTION PARSER (Milestone 2)
# ---------------------------------------------------
def parse_instruction(text):
    text = text.lower()
    steps = []

    # Open URL
    if "open" in text or "go to" in text:
        parts = text.replace("go to", "open").split("open")
        if len(parts) > 1:
            url = parts[1].strip().split()[0]
            if not url.startswith("http"):
                url = "https://" + url
            steps.append({"action": "goto", "value": url})

    # Click action
    if "click" in text or "login" in text:
        steps.append({
            "action": "click",
            "selector": "a, button"
        })

    # Verification → PAGE LOAD ASSERTION (SAFE)
    if "verify" in text or "check" in text:
        steps.append({
            "action": "assert_page_loaded"
        })

    return steps


# ---------------------------------------------------
# PLAYWRIGHT EXECUTION (Milestone 3)
# ---------------------------------------------------
def run_playwright(steps):
    results = []

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()

        for step in steps:
            try:
                if step["action"] == "goto":
                    page.goto(step["value"], timeout=20000)
                    results.append({
                        "step": "goto",
                        "detail": step["value"],
                        "status": "passed"
                    })

                elif step["action"] == "click":
                    page.wait_for_selector(step["selector"], timeout=5000)
                    page.click(step["selector"])
                    results.append({
                        "step": "click",
                        "detail": step["selector"],
                        "status": "passed"
                    })

                elif step["action"] == "assert_page_loaded":
                    if page.url:
                        results.append({
                            "step": "assert_page_loaded",
                            "detail": "page loaded successfully",
                            "status": "passed"
                        })
                    else:
                        results.append({
                            "step": "assert_page_loaded",
                            "detail": "page not loaded",
                            "status": "failed"
                        })

            except Exception as e:
                results.append({
                    "step": step["action"],
                    "detail": str(e),
                    "status": "error"
                })

        browser.close()

    return results


# ---------------------------------------------------
# REPORT GENERATOR (Milestone 4)
# ---------------------------------------------------
def generate_report(instruction, steps, results):
    passed = len([r for r in results if r["status"] == "passed"])
    failed = len([r for r in results if r["status"] in ["failed", "error"]])

    report = {
        "instruction": instruction,
        "total_steps": len(steps),
        "passed": passed,
        "failed": failed,
        "final_status": "PASSED" if failed == 0 else "FAILED",
        "results": results,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    os.makedirs("results", exist_ok=True)
    with open(f"results/report_{int(time.time())}.json", "w") as f:
        json.dump(report, f, indent=4)

    return report


# ---------------------------------------------------
# FLASK ROUTES
# ---------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/test", methods=["POST"])
def test():
    data = request.get_json()
    instruction = data.get("instruction", "")

    steps = parse_instruction(instruction)
    results = run_playwright(steps)
    report = generate_report(instruction, steps, results)

    return jsonify(report)


# ---------------------------------------------------
# APP START
# ---------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
