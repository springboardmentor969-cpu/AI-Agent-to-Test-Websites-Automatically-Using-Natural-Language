import re
from typing import Dict, Pattern, List, Optional


class InstructionParser:
    def __init__(self):
        # Supported instruction patterns
        self.action_patterns: Dict[str, Pattern] = {
            "navigate": re.compile(r"open\s+(the\s+)?(.+)", re.IGNORECASE),
            "search": re.compile(r"search\s+(for\s+)?(.+)", re.IGNORECASE),
            "fill": re.compile(r"enter\s+(.+)\s+in\s+(.+)", re.IGNORECASE),
            "fill_alt": re.compile(r"enter\s+(.+)\s+(.+)", re.IGNORECASE),  # Alternative: enter value field
            "click": re.compile(r"click\s+(.+)", re.IGNORECASE),
            "assert": re.compile(r"(verify|check|assert)\s+(.+)", re.IGNORECASE),
            "wait": re.compile(r"wait\s+(for\s+)?(.+)", re.IGNORECASE),
        }

        # Website mappings
        self.website_map: Dict[str, str] = {
            "youtube": "https://www.youtube.com",
            "google": "https://www.google.com",
            "login page": "http://127.0.0.1:5000/static/login.html",
        }

    def parse(self, instruction: str) -> List[dict]:
        actions: List[dict] = []
        parts = [p.strip() for p in instruction.split(",") if p.strip()]

        for part in parts:
            action = self._identify_action(part)
            if action:
                actions.append(action)

        return actions

    def _identify_action(self, part: str) -> Optional[dict]:
        for action_type, pattern in self.action_patterns.items():
            match = pattern.search(part)
            if not match:
                continue

            # NAVIGATE
            if action_type == "navigate":
                target = match.group(2).lower().strip()
                url = self.website_map.get(target, target)

                # If not a full URL, try to make it a valid URL
                if not url.startswith(('http://', 'https://', 'file://')):
                    # Check if it's a common site name
                    common_sites = {
                        'youtube': 'https://www.youtube.com',
                        'google': 'https://www.google.com',
                        'github': 'https://github.com',
                        'stackoverflow': 'https://stackoverflow.com',
                        'linkedin': 'https://www.linkedin.com',
                        'facebook': 'https://www.facebook.com',
                        'twitter': 'https://www.twitter.com',
                        'instagram': 'https://www.instagram.com'
                    }
                    
                    if target in common_sites:
                        url = common_sites[target]
                    elif '.' in target:
                        # Looks like a domain, add https://
                        url = f'https://{target}'
                    else:
                        # Assume it's a site name, try with .com
                        url = f'https://{target}.com'

                return {"action": "navigate", "url": url}

            # SEARCH
            if action_type == "search":
                search_term = match.group(2).strip()
                return {
                    "action": "press_enter",
                    "field": "q",  # Google search input name
                    "value": search_term
                }

            # FILL
            if action_type == "fill":
                value = match.group(1).strip()
                field = match.group(2).lower()

                if "user" in field:
                    field = "username"
                elif "pass" in field:
                    field = "password"
                elif "search" in field:
                    field = "q"  # Google search input name

                return {
                    "action": "fill",
                    "field": field,
                    "value": value
                }

            # FILL ALT (enter value field)
            if action_type == "fill_alt":
                value = match.group(1).strip()
                field = match.group(2).lower()

                if "user" in field:
                    field = "username"
                elif "pass" in field:
                    field = "password"
                elif "search" in field:
                    field = "q"  # Google search input name

                return {
                    "action": "fill",
                    "field": field,
                    "value": value
                }

            # CLICK
            if action_type == "click":
                element = match.group(1).lower().strip()

                # Special handling for search - press Enter instead of clicking button
                if "search" in element:
                    return {
                        "action": "press_enter",
                        "field": "q"  # Press Enter in the search field
                    }

                return {
                    "action": "click",
                    "element": element
                }

            # ASSERT
            if action_type == "assert":
                return {
                    "action": "assert",
                    "text": match.group(2).strip()
                }

            # WAIT
            if action_type == "wait":
                element = match.group(2).lower().strip()
                return {
                    "action": "wait",
                    "element": element
                }

        return None
