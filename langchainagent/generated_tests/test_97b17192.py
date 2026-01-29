from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(record_video_dir=r"D:\ai\artifacts\videos")
        page = context.new_page()
        for url in [
            "https://youtube.com",
            "https://www.youtube.com",
        ]:
            try:
                page.goto(url, wait_until='domcontentloaded', timeout=8000)
                break
            except:
                pass
        else:
            page.goto('https://www.google.com')
            page.fill("input[name='q']", "youtube")
            page.press("input[name='q']", 'Enter')
            page.wait_for_selector('h3')
            page.locator('h3').first.click()
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(1500)
        page.wait_for_selector("input[name='search_query']")
        page.click("input[name='search_query']")
        page.fill("input[name='search_query']", 'spiders')
        with page.expect_navigation():
            page.press("input[name='search_query']", 'Enter')
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(2000)
        page.wait_for_selector("ytd-video-renderer")
        assert "spiders" in page.content().lower()
        results = page.locator("ytd-video-renderer")
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