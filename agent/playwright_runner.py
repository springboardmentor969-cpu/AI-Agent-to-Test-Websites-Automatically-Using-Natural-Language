from playwright.sync_api import sync_playwright


def run_test(steps, assertions):
    result = "PASS"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Execute steps
        for step in steps:
            if step["action"] == "open_url":
                page.goto(step["value"])

            elif step["action"] == "fill":
                page.fill(step["selector"], step["text"])

            elif step["action"] == "click":
                page.click(step["value"])

        # Execute assertions
        try:
            for assertion in assertions:
                if assertion["type"] == "element_visible":
                    assert page.locator(assertion["selector"]).is_visible()
        except:
            result = "FAIL"

        browser.close()

    return result
