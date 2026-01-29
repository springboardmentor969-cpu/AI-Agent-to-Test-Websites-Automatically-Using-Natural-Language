from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(record_video_dir=r"D:\ai\artifacts\videos")
        page = context.new_page()
        for url in [
            "https://pixiv.com",
            "https://www.pixiv.com",
        ]:
            try:
                page.goto(url, wait_until='domcontentloaded', timeout=8000)
                break
            except:
                pass
        else:
            page.goto('https://www.google.com')
            page.fill("input[name='q']", "pixiv")
            page.press("input[name='q']", 'Enter')
            page.wait_for_selector('h3')
            page.locator('h3').first.click()
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(1500)
        page.screenshot(path=r"D:\ai\artifacts\screenshots\final.png")
        context.close()
        browser.close()

if __name__ == '__main__':
    run()