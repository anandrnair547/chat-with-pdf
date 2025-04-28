from abc import ABC, abstractmethod


class BaseProvider(ABC):
    """
    Abstract base class for LLM providers.
    """

    def __init__(self, model: str):
        self.model = model

    @abstractmethod
    def complete(self, query: str, context: str) -> str:
        """Generate a response given a user query and context."""
        pass

    def build_system_prompt(self) -> str:
        """Construct the system prompt with pronoun guidance."""
        prompt = "You are a helpful assistant that answers questions based on provided context. Infer gender from the context and use appropriately. If gender is not inferred use binary pronouns like he/she or his/her appropriately.\n\n"
        return prompt
