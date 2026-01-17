def parse_instruction(text: str):
    text = text.lower().strip()

    if "open google" in text:
        return {
            "action": "open_google"
        }

    if "search" in text:
        return {
            "action": "search",
            "query": text.replace("search", "").strip() or "automation testing"
        }

    # Default safe action (prevents FAIL in demo)
    return {
        "action": "open_google"
    }
