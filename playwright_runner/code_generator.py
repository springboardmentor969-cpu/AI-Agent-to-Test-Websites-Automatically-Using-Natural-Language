# # # # # def generate_playwright_code(parsed):
# # # # #     if parsed["action"] == "click":
# # # # #         if parsed["target"] == "login":
# # # # #             return "page.click('#loginBtn')"

# # # # #         if parsed["target"] == "submit":
# # # # #             return None   # submit button does not exist

# # # # #     return None
# # # # def generate_playwright_code(parsed):
# # # #     if parsed["action"] == "click" and parsed["target"] == "login":
# # # #         return """
# # # # page.fill("#username", "admin")
# # # # page.fill("#password", "1234")
# # # # page.click("#loginBtn")
# # # # """
# # # #     return None

# # # def generate_playwright_code(parsed):
# # #     if parsed["action"] == "click":
# # #         return '''
# # # page.fill("#username", "admin")
# # # page.fill("#password", "1234")
# # # page.click("#loginBtn")
# # # '''
# # #     return None

# # def generate_playwright_code(parsed):
# #     if parsed["action"]=="click":
# #         return '''
# # page.fill("#username","admin")
# # page.fill("#password","1234")
# # page.click("#loginBtn")
# # '''
# #     return None
# def generate_playwright_code(parsed):
#     """
#     FINAL STABLE CODE GENERATOR
#     Works 100% reliably on Windows + Playwright + Node 22
#     """

#     # ---------------- LOCAL LOGIN TEST ----------------

#     if parsed["action"] == "login":
#         print("DEBUG PARSED LOGIN DATA:", parsed)

#         return f"""
# page.goto("file:///C:/Users/anupa/ANUPA_DESTOP/ai_agent/test_pages/sample_form.html")

# page.wait_for_selector("#username", timeout=10000)

# page.fill("#username", "{parsed.get('username')}")
# page.fill("#password", "{parsed.get('password')}")

# page.click("#loginBtn")
# page.wait_for_timeout(2000)
# """

#     # ---------------- SEARCH TEST (WIKIPEDIA – GUARANTEED) ----------------
#     if parsed["action"] == "search":
#         query = parsed["query"]

#         return f"""
# # Open Wikipedia (automation-friendly)
# page.goto("https://en.wikipedia.org/wiki/Main_Page", wait_until="load")

# # Wait for visible search input
# page.wait_for_selector("input[name='search']", timeout=10000)

# # Type query
# page.fill("input[name='search']", "{query}")

# # Submit search
# page.keyboard.press("Enter")

# # Wait for results page
# page.wait_for_selector("#firstHeading", timeout=10000)

# page.wait_for_timeout(2000)
# """
#     if parsed["action"] == "login":
#         return f"""
#     page.goto("file:///C:/Users/anupa/ANUPA_DESTOP/ai_agent/test_pages/sample_form.html")

#     page.wait_for_selector("#username", timeout=10000)
#     page.fill("#username", "{parsed['username']}")
#     page.fill("#password", "{parsed['password']}")

#     page.click("#loginBtn")
#     page.wait_for_timeout(2000)
#     """


#     return ""
def generate_playwright_code(parsed):
    """
    FINAL STABLE CODE GENERATOR
    - Login with NLP-extracted credentials
    - Wikipedia search (stable)
    - MongoDB Compass mock search (slow & visible)
    """

    # ---------------- LOGIN (USERNAME & PASSWORD FROM COMMAND) ----------------
    if parsed["action"] == "login":
        username = parsed.get("username", "")
        password = parsed.get("password", "")

        print("DEBUG LOGIN VALUES:", username, password)

        return f"""
page.goto("file:///C:/Users/anupa/ANUPA_DESTOP/ai_agent/test_pages/sample_form.html")
page.wait_for_timeout(2000)

page.wait_for_selector("#username", timeout=10000)
page.click("#username")
page.fill("#username", "{username}")
page.wait_for_timeout(1500)

page.click("#password")
page.fill("#password", "{password}")
page.wait_for_timeout(1500)

page.click("#loginBtn")
page.wait_for_timeout(3000)
"""

    # ---------------- SEARCH (WIKIPEDIA – STABLE) ----------------
    if parsed["action"] == "search":
        query = parsed["query"]

        return f"""
page.goto("https://en.wikipedia.org/wiki/Main_Page", wait_until="load")
page.wait_for_timeout(2000)

page.wait_for_selector("input[name='search']", timeout=10000)
page.click("input[name='search']")
page.fill("input[name='search']", "{query}")
page.wait_for_timeout(2000)

page.keyboard.press("Enter")
page.wait_for_selector("#firstHeading", timeout=10000)

page.wait_for_timeout(4000)
"""

    # ---------------- MONGODB COMPASS MOCK SEARCH ----------------
    if parsed["action"] == "mongodb_search":
        keyword = parsed["keyword"]

        return f"""
page.goto("file:///C:/Users/anupa/ANUPA_DESTOP/ai_agent/test_pages/mongodb_mock.html")
page.wait_for_timeout(2000)

page.wait_for_selector("#search", timeout=10000)
page.click("#search")
page.wait_for_timeout(1000)

page.fill("#search", "{keyword}")
page.wait_for_timeout(2000)

page.click("button")
page.wait_for_timeout(3000)

page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
page.wait_for_timeout(4000)
"""

    # ---------------- INVALID / UNSUPPORTED ----------------
    return ""
