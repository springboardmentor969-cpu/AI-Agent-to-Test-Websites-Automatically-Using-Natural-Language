from playwright.sync_api import sync_playwright

def execute_test(parsed_steps):
    results = []
    error = None

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, slow_mo=800)
            page = browser.new_page()

            for step in parsed_steps:
                action = step.get("action", "").lower()

                if action in ["open", "open_url"]:
                    url = step.get("value")
                    if url:
                        page.goto(url)
                        page.wait_for_load_state("networkidle")
                        results.append({"step": url, "status": "PASS"})
                    else:
                        results.append({"step": str(step), "status": "FAIL", "reason": "No URL provided"})

                elif action == "fill":
                    selector = step.get("selector")
                    text = step.get("text", "")
                    if selector:
                        page.wait_for_selector(selector)
                        page.fill(selector, text)
                        results.append({"step": f"Fill {selector} with '{text}'", "status": "PASS"})
                    else:
                        results.append({"step": str(step), "status": "FAIL", "reason": "No selector provided"})

                elif action == "click":
                    selector = step.get("selector")
                    if selector:
                        page.wait_for_selector(selector)
                        page.click(selector)
                        results.append({"step": f"Click {selector}", "status": "PASS"})
                    else:
                        results.append({"step": str(step), "status": "FAIL", "reason": "No selector provided"})

            page.wait_for_timeout(2000)
            browser.close()

    except Exception as e:
        results.append({"step": "Execution failed", "status": "FAIL", "reason": str(e)})
        error = str(e)

    return results, error
