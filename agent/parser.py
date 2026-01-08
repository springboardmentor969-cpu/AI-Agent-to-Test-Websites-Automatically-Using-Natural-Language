"""
Instruction Parser Module
Milestone 1: Basic keyword-based parsing
Milestone 2: Will be enhanced with LLM-powered natural language understanding

This module handles parsing of natural language test instructions into
structured actions that can be executed by browser automation tools.
"""

import re
from typing import List, Dict


def parse_instruction(instruction: str) -> List[Dict]:
    """
    Parses a natural language test instruction into structured actions.
    
    For Milestone 1, this uses simple keyword matching to identify actions.
    This is a placeholder that will be significantly enhanced in Milestone 2
    with proper NLP using Claude API.
    
    Args:
        instruction: Natural language test instruction (e.g., "Click the login button")
    
    Returns:
        List of parsed actions, each containing:
        - action: Type of action (click, type, navigate, verify, wait)
        - target: Element or field to interact with (if detected)
        - value: Value to input (for type actions)
        - raw_instruction: Original instruction text
        - confidence: Confidence score (0.0 to 1.0)
    
    Examples:
        >>> parse_instruction("Click the submit button")
        [{'action': 'click', 'target': 'submit button', 'value': None, 
          'raw_instruction': '...', 'confidence': 0.8}]
        
        >>> parse_instruction("Type admin into username field")
        [{'action': 'type', 'target': 'username field', 'value': 'admin',
          'raw_instruction': '...', 'confidence': 0.8}]
    """
    
    instruction_lower = instruction.lower()
    parsed_actions = []
    
    # Action keywords mapping
    # Each action type has keywords that trigger it and a base confidence score
    action_keywords = {
        'click': {
            'keywords': ['click', 'press', 'tap', 'hit', 'select'],
            'confidence': 0.8
        },
        'type': {
            'keywords': ['type', 'enter', 'input', 'fill', 'write'],
            'confidence': 0.8
        },
        'navigate': {
            'keywords': ['go to', 'visit', 'open', 'navigate', 'load'],
            'confidence': 0.7
        },
        'verify': {
            'keywords': ['verify', 'check', 'assert', 'validate', 'ensure', 'confirm'],
            'confidence': 0.7
        },
        'wait': {
            'keywords': ['wait', 'pause', 'delay', 'sleep'],
            'confidence': 0.9
        }
    }
    
    # Try to detect actions from keywords
    detected_actions = set()
    
    for action_type, config in action_keywords.items():
        for keyword in config['keywords']:
            if keyword in instruction_lower:
                # Avoid duplicate detection of same action type
                if action_type not in detected_actions:
                    action_data = {
                        'action': action_type,
                        'target': extract_target(instruction, keyword),
                        'value': extract_value(instruction, action_type),
                        'raw_instruction': instruction,
                        'confidence': config['confidence']
                    }
                    parsed_actions.append(action_data)
                    detected_actions.add(action_type)
                    break
    
    # If no actions detected, create a generic "unknown" action
    # This helps us understand what users are asking for
    if not parsed_actions:
        parsed_actions.append({
            'action': 'unknown',
            'target': None,
            'value': None,
            'raw_instruction': instruction,
            'confidence': 0.3,
            'note': 'No recognizable action keywords found - will be enhanced in Milestone 2'
        })
    
    return parsed_actions


