
def validate(cmd: str, result: str):
    if cmd == "login":
        return "Successful" in result
    if cmd == "search":
        return "Results" in result
    return False