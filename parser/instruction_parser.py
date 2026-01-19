# # # def parse_instruction(text: str):
# # #     text = text.lower()

# # #     if "click" in text:
# # #         if "login" in text:
# # #             return {"action": "click", "target": "login"}
# # #         if "submit" in text:
# # #             return {"action": "click", "target": "submit"}

# # #     return {"action": "unknown", "target": None}

# # def parse_instruction(text):
# #     text = text.lower()
# #     if "click" in text and "login" in text:
# #         return {"action": "click", "target": "login"}
# #     return {"action": "unknown", "target": None}


# def parse_instruction(text):
#     if "login" in text.lower():
#         return {"action":"click","target":"login"}
#     return {"action":"unknown","target":None}
# def parse_instruction(text):
#     text = text.lower().strip()

#     if text == "click login":
#         return {"action": "login"}

#     if text.startswith("search for"):
#         query = text.replace("search for", "").strip()
#         if query:
#             return {"action": "search", "query": query}

#     return {"action": "invalid"}
import re

def parse_instruction(text):
    text = text.lower().strip()

    # ---------------- LOGIN WITH USERNAME & PASSWORD ----------------
    # Example:
    # "login with username as anu and password as anu"
    login_pattern = r"login with username as (\w+) and password as (\w+)"

    match = re.search(login_pattern, text)
    if match:
        username = match.group(1)
        password = match.group(2)

        return {
            "action": "login",
            "username": username,
            "password": password
        }

    # ---------------- SIMPLE LOGIN (fallback) ----------------
    

    # ---------------- SEARCH COMMAND ----------------
    if text.startswith("search for"):
        query = text.replace("search for", "").strip()
        return {
            "action": "search",
            "query": query
        }

    # ---------------- MONGODB MOCK SEARCH ----------------
    if "mongodb" in text and "search for" in text:
        keyword = text.split("search for")[-1].strip()
        return {
            "action": "mongodb_search",
            "keyword": keyword
        }

    # ---------------- INVALID ----------------
    return {"action": "invalid"}
