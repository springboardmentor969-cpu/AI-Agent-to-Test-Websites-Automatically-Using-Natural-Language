def generate_code(state):
    return {"code": [step["action"] for step in state["steps"]]}
