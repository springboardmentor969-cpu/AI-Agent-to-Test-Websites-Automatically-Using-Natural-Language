import json
from xai_sdk import Client
from config import XAI_API_KEY

# Initialize Grok client
client = Client(api_key=XAI_API_KEY)

MODEL_NAME = "grok-beta"

SYSTEM_PROMPT = """
You are an AI Web Testing Agent.

Convert a natural language web testing instruction into a JSON array
of steps.

Each step MUST have:
- action: navigate | type | click
- target: element id (string)
- value: string or null

Rules:
1. Return ONLY valid JSON.
2. Do NOT add explanations.
3. Use element IDs directly.
4. navigation target should be ignored (handled by system).

Example output:
[
  {"action":"type","target":"username_field","value":"admin"},
  {"action":"click","target":"submit_button","value":null}
]
"""

def parse_instruction_llm(instruction: str) -> list:
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": instruction}
            ],
            temperature=0
        )

        content = response.choices[0].message.content.strip()

        # Ensure JSON-only output
        parsed = json.loads(content)

        if isinstance(parsed, list):
            return parsed

        return []

    except Exception as e:
        print("⚠️ Grok parsing failed:", e)
        return []
