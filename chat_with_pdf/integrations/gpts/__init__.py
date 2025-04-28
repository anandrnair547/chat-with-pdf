from .base import BaseProvider
from .deepseek import DeepSeekProvider
from .openai import OpenAIProvider
from .perplexity import PerplexityProvider
from typing import Optional

# Registry of available providers
_PROVIDERS = {
    "openai": OpenAIProvider,
    "perplexity": PerplexityProvider,
    "deepseek": DeepSeekProvider,
}


def get_provider(provider_name: str, model: Optional[str] = None) -> BaseProvider:
    """
    Factory function to instantiate the specified LLM provider.

    Args:
        provider_name: Key of the provider in _PROVIDERS (e.g. 'openai').
        api_key: API key for the provider (overrides env var).
        model: Model identifier to use (overrides env var or default).

    Returns:
        An instance of BaseProvider configured accordingly.

    Raises:
        ValueError: If the provider_name is unsupported.
    """
    key = provider_name.lower()
    ProviderCls = _PROVIDERS.get(key)
    if not ProviderCls:
        raise ValueError(f"Unsupported provider: {provider_name}")

    # Instantiate and return the provider with provided settings
    return ProviderCls(model=model)
