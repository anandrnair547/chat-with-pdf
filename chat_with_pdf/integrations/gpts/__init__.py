import os
from .base import BaseProvider
from .deepseek import DeepSeekProvider
from .openai import OpenAIProvider
from .perplexity import PerplexityProvider
from .portkey import PortkeyProvider
from typing import Optional

# Registry of available providers
_PROVIDERS = {
    "openai": OpenAIProvider,
    "perplexity-ai": PerplexityProvider,
    "deepseek": DeepSeekProvider,
    "portkey": PortkeyProvider,
}


def get_provider(provider_name: str, model: Optional[str] = None) -> BaseProvider:
    """
    Factory function to instantiate the specified LLM provider.

    If a Portkey API key is set, PortkeyProvider will be used regardless
    of the provider_name argument.

    Args:
        provider_name: Key of the provider in _PROVIDERS (e.g. 'openai', 'portkey').
        model: Model identifier to use (overrides env var or default).

    Returns:
        An instance of BaseProvider configured accordingly.

    Raises:
        ValueError: If the provider_name is unsupported.
    """
    # If Portkey credentials are present, always use PortkeyProvider
    if os.getenv("PORTKEY_API_KEY"):
        return PortkeyProvider(model=model)

    # Otherwise use the specified provider_name
    key = provider_name.lower()
    ProviderCls = _PROVIDERS.get(key)
    if not ProviderCls:
        raise ValueError(f"Unsupported provider: {provider_name}")

    return ProviderCls(model=model)
