# # def generate_assertion(parsed):
# #     if parsed["action"] == "click" and parsed["target"] == "login":
# #         return "assert page.inner_text('#message') == 'Login Successful'"

# #     return None

# def generate_assertion(parsed):
#     if parsed["action"] == "click":
#         return 'assert page.inner_text("#message") == "Login Successful"'
#     return None

def generate_assertion(parsed):
    return 'assert page.inner_text("#message")=="Login Successful"'
