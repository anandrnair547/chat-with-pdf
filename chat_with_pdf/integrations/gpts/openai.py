import os
from .base import BaseProvider
from openai import (
    OpenAI,
    APIError,
    APIConnectionError,
    RateLimitError,
    AuthenticationError,
)

# Default timeout in seconds
DEFAULT_TIMEOUT = 60


class OpenAIProvider(BaseProvider):
    """Provider for OpenAI ChatCompletions."""

    def __init__(self, model: str = None):
        # Fetch API key from env
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OpenAI API key is required. Set OPENAI_API_KEY environment variable."
            )
        # Fetch model from env or use default
        model = model or os.getenv("OPENAI_MODEL", "gpt-4o")
        super().__init__(model)
        # Configure client with API key and timeout
        self.client = OpenAI(api_key=api_key, timeout=DEFAULT_TIMEOUT)

    def complete(self, query: str, context: str) -> str:
        system_prompt = self.build_system_prompt()
        messages = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion:\n{query} \n\n. Infer gender from the context and use appropriately. If gender is not inferred use binary pronouns like he/she or his/her appropriately.\n\n",
            },
        ]

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.2,
                max_tokens=500,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
                # Timeout can also be set per-request if needed, overriding client default
                # timeout=30,
            )

            try:
                # Safely access the response content
                return response.choices[0].message.content.strip()
            except (IndexError, AttributeError, TypeError) as e:
                print(f"Error parsing OpenAI response structure: {e}")
                print(f"Received response object: {response}")
                # Return empty string on parsing error
                return ""

        # Handle specific OpenAI API errors
        except AuthenticationError as e:
            print(f"OpenAI Authentication Error: {e}")
            # Potentially re-raise or handle specific auth issues
            return ""
        except RateLimitError as e:
            print(f"OpenAI Rate Limit Error: {e}")
            # Implement retry logic or inform the user
            return ""
        except APIConnectionError as e:
            print(f"OpenAI Connection Error: {e}")
            return ""
        except APIError as e:  # Catch other API-related errors
            print(f"OpenAI API Error: {e}")
            return ""
        except Exception as e:  # Catch any other unexpected errors
            print(f"An unexpected error occurred: {e}")
            return ""
