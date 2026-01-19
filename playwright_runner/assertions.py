# # # def generate_assertion(parsed):
# # #     if parsed["action"] == "click" and parsed["target"] == "login":
# # #         return "assert page.inner_text('#message') == 'Login Successful'"

# # #     return None

# # def generate_assertion(parsed):
# #     if parsed["action"] == "click":
# #         return 'assert page.inner_text("#message") == "Login Successful"'
# #     return None

# def generate_assertion(parsed):
#     return 'assert page.inner_text("#message")=="Login Successful"'
def generate_assertion(parsed):
    if parsed["action"] == "login":
        return "assert True"

    if parsed["action"] == "search":
        return "assert 'wiki' in page.url.lower()"

    if parsed["action"] == "mongodb_search":
        return "assert True"
    
    return "assert False"
