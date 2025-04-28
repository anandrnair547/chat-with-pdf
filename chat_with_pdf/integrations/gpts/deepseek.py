from .base import BaseProvider
import os
import requests
from requests.exceptions import RequestException


class DeepSeekProvider(BaseProvider):
    """Provider for DeepSeek API."""

    def complete(self, query: str, context: str) -> str:
        endpoint = os.getenv(
            "DEEPSEEK_ENDPOINT", "https://api.deepseek.com/chat/completions"
        )
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OpenAI API key is required. Set OPENAI_API_KEY environment variable."
            )

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion:\n{query} \n\n. Infer gender from the context and use appropriately. If gender is not inferred use binary pronouns like he/she or his/her appropriately.\n\n",
            },
        ]
        payload = {
            "model": self.model,
            "messages": messages,
            # Add other parameters like max_tokens if needed and supported
            # "max_tokens": 500,
        }

        try:
            # Added timeout
            response = requests.post(
                endpoint, json=payload, headers=headers, timeout=60
            )
            # Raises HTTPError for bad responses (4xx or 5xx)
            response.raise_for_status()
            data = response.json()

            try:
                # Extract content, ensuring keys and index exist
                return data["choices"][0]["message"]["content"].strip()
            except (KeyError, IndexError, TypeError) as e:
                print(f"Error parsing DeepSeek JSON response: {e}")
                print(f"Received data structure: {data}")
                # Return empty string on parsing error
                return ""

        except RequestException as e:
            # Handle connection errors, timeouts, etc.
            print(f"Error during DeepSeek API request: {e}")
            # Return empty string on request error
            return ""
        except Exception as e:
            # Catch any other unexpected errors during the request/parsing
            print(f"An unexpected error occurred: {e}")
            return ""
