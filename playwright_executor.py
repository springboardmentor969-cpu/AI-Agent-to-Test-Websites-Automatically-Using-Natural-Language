from playwright.sync_api import sync_playwright
from assertions import validate
from time import sleep
import os
def run_actions(actions, commands, target=None):
    results = []
    HEADLESS = os.getenv("HEADLESS", "1") == "1"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        page = browser.new_page()
        for cmd in commands:
            if cmd == "login":
                page.goto("http://127.0.0.1:5000/login")
                page.fill("#username", "testuser")
                page.fill("#password", "password")
                page.click("#login-btn")
                sleep(0.3)
                result = page.inner_text("#login-status")
            elif cmd == "search":
                q = target or "laptop"
                page.goto("http://127.0.0.1:5000/search")
                page.fill("#query", q)
                page.click("#search-btn")
                sleep(0.3)
                result = page.inner_text("#search-status")
            else:
                result = "Unsupported"
            passed = validate(cmd, result)
            results.append({
                "command": cmd,
                "output": result,
                "passed": passed
            })
        browser.close()
    return results