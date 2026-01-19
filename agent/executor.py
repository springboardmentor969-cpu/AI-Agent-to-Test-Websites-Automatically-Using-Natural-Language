from playwright.sync_api import sync_playwright

def execute_test(parsed_steps):
    results = []
    error = None

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=False,
                slow_mo=800
            )
            page = browser.new_page()

            for step in parsed_steps:
                if step["action"] in ["open", "open_url"]:
                    page.goto(step["value"])
                    page.wait_for_load_state("networkidle")
                    results.append({"step": step["value"], "status": "PASS"})

                elif step["action"] == "fill":
                    page.wait_for_selector(step["selector"])
                    page.fill(step["selector"], step["text"])
                    results.append({"step": step["selector"], "status": "PASS"})

                elif step["action"] == "click":
                    page.wait_for_selector(step["value"])
                    page.click(step["value"])
                    results.append({"step": step["value"], "status": "PASS"})

            page.wait_for_timeout(2000)
            browser.close()

    except Exception as e:
        error = str(e)

    return results, error
