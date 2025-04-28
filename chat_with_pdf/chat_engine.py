import os
from chat_with_pdf import settings
from chat_with_pdf.pdf_parser import PDFParser
from chat_with_pdf.embedder import Embedder
from chat_with_pdf.retriever import Retriever
from chat_with_pdf.utils import ask_llm


class PDFChat:
    def __init__(
        self,
        pdf_path,
        openai_api_key=None,
        model=None,
        embedding_model=None,
        chunk_size=None,
        top_k_retrieval=None,
    ):
        # Load from arguments first, then environment variables, then defaults
        self.openai_api_key = (
            openai_api_key or os.getenv("OPENAI_API_KEY") or settings.OPENAI_API_KEY
        )
        self.model = model or os.getenv("OPENAI_MODEL") or settings.DEFAULT_MODEL
        self.embedding_model = (
            embedding_model
            or os.getenv("EMBEDDING_MODEL")
            or settings.DEFAULT_EMBEDDING_MODEL
        )
        self.chunk_size = (
            int(chunk_size)
            if chunk_size is not None
            else int(os.getenv("DEFAULT_CHUNK_SIZE", settings.DEFAULT_CHUNK_SIZE))
        )
        self.top_k_retrieval = (
            int(top_k_retrieval)
            if top_k_retrieval is not None
            else int(os.getenv("TOP_K_RETRIEVAL", settings.TOP_K_RETRIEVAL))
        )

        # Initialize components
        self.parser = PDFParser(chunk_size=self.chunk_size)
        self.embedder = Embedder(model_name=self.embedding_model)
        self.retriever = None  # Will initialize after parsing and embedding

        # Load and prepare the document
        self._load_and_prepare_document(pdf_path)

    def _load_and_prepare_document(self, pdf_path):
        # Parse the PDF
        self.chunks = self.parser.parse(pdf_path)

        # Create embeddings
        self.embeddings = self.embedder.embed(self.chunks)

        # Initialize retriever
        self.retriever = Retriever(self.embeddings)

    def ask(self, query):
        # Find similar chunks
        relevant_chunks = self.retriever.retrieve(query, top_k=self.top_k_retrieval)

        # Build context
        context = "\n".join(relevant_chunks)

        # Ask LLM
        response = ask_llm(
            query=query, context=context, api_key=self.openai_api_key, model=self.model
        )
        return response
