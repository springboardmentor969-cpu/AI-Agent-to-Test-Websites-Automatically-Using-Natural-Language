history = []

def add_history(report):
    history.insert(0, {
        "input": report["input"],
        "status": report["status"]
    })
    if len(history) > 10:
        history.pop()

def get_history():
    return history
