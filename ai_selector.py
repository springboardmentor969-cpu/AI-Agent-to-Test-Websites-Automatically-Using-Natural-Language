import os
import requests

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Load from environment for safety
GROK_API_KEY = os.getenv("GROK_API_KEY")
GROK_URL = "https://api.x.ai/v1/chat/completions"

class AISelectorHealer:

    def heal(self, html_content, failed_selector, action_hint):
        """
        Use Grok to analyze the DOM and suggest the correct selector.
        """
        if not GROK_API_KEY:
            print("⚠️ AI Healer Warning: GROK_API_KEY not found in environment. Fallback to original selector.")
            return failed_selector

        prompt = f"""
        You are an expert in Web Automation.
        Failed Selector: {failed_selector}
        Intended Action: {action_hint}

        HTML SNIPPET:
        {html_content[:10000]}

        TASK:
        Find the element that matches the Intended Action.
        Return ONLY the MOST STABLE CSS selector (prefer IDs).
        No text, no markdown, no quotes. Just the selector.
        """

        try:
            response = requests.post(
                GROK_URL,
                headers={
                    "Authorization": f"Bearer {GROK_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "grok-1",
                    "messages": [
                        {"role": "system", "content": "You are a CSS selector generator."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.1
                }
            )

            result = response.json()
            selector = result["choices"][0]["message"]["content"].strip()

            # Remove any AI chatter or markdown
            if "```" in selector:
                selector = selector.split("```")[-2].replace("css", "").strip()

            return selector.replace('"', "'")
        except Exception as e:
            print(f"AI Healer Error: {e}")
            return failed_selector