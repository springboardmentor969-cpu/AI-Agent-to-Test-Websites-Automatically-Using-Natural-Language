# agent/ai_selector.py

import os
import requests
from typing import Optional, Tuple
from bs4 import BeautifulSoup

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from .selector_cache import SelectorCache

# Load from environment for safety
GROK_API_KEY = os.getenv("GROK_API_KEY")
GROK_URL = "https://api.x.ai/v1/chat/completions"

class AISelectorHealer:
    """
    Enhanced AI-powered selector healing with caching, better context,
    and multiple healing strategies.
    """
    
    def __init__(self, use_cache: bool = True):
        self.cache = SelectorCache() if use_cache else None
        self.healing_history = []
    
    def heal(self, html_content: str, failed_selector: str, action_hint: str, 
             page_url: str = "", page_title: str = "") -> Optional[str]:
        """
        Use Grok AI to analyze the DOM and suggest the correct selector.
        Now with caching and enhanced context.
        """
        if not GROK_API_KEY:
            print("⚠️ AI Healer Warning: GROK_API_KEY not found in environment. Fallback to original selector.")
            return failed_selector
        
        # Check cache first
        if self.cache:
            cached_selector = self.cache.get(page_url, failed_selector, action_hint)
            if cached_selector:
                print(f"✓ Using cached selector: {cached_selector}")
                return cached_selector
        
        # Try multiple healing strategies
        healed_selector = None
        
        # Strategy 1: AI with enhanced context
        healed_selector = self._heal_with_ai_enhanced(
            html_content, failed_selector, action_hint, page_url, page_title
        )
        
        # Strategy 2: If AI fails, try semantic analysis
        if not healed_selector or healed_selector == failed_selector:
            healed_selector = self._heal_with_semantic_analysis(
                html_content, failed_selector, action_hint
            )
        
        # Cache successful healing
        if healed_selector and healed_selector != failed_selector and self.cache:
            self.cache.set(page_url, failed_selector, action_hint, healed_selector, "AI")
        
        # Track healing history
        self.healing_history.append({
            'failed': failed_selector,
            'healed': healed_selector,
            'action': action_hint,
            'success': healed_selector != failed_selector
        })
        
        return healed_selector or failed_selector
    
    def _heal_with_ai_enhanced(self, html_content: str, failed_selector: str, 
                               action_hint: str, page_url: str, page_title: str) -> Optional[str]:
        """Enhanced AI healing with better context"""
        
        # Extract relevant HTML snippet (focus on interactive elements)
        relevant_html = self._extract_relevant_html(html_content, action_hint)
        
        prompt = f"""You are an expert CSS selector generator for web automation.

CONTEXT:
- Page URL: {page_url or 'Unknown'}
- Page Title: {page_title or 'Unknown'}
- Failed Selector: {failed_selector}
- Intended Action: {action_hint}

HTML SNIPPET (Interactive elements only):
{relevant_html[:8000]}

TASK:
Analyze the HTML and generate the MOST STABLE CSS selector for the element that matches the intended action.

SELECTOR PRIORITY (use in this order):
1. ID attributes (e.g., #submit-button)
2. Unique data attributes (e.g., [data-testid="login"])
3. Unique name attributes (e.g., input[name="email"])
4. Unique class combinations (e.g., .btn.btn-primary.submit)
5. Text-based selectors (e.g., button:has-text("Login"))
6. Structural selectors (e.g., form > button[type="submit"])

RULES:
- Return ONLY the selector, no explanations
- Prefer shorter, more stable selectors
- Avoid nth-child unless necessary
- Use :has-text() for buttons/links when appropriate
- Ensure selector is specific enough to match only one element

SELECTOR:"""

        try:
            response = requests.post(
                GROK_URL,
                headers={
                    "Authorization": f"Bearer {GROK_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "grok-beta",
                    "messages": [
                        {"role": "system", "content": "You are a CSS selector expert. Return only the selector, nothing else."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.1
                },
                timeout=15
            )

            result = response.json()
            selector = result["choices"][0]["message"]["content"].strip()
            
            # Clean up any AI chatter or markdown
            selector = self._clean_selector(selector)
            
            return selector
            
        except Exception as e:
            print(f"AI Healing Error: {e}")
            return None
    
    def _heal_with_semantic_analysis(self, html_content: str, failed_selector: str, 
                                     action_hint: str) -> Optional[str]:
        """Fallback: Use semantic analysis to find elements"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Determine element type from action hint
            if "click" in action_hint.lower():
                # Look for buttons, links
                candidates = soup.find_all(['button', 'a', 'input'])
            elif "type" in action_hint.lower() or "fill" in action_hint.lower():
                # Look for inputs, textareas
                candidates = soup.find_all(['input', 'textarea'])
            elif "select" in action_hint.lower():
                candidates = soup.find_all('select')
            else:
                candidates = soup.find_all(['button', 'a', 'input', 'textarea', 'select'])
            
            # Score candidates based on attributes
            best_candidate = None
            best_score = 0
            
            for element in candidates[:20]:  # Limit to first 20 to avoid slowdown
                score = 0
                
                # Prefer elements with IDs
                if element.get('id'):
                    score += 10
                    selector = f"#{element.get('id')}"
                
                # Check for data attributes
                elif any(attr.startswith('data-') for attr in element.attrs):
                    score += 8
                    data_attr = [attr for attr in element.attrs if attr.startswith('data-')][0]
                    selector = f"[{data_attr}='{element.get(data_attr)}']"
                
                # Check for name attribute
                elif element.get('name'):
                    score += 7
                    selector = f"{element.name}[name='{element.get('name')}']"
                
                # Check for unique class
                elif element.get('class'):
                    score += 5
                    classes = '.'.join(element.get('class')[:2])  # Use first 2 classes
                    selector = f"{element.name}.{classes}"
                
                # Text-based for buttons/links
                elif element.name in ['button', 'a'] and element.get_text(strip=True):
                    score += 6
                    text = element.get_text(strip=True)[:30]
                    selector = f"{element.name}:has-text('{text}')"
                
                else:
                    selector = element.name
                    score += 1
                
                if score > best_score:
                    best_score = score
                    best_candidate = selector
            
            return best_candidate
            
        except Exception as e:
            print(f"Semantic analysis error: {e}")
            return None
    
    def _extract_relevant_html(self, html_content: str, action_hint: str) -> str:
        """Extract only relevant HTML to reduce token usage"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Remove script and style tags
            for tag in soup(['script', 'style', 'noscript']):
                tag.decompose()
            
            # Focus on interactive elements
            interactive_tags = ['button', 'a', 'input', 'textarea', 'select', 'form']
            relevant_elements = soup.find_all(interactive_tags)
            
            # Build simplified HTML with context
            simplified = []
            for elem in relevant_elements[:50]:  # Limit to 50 elements
                # Include parent for context
                parent = elem.parent
                if parent:
                    simplified.append(str(parent)[:500])  # Limit each element
            
            return '\n'.join(simplified)
            
        except Exception as e:
            print(f"HTML extraction error: {e}")
            return html_content[:10000]
    
    def _clean_selector(self, selector: str) -> str:
        """Clean up AI-generated selector"""
        # Remove markdown code blocks
        if "```" in selector:
            parts = selector.split("```")
            for part in parts:
                if part.strip() and not part.strip().startswith('css'):
                    selector = part.strip()
                    break
        
        # Remove quotes if wrapped
        selector = selector.strip('"\'')
        
        # Remove any explanatory text (take first line only)
        selector = selector.split('\n')[0].strip()
        
        # Normalize quotes
        selector = selector.replace('"', "'")
        
        return selector
    
    def get_healing_stats(self) -> dict:
        """Get statistics about healing performance"""
        total = len(self.healing_history)
        if total == 0:
            return {'total': 0, 'success_rate': 0}
        
        successful = sum(1 for h in self.healing_history if h['success'])
        
        return {
            'total_healings': total,
            'successful': successful,
            'success_rate': (successful / total) * 100,
            'cache_stats': self.cache.get_stats() if self.cache else None
        }

