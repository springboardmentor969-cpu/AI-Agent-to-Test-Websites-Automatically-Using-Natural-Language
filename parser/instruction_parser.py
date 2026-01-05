# # def parse_instruction(text: str):
# #     text = text.lower()

# #     if "click" in text:
# #         if "login" in text:
# #             return {"action": "click", "target": "login"}
# #         if "submit" in text:
# #             return {"action": "click", "target": "submit"}

# #     return {"action": "unknown", "target": None}

# def parse_instruction(text):
#     text = text.lower()
#     if "click" in text and "login" in text:
#         return {"action": "click", "target": "login"}
#     return {"action": "unknown", "target": None}


def parse_instruction(text):
    if "login" in text.lower():
        return {"action":"click","target":"login"}
    return {"action":"unknown","target":None}
