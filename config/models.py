"""Gemini model factory for LangChain agents."""

from langchain_google_genai import ChatGoogleGenerativeAI

GEMINI_FLASH = "gemini-2.5-flash"
GEMINI_PRO   = "gemini-3-pro-preview"


def get_gemini(model=GEMINI_FLASH, thinking=False):
    """Create a ChatGoogleGenerativeAI instance.

    Args:
        model: Gemini model ID. Defaults to GEMINI_FLASH.
        thinking: Enable extended thinking. Defaults to False.

    Returns:
        Configured ChatGoogleGenerativeAI instance.
    """
    return ChatGoogleGenerativeAI(
        model=model,
        thinking_budget=0 if not thinking else 1024,
        include_thoughts=thinking,
    )
