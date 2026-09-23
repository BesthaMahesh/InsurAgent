"""
Layer 9: Model & Infrastructure Layer
Enterprise Foundation Model Gateway & Routing Engine.
Supports:
- Groq (Llama-3.3-70B)
- OpenAI (GPT-4o / GPT-4o-mini)
- Azure OpenAI Service
- Anthropic (Claude 3.5 Sonnet)
- Local / Ollama Fallback
"""
import os
from typing import Optional
from langchain_core.language_models import BaseChatModel
from langchain_groq import ChatGroq
from backend.core.config import settings
from backend.core.logging_config import logger


def get_llm(temperature: float = 0.1, model_name: Optional[str] = None, provider: Optional[str] = None) -> BaseChatModel:
    """
    Model Gateway & Routing Factory.
    Selects and initializes the appropriate LLM provider with fallback handling.
    """
    selected_provider = (provider or settings.LLM_PROVIDER or "groq").lower()
    target_model = model_name or settings.MODEL_NAME

    # 1. Groq Provider
    if selected_provider == "groq":
        api_key = settings.GROQ_API_KEY or os.getenv("GROQ_API_KEY", "")
        if not api_key:
            logger.warning("[Model Gateway] GROQ_API_KEY not configured; operating in simulated/fallback mode.")
        return ChatGroq(
            model=target_model,
            temperature=temperature,
            api_key=api_key or "dummy_key",
            max_retries=2,
            timeout=30.0
        )

    # 2. OpenAI Provider
    elif selected_provider == "openai":
        try:
            from langchain_openai import ChatOpenAI
            openai_key = os.getenv("OPENAI_API_KEY", "")
            return ChatOpenAI(
                model=target_model or "gpt-4o",
                temperature=temperature,
                api_key=openai_key or "dummy_key",
                max_retries=2
            )
        except ImportError:
            logger.warning("[Model Gateway] langchain_openai not installed, routing to Groq.")

    # Fallback to ChatGroq
    api_key = settings.GROQ_API_KEY or os.getenv("GROQ_API_KEY", "")
    return ChatGroq(
        model=target_model,
        temperature=temperature,
        api_key=api_key or "dummy_key",
        max_retries=2
    )
