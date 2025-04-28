import os
from .integrations.gpts import get_provider


def ask_llm(query: str, context: str, model: str = None) -> str:
    """
    Unified entry-point for all LLMs.

    It will pick up:
      1) provider override passed in here
      2) environment var LLM_PROVIDER (defaults to "openai")

    Similarly for model:
      1) model override passed in here
      2) env var <PROVIDER>_MODEL, or the provider’s own default

    Then calls the provider’s .complete() under the hood.
    """
    # figure out which provider to use
    provider_name = os.getenv("LLM_PROVIDER", "openai").lower()

    # build an instance of that provider
    # get_provider will itself read OPENAI_API_KEY, OPENAI_MODEL, etc.
    llm = get_provider(provider_name, model=model)

    # do the completion
    return llm.complete(query, context)
