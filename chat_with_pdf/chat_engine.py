from .pdf_parser import extract_text_from_pdf
from .embedder import Embedder
from .retriever import Retriever

import openai  # Assuming you're using OpenAI for generation
import textwrap


class PDFChat:
    def __init__(self, pdf_path: str, openai_api_key: str):
        self.text = extract_text_from_pdf(pdf_path)
        self.chunks = textwrap.wrap(self.text, width=1000)  # Basic chunking
        self.embedder = Embedder()
        self.embeddings = self.embedder.embed_texts(self.chunks)
        self.retriever = Retriever(self.embeddings, self.chunks)
        openai.api_key = openai_api_key

    def ask(self, question: str) -> str:
        question_embedding = self.embedder.embed_texts([question])[0]
        relevant_chunks = self.retriever.retrieve(question_embedding)

        prompt = f"Answer the question based on the following document excerpts:\n\n{''.join(relevant_chunks)}\n\nQuestion: {question}\nAnswer:"

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or use GPT-4 if you want
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
        )

        return response["choices"][0]["message"]["content"]
