# File: chat_with_pdf/providers/portkey.py
"""
Provider implementation for Portkey.ai LLM integration using the official portkey_ai SDK.
"""

import os
from portkey_ai import Portkey, AsyncPortkey
from .base import BaseProvider


class PortkeyProvider(BaseProvider):
    """LLM provider that routes calls through Portkey.ai gateway via the portkey_ai SDK."""

    def __init__(
        self,
        model: str = None,
        provider: str = None,
    ):
        # Load credentials
        portkey_api_key = os.getenv("PORTKEY_API_KEY")
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("Missing PORTKEY_API_KEY environment variable")

        virtual_key = os.getenv("PORTKEY_VIRTUAL_KEY", None)

        # Determine model
        self.model = model or os.getenv("OPENAI_MODEL") or "gpt-4o"
        # Determine provider identifier
        provider = provider or os.getenv("LLM_PROVIDER") or "portkey"
        config = {
            "retry": {"attempts": 5},
            "cache": {"mode": "simple"},
            "api_key": api_key,
            "provider": provider,
        }

        # Build client arguments
        client_kwargs = {
            "api_key": portkey_api_key,
            "config": config,
        }

        if virtual_key:
            client_kwargs["virtual_key"] = virtual_key

        # Initialize synchronous & asynchronous clients
        self.client = Portkey(**client_kwargs)
        self.async_client = AsyncPortkey(**client_kwargs)

    def complete(self, prompt: str, context: str = "") -> str:
        """
        Synchronously send a chat completion request via Portkey.ai.
        Optionally include a system prompt as context.
        """
        messages = []
        if context:
            messages.append({"role": "system", "content": context})
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )
        return response.choices[0].message.content

    async def acomplete(self, prompt: str, context: str = "") -> str:
        """
        Asynchronously send a chat completion request via Portkey.ai.
        Optionally include a system prompt as context.
        """
        messages = []
        if context:
            messages.append({"role": "system", "content": context})
        messages.append({"role": "user", "content": prompt})

        response = await self.async_client.chat.completions.create(
            model=self.model,
            messages=messages,
        )
        return response.choices[0].message.content
