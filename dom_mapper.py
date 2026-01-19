"""
Advanced Error Handling and Adaptive DOM Mapping Module for Milestone 4
Handles dynamic DOM changes and provides intelligent element selection.
"""

import re
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass


@dataclass
class ElementSelector:
    """Represents a DOM element selector with multiple strategies."""
    primary: str  # Primary selector
    alternatives: List[str]  # Alternative selectors
    description: str
    element_type: str  # input, button, link, etc.


class AdaptiveDOMMapper:
    """Handles adaptive DOM mapping and element selection."""
    
    def __init__(self):
        self.selector_strategies = {
            "id": lambda value: f"#{value}",
            "name": lambda value: f"[name='{value}']",
            "class": lambda value: f".{value}",
            "text": lambda value: f"text={value}",
            "placeholder": lambda value: f"[placeholder='{value}']",
            "type": lambda value: f"[type='{value}']",
            "label": lambda value: f"label:has-text('{value}')"
        }
    
    def generate_selectors(self, description: str, element_type: str = "element") -> ElementSelector:
        """
        Generate multiple selector strategies for an element.
        
        Args:
            description: Element description
            element_type: Type of element (input, button, etc.)
            
        Returns:
            ElementSelector with primary and alternative selectors
        """
        description_lower = description.lower()
        
        # Extract potential identifiers
        selectors = []
        
        # Try to find ID
        id_match = re.search(r'\bid[:\s]+([\w-]+)', description_lower)
        if id_match:
            selectors.append(f"#{id_match.group(1)}")
        
        # Try to find name attribute
        name_match = re.search(r'\bname[:\s]+([\w-]+)', description_lower)
        if name_match:
            selectors.append(f"[name='{name_match.group(1)}']")
        
        # Try to find class
        class_match = re.search(r'\bclass[:\s]+([\w-]+)', description_lower)
        if class_match:
            selectors.append(f".{class_match.group(1)}")
        
        # Try to find text content
        text_match = re.search(r'["\']([^"\']+)["\']', description)
        if text_match:
            text = text_match.group(1)
            selectors.append(f"text={text}")
            selectors.append(f"button:has-text('{text}')")
            selectors.append(f"a:has-text('{text}')")
        
        # Generate type-based selectors
        if element_type == "input":
            if "username" in description_lower or "user" in description_lower:
                selectors.extend([
                    "input[name='username']",
                    "input[type='text']",
                    "input[placeholder*='user' i]",
                    "input[placeholder*='name' i]"
                ])
            elif "password" in description_lower or "pass" in description_lower:
                selectors.extend([
                    "input[name='password']",
                    "input[type='password']",
                    "input[placeholder*='password' i]"
                ])
            elif "email" in description_lower:
                selectors.extend([
                    "input[name='email']",
                    "input[type='email']",
                    "input[placeholder*='email' i]"
                ])
        
        elif element_type == "button":
            if "submit" in description_lower or "login" in description_lower:
                selectors.extend([
                    "button[type='submit']",
                    "button:has-text('Login')",
                    "button:has-text('Submit')",
                    "input[type='submit']"
                ])
            elif "search" in description_lower:
                selectors.extend([
                    "button:has-text('Search')",
                    "#test-search-button",
                    "button[type='button']"
                ])
        
        elif element_type == "link":
            if "login" in description_lower:
                selectors.extend([
                    "a[href*='login']",
                    "a:has-text('Login')"
                ])
            elif "signup" in description_lower or "register" in description_lower:
                selectors.extend([
                    "a[href*='signup']",
                    "a:has-text('Sign Up')",
                    "a:has-text('Register')"
                ])
        
        # Remove duplicates while preserving order
        seen = set()
        unique_selectors = []
        for sel in selectors:
            if sel not in seen:
                seen.add(sel)
                unique_selectors.append(sel)
        
        # Set primary selector (first one) and alternatives
        primary = unique_selectors[0] if unique_selectors else "body"
        alternatives = unique_selectors[1:] if len(unique_selectors) > 1 else []
        
        return ElementSelector(
            primary=primary,
            alternatives=alternatives,
            description=description,
            element_type=element_type
        )
    
    def adapt_selector(self, original_selector: str, context: Dict[str, Any]) -> List[str]:
        """
        Adapt selector based on context and DOM changes.
        
        Args:
            original_selector: Original CSS selector
            context: Context information (page structure, etc.)
            
        Returns:
            List of adapted selectors to try
        """
        adapted = [original_selector]
        
        # If selector contains ID, try variations
        if "#" in original_selector:
            id_value = original_selector.split("#")[1].split()[0]
            adapted.extend([
                f"[id='{id_value}']",
                f"[data-id='{id_value}']",
                f".{id_value}"  # Sometimes IDs are used as classes
            ])
        
        # If selector contains class, try variations
        if "." in original_selector:
            class_value = original_selector.split(".")[1].split()[0]
            adapted.extend([
                f"[class*='{class_value}']",
                f"[data-class='{class_value}']"
            ])
        
        # Try attribute variations
        if "[" in original_selector:
            # Extract attribute name and value
            attr_match = re.search(r"\[([^=]+)=['\"]([^'\"]+)['\"]\]", original_selector)
            if attr_match:
                attr_name = attr_match.group(1)
                attr_value = attr_match.group(2)
                adapted.extend([
                    f"[{attr_name}*='{attr_value}']",  # Partial match
                    f"[{attr_name}^='{attr_value}']",  # Starts with
                    f"[data-{attr_name}='{attr_value}']"  # Data attribute
                ])
        
        return adapted


