import os
import requests
from io import BytesIO
from chat_with_pdf import settings
from chat_with_pdf.document_parser import DocumentParser
from chat_with_pdf.embedder import Embedder
from chat_with_pdf.retriever import Retriever
from chat_with_pdf.utils import ask_llm


class DocumentChat:
    def __init__(
        self,
        document_source,
        model=None,
        embedding_model=None,
        chunk_size=None,
        top_k_retrieval=None,
        file_type=None,
    ):
        # Settings priority: passed arg > settings default
        self.model = model or settings.DEFAULT_MODEL
        self.embedding_model = embedding_model or settings.DEFAULT_EMBEDDING_MODEL
        self.chunk_size = chunk_size or settings.DEFAULT_CHUNK_SIZE
        self.top_k_retrieval = top_k_retrieval or settings.TOP_K_RETRIEVAL
        self.file_type = file_type

        # Initialize components
        self.parser = DocumentParser(chunk_size=self.chunk_size)
        self.embedder = Embedder(model_name=self.embedding_model)
        self.retriever = None

        # Load and prepare
        self._load_and_prepare_document(document_source)

    def _load_and_prepare_document(self, document_source):
        document_data = self._resolve_document_source(document_source)
        self.chunks = self.parser.parse(document_data, file_type=self.file_type)
        self.embeddings = self.embedder.embed(self.chunks)
        self.retriever = Retriever(self.embeddings, self.chunks)

    def _resolve_document_source(self, document_source):
        if isinstance(document_source, bytes):
            # Binary document provided directly
            return BytesIO(document_source)

        elif isinstance(document_source, str):
            if document_source.startswith("http://") or document_source.startswith(
                "https://"
            ):
                # It's a URL, download
                response = requests.get(document_source)
                response.raise_for_status()
                return BytesIO(response.content)
            else:
                # Assume local file path
                if not os.path.exists(document_source):
                    raise FileNotFoundError(f"File not found: {document_source}")
                with open(document_source, "rb") as f:
                    return BytesIO(f.read())

        else:
            raise ValueError(
                "Unsupported document_source type. Provide a file path, URL, or bytes."
            )

    def ask(self, query):
        relevant_chunks = self.retriever.retrieve(query, top_k=self.top_k_retrieval)
        context = "\n".join(relevant_chunks)
        print("context", context)
        response = ask_llm(query=query, context=context, model=self.model)
        return response


# For backward compatibility
PDFChat = DocumentChat
