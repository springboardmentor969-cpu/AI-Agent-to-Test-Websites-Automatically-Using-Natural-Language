# agent/enhanced_parser.py

import re
import os
import requests
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

class EnhancedInstructionParser:
    """
    Advanced instruction parser with AI-powered natural language understanding,
    variable support, conditional logic, and comprehensive action types.
    """
    
    def __init__(self):
        self.variables: Dict[str, Any] = {}
        self.grok_api_key = os.getenv("GROK_API_KEY")
        self.grok_url = "https://api.x.ai/v1/chat/completions"
        self.use_ai_parsing = bool(self.grok_api_key)
    
    def parse(self, instruction: str, use_ai: bool = True) -> List[Dict[str, Any]]:
        """
        Parse instruction using AI-powered understanding or fallback to pattern matching
        """
        if use_ai and self.use_ai_parsing:
            try:
                return self._parse_with_ai(instruction)
            except Exception as e:
                print(f"AI parsing failed, falling back to pattern matching: {e}")
                return self._parse_with_patterns(instruction)
        else:
            return self._parse_with_patterns(instruction)
    
    def _parse_with_ai(self, instruction: str) -> List[Dict[str, Any]]:
        """Use Grok AI to parse complex instructions"""
        
        prompt = f"""You are an expert web automation instruction parser. Convert the following natural language instruction into a JSON array of actions.

INSTRUCTION: {instruction}

AVAILABLE ACTIONS:
- goto: Navigate to URL (value: url)
- click: Click element (value: selector)
- type: Type text (field: selector, value: text)
- hover: Hover over element (value: selector)
- select: Select dropdown option (field: selector, value: option_value OR label: option_label)
- scroll: Scroll (direction: "up"/"down"/"to_element", value: selector or pixels)
- wait: Wait for condition (condition: "element"/"text"/"time", value: selector/text/milliseconds)
- extract: Extract data (field: selector, variable: variable_name, attribute: optional)
- assert_text: Verify text exists (value: expected_text)
- assert_element: Verify element exists (value: selector)
- upload: Upload file (field: selector, value: file_path)
- download: Download file (value: trigger_selector)
- switch_tab: Switch to tab (value: tab_id or "new")
- press_key: Press keyboard key (value: key_name, field: optional_selector)
- execute_js: Execute JavaScript (value: js_code)

RULES:
1. Return ONLY a valid JSON array of action objects
2. Each action must have an "action" field
3. Use appropriate selectors (CSS preferred, can use text-based like "button:has-text('Login')")
4. For variables, use {{variable_name}} syntax in values
5. Be specific with selectors
6. No markdown, no explanations, just JSON

EXAMPLE:
Input: "go to google.com then search for playwright"
Output: [{{"action": "goto", "value": "https://google.com"}}, {{"action": "type", "field": "input[name='q']", "value": "playwright"}}, {{"action": "press_key", "value": "Enter"}}]

Now parse this instruction:"""

        try:
            response = requests.post(
                self.grok_url,
                headers={
                    "Authorization": f"Bearer {self.grok_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "grok-beta",
                    "messages": [
                        {"role": "system", "content": "You are a JSON-only instruction parser. Return only valid JSON arrays."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.1
                },
                timeout=10
            )
            
            result = response.json()
            content = result["choices"][0]["message"]["content"].strip()
            
            # Clean up markdown if present
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            # Parse JSON
            import json
            actions = json.loads(content)
            
            # Validate and normalize actions
            return self._normalize_actions(actions)
            
        except Exception as e:
            print(f"AI parsing error: {e}")
            raise
    
    def _parse_with_patterns(self, instruction: str) -> List[Dict[str, Any]]:
        """Fallback pattern-based parsing (enhanced version of original parser)"""
        steps = re.split(r' then |\\. |; ', instruction.lower())
        actions = []

        for step in steps:
            step = step.strip()
            if not step:
                continue

            # --- NAVIGATION ---
            if any(k in step for k in ["navigate", "open", "go to", "visit"]):
                url = re.findall(r'(https?://\\S+)', step)
                if url:
                    actions.append({"action": "goto", "value": url[0]})
                else:
                    # Try to extract domain
                    words = step.split()
                    for word in words:
                        if "." in word and not word.startswith("."):
                            url = word if word.startswith("http") else f"https://{word}"
                            actions.append({"action": "goto", "value": url})
                            break
                continue

            # --- WAIT ---
            if "wait" in step:
                # Wait for time
                time_match = re.findall(r'(\\d+)\\s*(second|sec|ms|millisecond)', step)
                if time_match:
                    value = int(time_match[0][0])
                    unit = time_match[0][1]
                    if unit in ["second", "sec"]:
                        value *= 1000
                    actions.append({"action": "wait", "condition": "time", "value": value})
                    continue
                
                # Wait for element
                if "for" in step:
                    selector = self._extract_selector_from_text(step)
                    actions.append({"action": "wait", "condition": "element", "value": selector})
                    continue

            # --- SCROLL ---
            if "scroll" in step:
                if "down" in step or "bottom" in step:
                    actions.append({"action": "scroll", "direction": "down", "value": 500})
                elif "up" in step or "top" in step:
                    actions.append({"action": "scroll", "direction": "up", "value": 500})
                elif "to" in step:
                    selector = self._extract_selector_from_text(step)
                    actions.append({"action": "scroll", "direction": "to_element", "value": selector})
                continue

            # --- HOVER ---
            if "hover" in step:
                selector = self._extract_selector_from_text(step)
                actions.append({"action": "hover", "value": selector})
                continue

            # --- CLICK ---
            if "click" in step:
                selector = self._extract_selector_from_text(step)
                actions.append({"action": "click", "value": selector})
                continue

            # --- SELECT (dropdown) ---
            if "select" in step:
                # Extract option value
                option_match = re.findall(r'["\']([^"\']+)["\']', step)
                selector = "select"  # Default, should be improved
                
                if option_match:
                    actions.append({
                        "action": "select",
                        "field": selector,
                        "label": option_match[0]
                    })
                continue

            # --- PRESS KEY (must come before TYPE to handle 'press enter') ---
            if "press" in step:
                # Extract key name after 'press'
                key_match = re.findall(r'press\s+(\w+)', step)
                key = key_match[0].capitalize() if key_match else "Enter"
                actions.append({"action": "press_key", "value": key})
                continue

            # --- TYPE / FILL ---
            if any(k in step for k in ["type", "fill", "input", "enter"]) and "press" not in step:
                text_match = re.findall(r'["\']([^"\']+)["\']', step)
                typed_value = text_match[0] if text_match else ""
                
                # Skip if no text to type (might be 'press enter' handled above)
                if not typed_value and "enter" in step:
                    actions.append({"action": "press_key", "value": "Enter"})
                    continue
                
                selector = self._extract_selector_from_text(step)
                actions.append({
                    "action": "type",
                    "field": selector,
                    "value": typed_value
                })
                continue

            # --- EXTRACT DATA ---
            if "extract" in step or "save" in step or "get" in step:
                # Extract variable name
                var_match = re.findall(r'as\\s+\\{([^}]+)\\}', step)
                variable = var_match[0] if var_match else "extracted_value"
                
                selector = self._extract_selector_from_text(step)
                actions.append({
                    "action": "extract",
                    "field": selector,
                    "variable": variable
                })
                continue

            # --- UPLOAD FILE ---
            if "upload" in step:
                file_match = re.findall(r'["\']([^"\']+)["\']', step)
                file_path = file_match[0] if file_match else ""
                
                selector = "input[type='file']"
                actions.append({
                    "action": "upload",
                    "field": selector,
                    "value": file_path
                })
                continue

            # --- PRESS KEY (backup, mostly handled above) ---
            # This is a fallback for any press commands not caught earlier

            # --- VERIFY / ASSERT TEXT ---
            if any(k in step for k in ["verify", "assert", "check", "ensure"]):
                if "element" in step or "exists" in step:
                    selector = self._extract_selector_from_text(step)
                    actions.append({"action": "assert_element", "value": selector})
                else:
                    # Try to extract quoted text first
                    quoted_match = re.findall(r'["\']([^"\']+)["\']', step)
                    if quoted_match:
                        target = quoted_match[0]
                    else:
                        # Clean up the step to extract the expected text
                        target = step
                        # Remove common assertion words and phrases
                        for phrase in ["verify", "assert", "check", "ensure", "that", "appears", "on the page", "on page", "is visible", "is displayed", "exists", "shows", "contains"]:
                            target = target.replace(phrase, " ")
                        target = " ".join(target.split()).strip()  # Clean up whitespace
                    
                    if target:
                        actions.append({"action": "assert_text", "value": target})
                continue

        return actions
    
    def _extract_selector_from_text(self, text: str) -> str:
        """Extract selector from natural language text"""
        # Remove common action words
        text = text.lower()
        for word in ["click", "hover", "type", "scroll", "wait", "on", "the", "to", "into", "in"]:
            text = text.replace(word, "")
        text = text.strip()
        
        # Specific patterns
        if "email" in text:
            return "input[type='email']"
        if "password" in text:
            return "input[type='password']"
        if "search" in text:
            return "input[placeholder*='Search'], input[name='q'], input[type='search']"
        if "button" in text:
            subject = text.replace("button", "").strip()
            if subject:
                return f"button:has-text('{subject}'), input[type='button'][value*='{subject}']"
            return "button"
        if "link" in text:
            subject = text.replace("link", "").strip()
            if subject:
                return f"a:has-text('{subject}')"
            return "a"
        
        # If text has quotes, use it as text selector
        quoted = re.findall(r'["\']([^"\']+)["\']', text)
        if quoted:
            return f"*:has-text('{quoted[0]}')"
        
        # Default to the cleaned text as selector
        return text.strip() or "body"
    
    def _normalize_actions(self, actions: List[Dict]) -> List[Dict]:
        """Normalize and validate actions"""
        normalized = []
        
        for action in actions:
            if not isinstance(action, dict) or "action" not in action:
                continue
            
            # Ensure required fields exist
            action_type = action["action"]
            
            # Add defaults based on action type
            if action_type in ["click", "hover", "assert_element", "scroll"]:
                if "value" not in action:
                    action["value"] = "body"
            
            if action_type in ["type", "select", "upload", "extract"]:
                if "field" not in action:
                    action["field"] = "input"
            
            normalized.append(action)
        
        return normalized
    
    def set_variable(self, name: str, value: Any):
        """Store variable for later use"""
        self.variables[name] = value
    
    def get_variable(self, name: str) -> Any:
        """Retrieve stored variable"""
        return self.variables.get(name)
    
    def replace_variables(self, text: str) -> str:
        """Replace {{variable}} placeholders with actual values"""
        for var_name, var_value in self.variables.items():
            text = text.replace(f"{{{{{var_name}}}}}", str(var_value))
        return text