class AdvancedErrorHandler:
    """Handles advanced error scenarios and provides recovery strategies."""
    
    def __init__(self):
        self.error_patterns = {
            "element_not_found": [
                r"element.*not found",
                r"selector.*not found",
                r"timeout.*waiting for",
                r"element.*not visible"
            ],
            "network_error": [
                r"network.*error",
                r"connection.*refused",
                r"timeout.*network",
                r"failed to fetch"
            ],
            "assertion_failed": [
                r"assertion.*failed",
                r"expected.*but got",
                r"assert.*error"
            ],
            "browser_error": [
                r"browser.*not found",
                r"executable.*doesn't exist",
                r"chromium.*not installed"
            ]
        }
    
    def classify_error(self, error_message: str) -> Tuple[str, str]:
        """
        Classify error type and provide recovery suggestion.
        
        Args:
            error_message: Error message text
            
        Returns:
            Tuple of (error_type, recovery_suggestion)
        """
        error_lower = error_message.lower()
        
        for error_type, patterns in self.error_patterns.items():
            for pattern in patterns:
                if re.search(pattern, error_lower):
                    return (error_type, self._get_recovery_suggestion(error_type))
        
        return ("unknown", "Review the error message and check the test configuration.")
    
    def _get_recovery_suggestion(self, error_type: str) -> str:
        """Get recovery suggestion for error type."""
        suggestions = {
            "element_not_found": (
                "Element not found. Try:\n"
                "1. Check if the page has loaded completely\n"
                "2. Verify the selector is correct\n"
                "3. Add a wait for the element before interaction"
            ),
            "network_error": (
                "Network error detected. Try:\n"
                "1. Check if the server is running\n"
                "2. Verify the URL is correct\n"
                "3. Check network connectivity"
            ),
            "assertion_failed": (
                "Assertion failed. Try:\n"
                "1. Verify the expected value is correct\n"
                "2. Check if the element contains the expected content\n"
                "3. Add debugging to see actual vs expected values"
            ),
            "browser_error": (
                "Browser not found. Run:\n"
                "python -m playwright install chromium"
            )
        }
        return suggestions.get(error_type, "Review the error and adjust the test accordingly.")
    
    def enhance_error_message(self, error: str, context: Dict[str, Any]) -> str:
        """
        Enhance error message with context and suggestions.
        
        Args:
            error: Original error message
            context: Context information
            
        Returns:
            Enhanced error message
        """
        error_type, suggestion = self.classify_error(error)
        
        enhanced = f"""
Error Type: {error_type.replace('_', ' ').title()}

Original Error:
{error}

Recovery Suggestion:
{suggestion}
"""
        
        if context.get("selector"):
            enhanced += f"\nSelector Used: {context['selector']}\n"
        
        if context.get("page_url"):
            enhanced += f"Page URL: {context['page_url']}\n"
        
        return enhanced



