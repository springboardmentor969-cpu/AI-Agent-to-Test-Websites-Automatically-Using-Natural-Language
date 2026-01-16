import re

class InstructionParser:

    def detect_selector(self, text):
        # Specific patterns
        if "email" in text:
            return "input[type='email']"
        if "password" in text:
            return "input[type='password']"
        if "search" in text:
            return "input[placeholder*='Search'], input[name='q'], input[type='search']"
        
        # Handle "click [something] button"
        if "button" in text:
            subject = text.replace("click", "").replace("button", "").strip()
            if subject:
                return f"button:has-text('{subject}'), input[type='button'][value*='{subject}'], .btn:has-text('{subject}')"
            return "button"
            
        selector = text.strip()
        # Block non-interactive tags if they appear alone
        if selector.lower() in ["script", "style", "head", "meta", "link", "html", "body"]:
            return "button, input, a" # Reset to generic interactives
            
        return selector

    def parse(self, instruction: str):
        # Split by both 'then' and periods to allow natural sentencing
        steps = re.split(r' then |\. ', instruction.lower())
        actions = []

        for step in steps:
            step = step.strip()
            if not step: continue

            # --- NAVIGATION ---
            if any(k in step for k in ["navigate", "open", "go to"]):
                url = re.findall(r'(https?://\S+)', step)
                if url:
                    actions.append({"action": "goto", "value": url[0]})
                continue

            # --- CLICK ---
            if "click" in step:
                selector = self.detect_selector(step)
                actions.append({"action": "click", "value": selector})
                continue

            # --- TYPE / ENTER ---
            if any(k in step for k in ["type", "enter", "fill"]):
                # Extract quoted text or text after 'typed' keywords
                text_match = re.findall(r'"(.*?)"', step)
                typed_value = text_match[0] if text_match else ""
                
                # If no quotes, try to find text after "as" or "enter"
                if not typed_value:
                    as_match = re.findall(r'(?:type|enter|fill)\s+(\S+)\s+(?:in|into|as)', step)
                    if as_match:
                        typed_value = as_match[0]

                selector = self.detect_selector(step)
                actions.append({
                    "action": "type",
                    "field": selector,
                    "value": typed_value
                })
                continue

            # --- VERIFY TEXT ---
            if any(k in step for k in ["verify", "assert", "check"]):
                target = step.replace("verify", "").replace("assert", "").replace("check", "").strip()
                # Clean up "that" or "if"
                target = re.sub(r'^(that|if|contains|is)\s+', '', target)
                actions.append({"action": "assert_text", "value": target})
                continue

        return actions
