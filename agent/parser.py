def parse_instruction(text):
    actions = []
    text = text.lower()

    # ---------------------------------
    # OPEN PAGE (Local + Future Support)
    # ---------------------------------
    if "open" in text:
        if "login" in text:
            actions.append({
                "action": "open_url",
                "value": "http://127.0.0.1:5000/static/login.html"
            })
        elif "register" in text:
            actions.append({
                "action": "open_url",
                "value": "http://127.0.0.1:5000/static/register.html"
            })
        else:
            actions.append({
                "action": "open_url",
                "value": "http://127.0.0.1:5000"
            })

    # ---------------------------------
    # USERNAME / EMAIL
    # ---------------------------------
    if "username" in text or "user name" in text:
        actions.append({
            "action": "fill",
            "selector": "#username",
            "text": "admin"
        })

    if "email" in text:
        actions.append({
            "action": "fill",
            "selector": "#email",
            "text": "admin@test.com"
        })

    # ---------------------------------
    # PASSWORD
    # ---------------------------------
    if "password" in text:
        actions.append({
            "action": "fill",
            "selector": "#password",
            "text": "1234"
        })

    # ---------------------------------
    # CLICK / SUBMIT / LOGIN
    # ---------------------------------
    if any(word in text for word in ["click", "submit", "login", "sign in"]):
        actions.append({
            "action": "click",
            "value": "#login-btn"
        })

    return actions
