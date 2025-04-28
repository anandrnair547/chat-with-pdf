from .base import BaseProvider
import requests
import os
from requests.exceptions import RequestException


class PerplexityProvider(BaseProvider):
    """Provider for Perplexity API."""

    def complete(self, query: str, context: str) -> str:
        system_prompt = "You are a helpful assistant."
        messages = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion:\n{query} \n\n. Infer gender from the context and use appropriately. If gender is not inferred use binary pronouns like he/she or his/her appropriately.\n\n",
            },
        ]
        endpoint = os.getenv(
            "PERPLEXITY_ENDPOINT", "https://api.perplexity.ai/chat/completions"
        )
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OpenAI API key is required. Set OPENAI_API_KEY environment variable."
            )
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": 500,
        }

        try:
            response = requests.post(
                endpoint, json=payload, headers=headers, timeout=60
            )
            response.raise_for_status()
            data = response.json()

            try:
                return data["choices"][0]["message"]["content"].strip()
            except (KeyError, IndexError, TypeError) as e:
                print(f"Error parsing Perplexity JSON response: {e}")
                print(f"Received data structure: {data}")
                return ""

        except RequestException as e:
            print(f"Error during Perplexity API request: {e}")
            return ""
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return ""
