import os
from typing import List

# Retry settings
MAX_RETRIES = 2

# Ordered by preference - using correct Groq model names
SUPPORTED_GROQ_MODELS: List[str] = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "mixtral-8x7b-32768",
]

def groq_api_key() -> str:
    key = os.getenv("GROQ_API_KEY")
    if not key:
        raise RuntimeError("GROQ_API_KEY not set in environment")
    return key

def preferred_model() -> str:
    return os.getenv("GROQ_MODEL", SUPPORTED_GROQ_MODELS[0])

