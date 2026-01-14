import os
from datetime import datetime
from playwright.sync_api import sync_playwright

def execute_test(playwright_steps, assertions):
    execution_log = []
    result = "PASS"
    screenshot_path = None

    os.makedirs("screenshots", exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            # Execute steps
            for step in playwright_steps:
                exec(step)
                execution_log.append(step)

            # Execute assertions
            for assertion in assertions:
                exec(assertion)
                execution_log.append(assertion)

        except Exception as e:
            result = "FAIL"
            execution_log.append(str(e))

            # ✅ TAKE SCREENSHOT IMMEDIATELY
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"screenshots/fail_{timestamp}.png"

            try:
                page.screenshot(path=screenshot_path, full_page=True)
            except Exception as se:
                execution_log.append(f"Screenshot error: {se}")

        finally:
            browser.close()

    return result, execution_log, screenshot_path
