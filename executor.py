from playwright.sync_api import sync_playwright
import os
import traceback

def execute_test(action_block: str):
    os.makedirs("screenshots", exist_ok=True)

    result = {
        "result": "PASSED",
        "error": None,
        "screenshot": None
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            
            exec(action_block, {"page": page})

            screenshot_path = "screenshots/test.png"
            page.screenshot(path=screenshot_path)
            result["screenshot"] = f"/screenshots/test.png"

        except Exception as e:
            result["result"] = "FAILED"
            result["error"] = str(e)
            traceback.print_exc()

        finally:
            browser.close()

    return result
