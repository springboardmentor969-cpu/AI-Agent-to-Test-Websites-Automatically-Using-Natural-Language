from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(record_video_dir=r"D:\ai\artifacts\videos")
        page = context.new_page()
        for url in [
            "https://wikipedia.com",
            "https://www.wikipedia.com",
        ]:
            try:
                page.goto(url, wait_until='domcontentloaded', timeout=8000)
                break
            except:
                pass
        else:
            page.goto('https://www.google.com')
            page.fill("input[name='q']", "wikipedia")
            page.press("input[name='q']", 'Enter')
            page.wait_for_selector('h3')
            page.locator('h3').first.click()
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(1500)
        page.wait_for_selector("input[name='search']")
        page.click("input[name='search']")
        page.fill("input[name='search']", 'openai')
        with page.expect_navigation():
            page.press("input[name='search']", 'Enter')
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(2000)
        page.wait_for_selector("#mw-content-text")
        assert "openai" in page.content().lower()
        results = page.locator("#mw-content-text")
        if results.count() > 0:
            with context.expect_page() as p2:
                results.first.click()
            tab = p2.value
            tab.wait_for_load_state('networkidle')
            tab.screenshot(path=r"D:\ai\artifacts\screenshots\detail.png")
            tab.close()
        page.screenshot(path=r"D:\ai\artifacts\screenshots\final.png")
        context.close()
        browser.close()

if __name__ == '__main__':
    run()