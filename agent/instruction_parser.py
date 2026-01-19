def parse_instruction(text: str):
    text = text.lower().strip()

    if "open google" in text:
        return {"action": "open", "url": "https://www.google.com"}

    if text.startswith("search"):
        query = text.replace("search", "").strip()
        return {
            "action": "search",
            "url": "https://www.google.com",
            "query": query if query else "automation testing"
        }

    if "open" in text and "http" in text:
        url = text.replace("open", "").strip()
        return {"action": "open", "url": url}

    return {"action": "open", "url": "https://www.google.com"}
