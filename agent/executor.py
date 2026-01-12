from playwright.sync_api import sync_playwright

def execute_test(playwright_steps, assertions):
    execution_log = []
    result = "PASS"

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            for step in playwright_steps:
                exec(step)
                execution_log.append(step)

            for assertion in assertions:
                exec(assertion)
                execution_log.append(assertion)

            browser.close()

    except Exception as e:
        result = "FAIL"
        execution_log.append(str(e))

    return result, execution_log
