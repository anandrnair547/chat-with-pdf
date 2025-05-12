import os
from .integrations.gpts import get_provider
from chat_with_pdf import settings


def ask_llm(query: str, context: str, model: str = None) -> str:
    """
    Unified entry-point for all LLMs.

    It will pick up:
      1) provider override passed in here
      2) settings.LLM_PROVIDER (defaults to "openai")

    Similarly for model:
      1) model override passed in here
      2) settings.DEFAULT_MODEL

    Then calls the provider's .complete() under the hood.
    """
    # figure out which provider to use
    provider_name = settings.LLM_PROVIDER or "openai"

    # build an instance of that provider
    llm = get_provider(provider_name, model=model)

    # do the completion
    return llm.complete(query, context)
