# agent/parser.py

import re

class InstructionParser:
    """
    Simple and Robust Natural Language Parser for Web Testing
    """

    def extract_quoted_text(self, text):
        """Extract text from quotes"""
        # Double quotes
        match = re.findall(r'"([^"]+)"', text)
        if match:
            return match[0]
        # Single quotes
        match = re.findall(r"'([^']+)'", text)
        if match:
            return match[0]
        return ""

    def extract_url(self, text):
        """Extract URL from text"""
        url_match = re.findall(r'(https?://[^\s]+)', text)
        if url_match:
            return url_match[0].rstrip('.,;')
        return ""

    def parse(self, instruction: str):
        """Parse natural language instruction into actions"""
        
        print(f"\n{'='*60}")
        print(f"[PARSER] Input: {instruction}")
        print(f"{'='*60}")
        
        # Split by common separators
        # Replace newlines and "then" with a delimiter
        text = instruction.lower()
        text = text.replace('\n', ' ||| ')
        text = text.replace(' then ', ' ||| ')
        text = text.replace(' and then ', ' ||| ')
        text = text.replace('. ', ' ||| ')
        
        steps = [s.strip() for s in text.split('|||') if s.strip()]
        
        print(f"[PARSER] Split into {len(steps)} steps:")
        for i, s in enumerate(steps):
            print(f"  Step {i+1}: '{s}'")
        
        actions = []

        for step in steps:
            step = step.strip()
            if len(step) < 3:
                continue
            
            action = None
            
            # 1. GOTO / NAVIGATE
            if any(word in step for word in ['go to', 'goto', 'navigate', 'open ', 'visit', 'launch']):
                url = self.extract_url(step)
                # Also try to extract from original instruction in case URL has capitals
                if not url:
                    url = self.extract_url(instruction)
                if url:
                    action = {"action": "goto", "value": url}
                    print(f"[PARSER] -> GOTO: {url}")
            
            # 2. SEARCH - Check this BEFORE other actions
            elif any(word in step for word in ['search for', 'search ', 'find ', 'look for', 'looking for']) and 'direction' not in step:
                search_text = self.extract_quoted_text(step)
                if not search_text:
                    # Try original instruction for quoted text
                    search_text = self.extract_quoted_text(instruction)
                if not search_text:
                    # Extract text after "search for" or "search"
                    match = re.search(r'(?:search for|search|find|look for)\s+([^\|]+)', step)
                    if match:
                        search_text = match.group(1).strip()
                        # Clean up common trailing words
                        search_text = re.sub(r'\s+(then|and|in|on).*$', '', search_text)
                        search_text = search_text.strip("'\"")
                
                if search_text:
                    action = {"action": "search", "value": search_text}
                    print(f"[PARSER] -> SEARCH: '{search_text}'")
            
            # 2.5 GET DIRECTIONS (Google Maps)
            elif any(word in step for word in ['direction', 'directions', 'route', 'navigate', 'how to get', 'way to']):
                # Extract destination
                destination = self.extract_quoted_text(step)
                if not destination:
                    # Try to extract place name after "to" or "for"
                    match = re.search(r'(?:to|for|directions?)\s+([^\|]+?)(?:\s+from|\s+then|$)', step)
                    if match:
                        destination = match.group(1).strip()
                        destination = destination.strip("'\"")
                        # Remove common words
                        destination = re.sub(r'^(the|a|an)\s+', '', destination)
                
                if destination:
                    action = {"action": "get_directions", "destination": destination}
                    print(f"[PARSER] -> GET_DIRECTIONS: '{destination}'")
            
            # 3. SELECT PRODUCT
            elif any(word in step for word in ['select', 'choose', 'pick', 'click on']) and \
                 any(word in step for word in ['product', 'item', 'result', 'first', 'second', 'third', '1st', '2nd', '3rd']):
                position = 1
                if 'second' in step or '2nd' in step:
                    position = 2
                elif 'third' in step or '3rd' in step:
                    position = 3
                elif 'fourth' in step or '4th' in step:
                    position = 4
                
                action = {"action": "select_product", "position": position}
                print(f"[PARSER] -> SELECT_PRODUCT: position {position}")
            
            # 4. ADD TO CART
            elif ('add' in step or 'put' in step) and ('cart' in step or 'basket' in step or 'bag' in step):
                action = {"action": "add_to_cart"}
                print(f"[PARSER] -> ADD_TO_CART")
            
            # 5. VIEW DETAILS
            elif any(word in step for word in ['view', 'see', 'show']) and \
                 any(word in step for word in ['detail', 'info', 'spec']):
                action = {"action": "view_details"}
                print(f"[PARSER] -> VIEW_DETAILS")
            
            # 6. LOGIN - Must check BEFORE click to prevent duplicate actions
            elif any(word in step for word in ['login', 'log in', 'signin', 'sign in']):
                quoted = re.findall(r'["\']([^"\']+)["\']', step)
                if len(quoted) >= 2:
                    action = {"action": "login", "email": quoted[0], "password": quoted[1]}
                    print(f"[PARSER] -> LOGIN: {quoted[0]}")
                elif len(quoted) == 1:
                    action = {"action": "login", "email": quoted[0], "password": ""}
                    print(f"[PARSER] -> LOGIN (no password): {quoted[0]}")
                else:
                    # No credentials - just click login button
                    action = {"action": "click", "value": "button[type='submit'], button:has-text('Log in')"}
                    print(f"[PARSER] -> CLICK: login button")
            
            # 7. LOGOUT
            elif any(word in step for word in ['logout', 'log out', 'signout', 'sign out']):
                action = {"action": "logout"}
                print(f"[PARSER] -> LOGOUT")
            
            # 8. TYPE/FILL
            elif any(word in step for word in ['type', 'enter', 'fill', 'input', 'write']):
                typed_value = self.extract_quoted_text(step)
                if typed_value:
                    # Determine field
                    if 'email' in step or 'username' in step or 'user' in step:
                        field = "input[type='email'], input[name*='email'], input[name*='user'], input[id*='email']"
                    elif 'password' in step:
                        field = "input[type='password']"
                    elif 'search' in step:
                        action = {"action": "search", "value": typed_value}
                        print(f"[PARSER] -> SEARCH (from type): '{typed_value}'")
                        if action:
                            actions.append(action)
                        continue
                    else:
                        field = "input:visible, textarea:visible"
                    
                    action = {"action": "type", "field": field, "value": typed_value, "press_enter": False}
                    print(f"[PARSER] -> TYPE: '{typed_value}'")
            
            # 9. CLICK - But not if it's a login (already handled above)
            elif any(word in step for word in ['click', 'press', 'tap', 'hit']) and not any(word in step for word in ['login', 'log in', 'signin', 'sign in']):
                # Determine what to click
                if 'submit' in step:
                    selector = "button[type='submit'], input[type='submit']"
                elif 'button' in step:
                    selector = "button, input[type='button']"
                else:
                    selector = "button, a, input[type='submit']"
                
                action = {"action": "click", "value": selector}
                print(f"[PARSER] -> CLICK: {selector[:50]}")
            
            # 10. WAIT
            elif 'wait' in step:
                time_match = re.findall(r'(\d+)', step)
                wait_ms = int(time_match[0]) * 1000 if time_match else 3000
                action = {"action": "wait", "value": wait_ms}
                print(f"[PARSER] -> WAIT: {wait_ms}ms")
            
            # 11. SCROLL
            elif 'scroll' in step:
                direction = "up" if "up" in step else "down"
                action = {"action": "scroll", "direction": direction}
                print(f"[PARSER] -> SCROLL: {direction}")
            
            # 12. SCREENSHOT
            elif any(word in step for word in ['screenshot', 'capture', 'snap']):
                action = {"action": "screenshot"}
                print(f"[PARSER] -> SCREENSHOT")
            
            # 13. VERIFY/ASSERT
            elif any(word in step for word in ['verify', 'assert', 'check', 'confirm', 'should']):
                text_to_verify = self.extract_quoted_text(step)
                if text_to_verify:
                    action = {"action": "assert_text", "value": text_to_verify}
                    print(f"[PARSER] -> ASSERT: '{text_to_verify}'")
            
            else:
                print(f"[PARSER] -> UNRECOGNIZED: '{step}'")
            
            if action:
                actions.append(action)
        
        print(f"\n[PARSER] Final actions ({len(actions)}):")
        for i, a in enumerate(actions):
            print(f"  {i+1}. {a}")
        print(f"{'='*60}\n")
        
        return actions