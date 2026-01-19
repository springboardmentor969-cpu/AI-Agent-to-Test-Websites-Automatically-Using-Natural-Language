def generate_assertions(expected_result):
    """
    Generates adaptive Playwright-compatible assertions
    """
    assertions = []

    # ------------------------------
    # LOGIN SUCCESS (Local HTML)
    # ------------------------------
    if expected_result == "login_success":
        assertions.append({
            "type": "element_visible",
            "selectors": [
                "#success",
                ".success",
                "text=Login Successful"
            ]
        })

    # ------------------------------
    # FORM SUBMISSION (Generic)
    # ------------------------------
    if expected_result == "form_submitted":
        assertions.append({
            "type": "element_visible",
            "selectors": [
                "#message",
                ".alert-success",
                "text=Submitted"
            ]
        })

    # ------------------------------
    # URL CHANGE (Real Websites)
    # ------------------------------
    if expected_result == "url_change":
        assertions.append({
            "type": "url_contains",
            "value": "dashboard"
        })

    return assertions
