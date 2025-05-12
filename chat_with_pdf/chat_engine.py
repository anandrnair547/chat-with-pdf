import os
import requests
from io import BytesIO
from chat_with_pdf import settings
from chat_with_pdf.pdf_parser import PDFParser
from chat_with_pdf.embedder import Embedder
from chat_with_pdf.retriever import Retriever
from chat_with_pdf.utils import ask_llm


class PDFChat:
    def __init__(
        self,
        pdf_source,
        model=None,
        embedding_model=None,
        chunk_size=None,
        top_k_retrieval=None,
    ):
        # Settings priority: passed arg > settings default
        self.model = model or settings.DEFAULT_MODEL
        self.embedding_model = embedding_model or settings.DEFAULT_EMBEDDING_MODEL
        self.chunk_size = chunk_size or settings.DEFAULT_CHUNK_SIZE
        self.top_k_retrieval = top_k_retrieval or settings.TOP_K_RETRIEVAL

        # Initialize components
        self.parser = PDFParser(chunk_size=self.chunk_size)
        self.embedder = Embedder(model_name=self.embedding_model)
        self.retriever = None

        # Load and prepare
        self._load_and_prepare_document(pdf_source)

    def _load_and_prepare_document(self, pdf_source):
        pdf_data = self._resolve_pdf_source(pdf_source)
        self.chunks = self.parser.parse(pdf_data)
        self.embeddings = self.embedder.embed(self.chunks)
        self.retriever = Retriever(self.embeddings, self.chunks)

    def _resolve_pdf_source(self, pdf_source):
        if isinstance(pdf_source, bytes):
            # Binary PDF provided directly
            return BytesIO(pdf_source)

        elif isinstance(pdf_source, str):
            if pdf_source.startswith("http://") or pdf_source.startswith("https://"):
                # It's a URL, download
                response = requests.get(pdf_source)
                response.raise_for_status()
                return BytesIO(response.content)
            else:
                # Assume local file path
                if not os.path.exists(pdf_source):
                    raise FileNotFoundError(f"File not found: {pdf_source}")
                with open(pdf_source, "rb") as f:
                    return BytesIO(f.read())

        else:
            raise ValueError(
                "Unsupported pdf_source type. Provide a file path, URL, or bytes."
            )

    def ask(self, query):
        relevant_chunks = self.retriever.retrieve(query, top_k=self.top_k_retrieval)
        context = "\n".join(relevant_chunks)
        response = ask_llm(query=query, context=context, model=self.model)
        return response
