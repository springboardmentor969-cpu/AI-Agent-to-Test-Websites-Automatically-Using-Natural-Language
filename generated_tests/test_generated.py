from playwright.sync_api import sync_playwright, expect

def test_generated():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        page.goto("http://127.0.0.1:5000/login", wait_until='domcontentloaded', timeout=10000)

        context.close()
        browser.close()