from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class Retriever:
    def __init__(self, embeddings: list[list[float]], texts: list[str]):
        self.embeddings = np.array(embeddings)
        self.texts = texts

    def retrieve(self, query_embedding: list[float], top_k=3) -> list[str]:
        query_embedding = np.array(query_embedding).reshape(1, -1)
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]
        top_indices = similarities.argsort()[-top_k:][::-1]
        return [self.texts[i] for i in top_indices]
