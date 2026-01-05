# # # def generate_playwright_code(parsed):
# # #     if parsed["action"] == "click":
# # #         if parsed["target"] == "login":
# # #             return "page.click('#loginBtn')"

# # #         if parsed["target"] == "submit":
# # #             return None   # submit button does not exist

# # #     return None
# # def generate_playwright_code(parsed):
# #     if parsed["action"] == "click" and parsed["target"] == "login":
# #         return """
# # page.fill("#username", "admin")
# # page.fill("#password", "1234")
# # page.click("#loginBtn")
# # """
# #     return None

# def generate_playwright_code(parsed):
#     if parsed["action"] == "click":
#         return '''
# page.fill("#username", "admin")
# page.fill("#password", "1234")
# page.click("#loginBtn")
# '''
#     return None

def generate_playwright_code(parsed):
    if parsed["action"]=="click":
        return '''
page.fill("#username","admin")
page.fill("#password","1234")
page.click("#loginBtn")
'''
    return None
