# # from playwright.sync_api import sync_playwright

# # def run_test(playwright_code, assertion_code):
# #     with sync_playwright() as p:
# #         browser = p.chromium.launch(
# #             headless=False,
# #             slow_mo=1000   # 1000 ms = 1 second delay
# #             )

# #         page = browser.new_page()

# #         # Open local HTML file
# #         page.goto("file:///C:/Users/anupa/ANUPA_DESTOP/ai_agent/test_pages/sample_form.html")

# #         # Execute generated action
# #         exec(playwright_code)

# #         # Execute assertion
# #         try:
# #             exec(assertion_code)
# #             result = "PASS"
# #         except Exception as e:
# #             result = f"FAIL: {str(e)}"

# #         browser.close()
# #         return result
# from playwright.sync_api import sync_playwright
# import time, os

# def run_test(code, assertion):
#     steps = []
#     start = time.time()

#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False, slow_mo=900, channel="chrome")
#         page = browser.new_page()

#         page.goto("file:///C:/Users/anupa/ANUPA_DESTOP/ai_agent/test_pages/sample_form.html")
#         steps.append("Opened login page")

#         try:
#             exec(code, {"page": page})
#             steps.append("Performed actions")

#             exec(assertion, {"page": page})
#             steps.append("Assertion passed")

#             browser.close()
#             return "PASS", steps, None, round(time.time() - start, 2), None

#         except Exception as e:
#             screenshot_path = f"reports/failure_{int(time.time())}.png"
#             page.screenshot(path=screenshot_path)
#             browser.close()
#             return "FAIL", steps, str(e), round(time.time() - start, 2), screenshot_path
from playwright.sync_api import sync_playwright
import time

def run_test(code, assertion, headless):
    steps=[]
    start=time.time()
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=headless,slow_mo=800,channel="chrome")
        page=browser.new_page()
        page.goto("file:///C:/Users/anupa/ANUPA_DESTOP/ai_agent/test_pages/sample_form.html")
        steps.append("Opened login page")
        try:
            exec(code,{"page":page})
            steps.append("Performed login")
            exec(assertion,{"page":page})
            browser.close()
            return "PASS",steps,None,round(time.time()-start,2),None
        except Exception as e:
            browser.close()
            return "FAIL",steps,str(e),round(time.time()-start,2),None
