from playwright.sync_api import sync_playwright

def test_home_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://127.0.0.1:5000")
        title = page.title()
        print("Page title:", title)
        assert "Welcome" in page.content()
        browser.close()

if __name__ == "__main__":
    test_home_page()
