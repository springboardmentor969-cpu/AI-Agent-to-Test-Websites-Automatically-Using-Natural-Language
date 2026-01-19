import asyncio
import sys

# FIX: Required for Playwright on Windows
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

from playwright.sync_api import sync_playwright


def run_test(steps, assertions):
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            # Execute steps
            for step in steps:
                try:
                    if step["type"] == "goto":
                        page.goto(step["url"], timeout=30000)
                        results.append({"action": f"Open {step['url']}", "status": "PASS"})

                    elif step["type"] == "fill":
                        selector = step["selector"]
                        value = step["value"]
                        page.fill(selector, value, timeout=10000)
                        results.append({"action": f"Fill input: {selector}", "status": "PASS"})

                    elif step["type"] == "press":
                        key = step["key"]
                        page.keyboard.press(key)
                        results.append({"action": f"Press {key}", "status": "PASS"})

                    elif step["type"] == "click":
                        selector = step["selector"]
                        page.click(selector, timeout=10000)
                        results.append({"action": f"Click: {selector}", "status": "PASS"})

                except Exception as e:
                    results.append({"action": step.get("type", "unknown"), "status": "FAIL", "error": str(e)})

            # Execute assertions
            for assertion in assertions:
                try:
                    if assertion["type"] == "page_loaded":
                        page.wait_for_load_state("load", timeout=30000)
                        results.append({"action": "Page loaded", "status": "PASS"})

                    elif assertion["type"] == "selector":
                        selector = assertion["value"]
                        page.wait_for_selector(selector, timeout=10000)
                        results.append({"action": f"Element present: {selector}", "status": "PASS"})

                    elif assertion["type"] == "text":
                        text = assertion["value"]
                        page.get_by_text(text, exact=True).wait_for(timeout=10000)
                        results.append({"action": f"Text found: {text}", "status": "PASS"})

                except Exception as e:
                    results.append({"action": assertion.get("type", "unknown"), "status": "FAIL", "error": str(e)})

        finally:
            browser.close()

    return results
