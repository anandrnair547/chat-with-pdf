from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class Retriever:
    def __init__(self, embeddings, chunks):
        if not chunks or len(chunks) == 0:
            raise ValueError(
                "No content found in the document. Please check if the document contains any text or if it's properly formatted."
            )

        if not isinstance(embeddings, (list, np.ndarray)) or len(embeddings) == 0:
            raise ValueError(
                "No embeddings generated. Please check if the document contains any text or if it's properly formatted."
            )

        self.embeddings = np.array(embeddings)
        self.chunks = chunks  # Store the original text chunks

    def retrieve(self, query, top_k=5):
        from chat_with_pdf.embedder import Embedder

        if not query.strip():
            return ["Please provide a non-empty query."]

        embedder = Embedder()
        query_embedding = embedder.embed([query])[0]

        # Ensure we have valid embeddings
        if self.embeddings.size == 0:
            return ["No content found in the document to search through."]

        similarities = cosine_similarity([query_embedding], self.embeddings)[0]
        top_indices = similarities.argsort()[-top_k:][::-1]
        return [
            self.chunks[i] for i in top_indices
        ]  # Return the TEXT chunks, not embeddings
