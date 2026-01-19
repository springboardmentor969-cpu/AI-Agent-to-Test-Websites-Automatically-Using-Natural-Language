# # # # from playwright.sync_api import sync_playwright

# # # # def run_test(playwright_code, assertion_code):
# # # #     with sync_playwright() as p:
# # # #         browser = p.chromium.launch(
# # # #             headless=False,
# # # #             slow_mo=1000   # 1000 ms = 1 second delay
# # # #             )

# # # #         page = browser.new_page()

# # # #         # Open local HTML file
# # # #         page.goto("file:///C:/Users/anupa/ANUPA_DESTOP/ai_agent/test_pages/sample_form.html")

# # # #         # Execute generated action
# # # #         exec(playwright_code)

# # # #         # Execute assertion
# # # #         try:
# # # #             exec(assertion_code)
# # # #             result = "PASS"
# # # #         except Exception as e:
# # # #             result = f"FAIL: {str(e)}"

# # # #         browser.close()
# # # #         return result
# # # from playwright.sync_api import sync_playwright
# # # import time, os

# # # def run_test(code, assertion):
# # #     steps = []
# # #     start = time.time()

# # #     with sync_playwright() as p:
# # #         browser = p.chromium.launch(headless=False, slow_mo=900, channel="chrome")
# # #         page = browser.new_page()

# # #         page.goto("file:///C:/Users/anupa/ANUPA_DESTOP/ai_agent/test_pages/sample_form.html")
# # #         steps.append("Opened login page")

# # #         try:
# # #             exec(code, {"page": page})
# # #             steps.append("Performed actions")

# # #             exec(assertion, {"page": page})
# # #             steps.append("Assertion passed")

# # #             browser.close()
# # #             return "PASS", steps, None, round(time.time() - start, 2), None

# # #         except Exception as e:
# # #             screenshot_path = f"reports/failure_{int(time.time())}.png"
# # #             page.screenshot(path=screenshot_path)
# # #             browser.close()
# # #             return "FAIL", steps, str(e), round(time.time() - start, 2), screenshot_path
# # from playwright.sync_api import sync_playwright
# # import time
# # from playwright_runner.ai_selector import find_element

# # def run_test(code, assertion, headless):
# #     steps=[]
# #     start=time.time()
# #     with sync_playwright() as p:
# #         browser=p.chromium.launch(headless=headless,slow_mo=800,channel="chrome")
# #         page=browser.new_page()
# #         page.goto("file:///C:/Users/anupa/ANUPA_DESTOP/ai_agent/test_pages/sample_form.html")
# #         steps.append("Opened login page")
# #         try:
# #             exec(code,{"page":page})
# #             steps.append("Performed login")
# #             exec(assertion,{"page":page})
# #             browser.close()
# #             return "PASS",steps,None,round(time.time()-start,2),None
# #         except Exception as e:
# #             browser.close()
# #             return "FAIL",steps,str(e),round(time.time()-start,2),None
# from playwright.sync_api import sync_playwright
# import time

# def run_test(code, assertion, headless):
#     steps = []
#     start = time.time()

#     with sync_playwright() as p:
#         browser = p.chromium.launch(
#             headless=headless,
#             slow_mo=600
#         )
#         steps.append("Browser launched")

#         page = browser.new_page()
#         steps.append("New page created")

#         try:
#             exec(code, {"page": page})
#             steps.append("Automation code executed")

#             exec(assertion, {"page": page})
#             steps.append("Assertion passed")

#             status = "PASS"
#             error = None

#         except Exception as e:
#             status = "FAIL"
#             error = str(e)
#             steps.append(f"Error occurred: {error}")

#         duration = round(time.time() - start, 2)
#         browser.close()
#         steps.append("Browser closed")

#     return {
#         "status": status,
#         "steps": steps,
#         "generated_code": code,
#         "duration_seconds": duration,
#         "error": error
#     }
from playwright.sync_api import sync_playwright
import time

def run_test(code, assertion, headless):
    steps = []
    start = time.time()
    error = None
    screenshot = None

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless, slow_mo=400)
        page = browser.new_page()

        try:
            steps.append("Browser launched")
            exec(code, {"page": page})
            steps.append("Automation steps executed")

            exec(assertion, {"page": page})
            steps.append("Assertion passed")

            status = "PASS"

        except Exception as e:
            status = "FAIL"
            error = str(e)
            steps.append(f"Error: {error}")

        finally:
            browser.close()
            steps.append("Browser closed")

    duration = round(time.time() - start, 2)
    return status, steps, error, duration, screenshot
