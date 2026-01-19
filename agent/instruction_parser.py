import re
from urllib.parse import urlparse

def extract_url(text):
    """Extract URLs from text"""
    url_pattern = r'https?://[^\s]+'
    urls = re.findall(url_pattern, text)
    return urls[0] if urls else None

def extract_credentials(text):
    """Extract username and password from text"""
    username = ""
    password = ""
    
    try:
        parts = text.lower().split()
        
        # Extract username
        if "username" in text or "user" in text:
            for i, word in enumerate(parts):
                if word in ["username", "user"]:
                    username = parts[i + 1] if i + 1 < len(parts) else ""
                    break
        
        # Extract password
        if "password" in text or "pass" in text:
            for i, word in enumerate(parts):
                if word in ["password", "pass"]:
                    password = parts[i + 1] if i + 1 < len(parts) else ""
                    break
    except:
        pass
    
    return username, password

def normalize_url(url):
    """Normalize URL to ensure it's valid"""
    url = url.strip()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url

def parse_instruction(text: str):
    text_lower = text.lower().strip()
    
    # Extract any URLs from the text
    url_from_text = extract_url(text)
    username, password = extract_credentials(text)
    
    # Check for login/authentication action
    if any(keyword in text_lower for keyword in ["login", "sign in", "authenticate", "user", "password"]):
        url = url_from_text if url_from_text else "https://www.google.com"
        return {
            "action": "login",
            "url": normalize_url(url),
            "username": username,
            "password": password
        }
    
    # Check for search action
    if any(keyword in text_lower for keyword in ["search", "find", "look for", "query"]):
        query = text_lower.replace("search", "").replace("find", "").replace("look for", "").replace("query", "").strip()
        return {
            "action": "search",
            "url": "https://www.google.com",
            "query": query if query else "automation testing"
        }
    
    # Check for navigation/open action
    if any(keyword in text_lower for keyword in ["open", "go to", "visit", "navigate"]):
        if url_from_text:
            return {"action": "open", "url": normalize_url(url_from_text)}
        elif "google" in text_lower:
            return {"action": "open", "url": "https://www.google.com"}
        elif "github" in text_lower:
            return {"action": "open", "url": "https://github.com"}
        elif "youtube" in text_lower:
            return {"action": "open", "url": "https://www.youtube.com"}
        elif "facebook" in text_lower:
            return {"action": "open", "url": "https://www.facebook.com"}
        else:
            # Try to find any domain-like word
            words = text.split()
            for word in words:
                if "." in word and len(word) > 3:
                    return {"action": "open", "url": normalize_url(word)}
    
    # Check for click action
    if any(keyword in text_lower for keyword in ["click", "tap", "press button"]):
        return {
            "action": "click",
            "selector": "button, a, input[type='submit']"
        }
    
    # Check for fill/type action
    if any(keyword in text_lower for keyword in ["fill", "type", "enter", "input"]):
        value = text_lower.replace("fill", "").replace("type", "").replace("enter", "").replace("input", "").strip()
        return {
            "action": "fill",
            "selector": "input",
            "value": value
        }
    
    # Check for wait/scroll action
    if any(keyword in text_lower for keyword in ["wait", "scroll", "load", "pause"]):
        return {
            "action": "wait",
            "duration": 3
        }
    
    # Default: if URL found, open it; otherwise open Google
    if url_from_text:
        return {"action": "open", "url": normalize_url(url_from_text)}
    
    return {"action": "open", "url": "https://www.google.com"}
