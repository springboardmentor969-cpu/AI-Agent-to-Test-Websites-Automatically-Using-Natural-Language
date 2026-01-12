def parse_instruction(text):
    steps = []
    text = text.lower()

    if "open" in text:
        if "youtube" in text:
            steps.append({
                "action": "open_browser",
                "url": "https://www.youtube.com"
            })
        else:
            steps.append({
                "action": "open_browser",
                "url": "http://127.0.0.1:5000/sample_form.html"
            })

    if "click" in text:
        steps.append({
            "action": "click",
            "selector": "#submit"
        })

    if "submit" in text:
        steps.append({
            "action": "submit",
            "selector": "#submit"
        })

    return steps
