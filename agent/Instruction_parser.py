from groq import Groq
from typing import Dict
import json
import re

class Instruction_Parser:
    """
    Parses natural language test instructions using Groq AI
    """
    
    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile"):
        self.client = Groq(api_key=api_key)
        self.model = model
    
    def parse(self, natural_language_input: str) -> Dict:
        """Parse natural language test case into structured steps"""
        
        prompt = """You are an expert test automation engineer. Parse the given natural language test case into structured test steps.

Extract the following information:
1. Test name/description
2. URL to test (if mentioned)
3. Individual test steps with:
   - action type (navigate, click, type, select, verify, wait, scroll, hover)
   - target element (selector description)
   - value (if applicable)
   - expected result (for assertions)

Return ONLY valid JSON in this exact format:
{
    "test_name": "descriptive test name",
    "url": "URL or null",
    "steps": [
        {
            "step_number": 1,
            "action": "navigate|click|type|select|verify|wait|scroll|hover",
            "target": "element description (e.g., 'login button', 'email input field')",
            "value": "value to input or null",
            "expected": "expected result or null",
            "description": "human readable step description"
        }
    ]
}

Be specific about element descriptions. For example:
- "button with text 'Submit'"
- "input field with placeholder 'Email'"
- "link containing 'Sign Up'"
"""

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": natural_language_input}
                ],
                temperature=0,
                max_tokens=2000
            )
            
            content = completion.choices[0].message.content
            
            # Extract JSON from response
            json_match = re.search(r'\{[\s\S]*\}', content)
            if json_match:
                parsed_data = json.loads(json_match.group())
            else:
                parsed_data = json.loads(content)
            
            return self._validate_and_enrich(parsed_data, natural_language_input)
            
        except Exception as e:
            raise ValueError(f"Failed to parse with Groq: {str(e)}")
    
    def _validate_and_enrich(self, parsed_data: Dict, original_input: str) -> Dict:
        """Validate and enrich parsed data"""
        if 'steps' not in parsed_data or not parsed_data['steps']:
            raise ValueError("No test steps were parsed from the input")
        
        parsed_data['original_input'] = original_input
        parsed_data['step_count'] = len(parsed_data['steps'])
        
        for i, step in enumerate(parsed_data['steps'], 1):
            if 'action' not in step:
                raise ValueError(f"Step {i} is missing required 'action' field")
            step['step_number'] = i
            step['action'] = step['action'].lower()
        
        return parsed_data
    
    def get_test_summary(self, parsed_data: Dict) -> str:
        """Generate a human-readable summary of parsed test"""
        summary = f"Test: {parsed_data.get('test_name', 'Unnamed Test')}\n"
        if parsed_data.get('url'):
            summary += f"URL: {parsed_data['url']}\n"
        summary += f"Steps: {parsed_data['step_count']}\n\n"
        
        for step in parsed_data['steps']:
            summary += f"{step['step_number']}. {step['description']}\n"
        
        return summary