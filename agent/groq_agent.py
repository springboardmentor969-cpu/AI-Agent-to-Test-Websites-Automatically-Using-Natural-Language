from groq import Groq
import os

# Read API key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("❌ GROQ_API_KEY not found. Check .env file")

# Create Groq client
client = Groq(api_key=api_key)

def get_steps_from_instruction(instruction):
    prompt = f"""
You are an automation testing agent.
Convert the following instruction into JSON steps ONLY.

Instruction:
{instruction}

Return STRICT JSON only, no explanation.

Format:
[
  {{ "action": "open", "url": "https://example.com" }},
  {{ "action": "search", "selector": "input[name='q']", "text": "query" }},
  {{ "action": "click", "selector": "css_selector" }}
]
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
