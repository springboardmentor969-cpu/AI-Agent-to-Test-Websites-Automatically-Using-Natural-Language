from playwright.sync_api import sync_playwright

def run_test(steps, assertions, headless=True):
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(
            channel="chrome",
            headless=headless
        )
        page = browser.new_page()

        # Execute steps
        for step in steps:
            try:
                eval(step)
                results.append({
                    "action": step,
                    "status": "PASS"
                })
            except Exception as e:
                results.append({
                    "action": step,
                    "status": "FAIL",
                    "error": str(e)
                })

        # Execute assertions
        for assertion in assertions:
            try:
                eval(assertion)
                results.append({
                    "action": assertion,
                    "status": "PASS"
                })
            except Exception as e:
                results.append({
                    "action": assertion,
                    "status": "FAIL",
                    "error": str(e)
                })

        browser.close()

    return results