def extract_target(instruction: str, keyword: str) -> str:
    """
    Attempts to extract the target element from the instruction.
    
    The target is the element that the action will interact with,
    such as "submit button" in "click the submit button".
    
    Args:
        instruction: Full instruction text
        keyword: The action keyword that was matched
    
    Returns:
        Extracted target string, or None if no target found
    
    Examples:
        >>> extract_target("click the submit button", "click")
        "submit button"
        
        >>> extract_target("fill username field", "fill")
        "username field"
    """
    instruction_lower = instruction.lower()
    
    try:
        # Find the keyword position
        keyword_pos = instruction_lower.index(keyword)
        
        # Get text after the keyword
        after_keyword = instruction[keyword_pos + len(keyword):].strip()
        
        # Remove common articles like "the", "a", "an"
        after_keyword = re.sub(r'^(the|a|an)\s+', '', after_keyword, flags=re.IGNORECASE)
        
        # Take the next few words (up to 5 words or until punctuation)
        words = after_keyword.split()[:5]
        target = ' '.join(words)
        
        # Remove trailing punctuation
        target = re.sub(r'[,.\?!]+$', '', target)
        
        return target if target else None
        
    except (ValueError, IndexError):
        return None


def extract_value(instruction: str, action_type: str) -> str:
    """
    Attempts to extract the value to be entered (for 'type' actions).
    
    For type/input actions, this tries to find what text should be entered,
    such as "admin" in "type admin into username field".
    
    Args:
        instruction: Full instruction text
        action_type: Type of action (only 'type' actions have values)
    
    Returns:
        Extracted value string, or None if no value found or not a type action
    
    Examples:
        >>> extract_value('type "admin" into username', 'type')
        "admin"
        
        >>> extract_value('enter password123 in password field', 'type')
        "password123"
        
        >>> extract_value('click the button', 'click')
        None
    """
    # Only type/input actions have values
    if action_type != 'type':
        return None
    
    # Look for quoted strings (most reliable)
    quoted_match = re.search(r'["\']([^"\']+)["\']', instruction)
    if quoted_match:
        return quoted_match.group(1)
    
    # Look for "with X" or "as X" patterns
    # Example: "fill username with john" or "type admin as password"
    with_pattern = re.search(r'(?:with|as)\s+(\S+)', instruction, re.IGNORECASE)
    if with_pattern:
        return with_pattern.group(1)
    
    return None


def parse_complex_instruction(instruction: str) -> List[Dict]:
    """
    Parses complex multi-step instructions.
    
    This function handles instructions that contain multiple actions,
    such as "Fill username with 'john', fill email with 'john@test.com', and click submit"
    
    For Milestone 1, this just splits on common separators.
    In Milestone 2, this will use Claude to understand complex instructions better.
    
    Args:
        instruction: Multi-step instruction string
    
    Returns:
        List of parsed actions from all steps
    
    Example:
        >>> parse_complex_instruction("Fill name with John, fill email with john@test.com, then click submit")
        [
            {'action': 'type', 'target': 'name', 'value': 'John', ...},
            {'action': 'type', 'target': 'email', 'value': 'john@test.com', ...},
            {'action': 'click', 'target': 'submit', ...}
        ]
    """
    # Split on common separators
    separators = [', and ', ' and then ', ', then ', ' then ', ',']
    
    parts = [instruction]
    for sep in separators:
        new_parts = []
        for part in parts:
            new_parts.extend(part.split(sep))
        parts = new_parts
    
    # Parse each part separately
    all_actions = []
    for part in parts:
        part = part.strip()
        if part:
            actions = parse_instruction(part)
            all_actions.extend(actions)
    
    return all_actions


def format_parsed_actions(actions: List[Dict]) -> str:
    """
    Formats parsed actions into a readable string for debugging/display.
    
    Args:
        actions: List of parsed action dictionaries
    
    Returns:
        Formatted string representation of actions
    
    Example:
        >>> actions = [{'action': 'click', 'target': 'button', 'confidence': 0.8}]
        >>> print(format_parsed_actions(actions))
        1. Action: click | Target: button | Confidence: 80.0%
    """
    if not actions:
        return "No actions parsed"
    
    output = []
    for idx, action in enumerate(actions, 1):
        line = f"{idx}. Action: {action['action']}"
        
        if action.get('target'):
            line += f" | Target: {action['target']}"
        
        if action.get('value'):
            line += f" | Value: {action['value']}"
        
        line += f" | Confidence: {action['confidence']:.1%}"
        output.append(line)
    
    return '\n'.join(output)