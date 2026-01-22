from langchain_groq import ChatGroq
from agent.config import (
    groq_api_key,
    preferred_model,
    SUPPORTED_GROQ_MODELS
)

def get_llm() -> ChatGroq:
    """
    Returns a Groq LLM client using the preferred model.
    Falls back automatically if a model is unavailable.
    """
    last_error = None

    for model in [preferred_model(), *SUPPORTED_GROQ_MODELS]:
        try:
            # Model names should NOT have 'groq/' prefix
            model_name = model.replace("groq/", "") if model.startswith("groq/") else model
            
            return ChatGroq(
                model=model_name,
                temperature=0,
                api_key=groq_api_key(),
                timeout=30
            )
        except Exception as e:
            last_error = e

    raise RuntimeError(
        f"All Groq models failed. Last error: {last_error}"
    )

