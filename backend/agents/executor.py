from playwright.sync_api import sync_playwright
import os
from reports.formatter import format_report

def execute_test(state):
    results = []

    demo_page_path = os.path.abspath("tests/static/demo.html")
    demo_url = f"file://{demo_page_path}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            for step in state["steps"]:
                action = step.get("action")

                if action == "open":
                    page.goto(demo_url)
                    results.append({"step": "Open page", "status": "PASS"})

                elif action == "fill":
                    page.fill(step["selector"], step["value"])
                    results.append({"step": "Fill email", "status": "PASS"})

                elif action == "click":
                    page.click(step["selector"])
                    results.append({"step": "Click submit", "status": "PASS"})

                elif action == "assert_text":
                    page.wait_for_selector(f"text={step['text']}")
                    results.append({"step": "Verify success", "status": "PASS"})

            browser.close()

        except Exception as e:
            browser.close()
            results.append({
                "step": "Execution error",
                "status": "FAIL",
                "error": str(e)
            })

    # ✅ Professional report output
    return format_report(results)
