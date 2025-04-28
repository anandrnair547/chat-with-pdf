from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class Retriever:
    def __init__(self, embeddings, chunks):
        self.embeddings = np.array(embeddings)
        self.chunks = chunks  # Store the original text chunks

    def retrieve(self, query, top_k=5):
        from chat_with_pdf.embedder import Embedder

        embedder = Embedder()
        query_embedding = embedder.embed([query])[0]

        similarities = cosine_similarity([query_embedding], self.embeddings)[0]
        top_indices = similarities.argsort()[-top_k:][::-1]
        return [
            self.chunks[i] for i in top_indices
        ]  # Return the TEXT chunks, not embeddings
