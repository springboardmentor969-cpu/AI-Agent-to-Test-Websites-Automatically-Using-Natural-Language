import json

def parse_steps(step_text):
    try:
        return json.loads(step_text)
    except:
        return []
