from sentence_transformers import SentenceTransformer


class Embedder:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed(self, texts):
        """
        Given a list of texts, return their embeddings.
        """
        return self.model.encode(
            texts, show_progress_bar=False, convert_to_tensor=False
        )
