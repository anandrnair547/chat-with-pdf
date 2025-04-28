import fitz  # PyMuPDF
from io import BytesIO


class PDFParser:
    def __init__(self, chunk_size=500):
        self.chunk_size = chunk_size

    def parse(self, pdf_data):
        """
        Parses a PDF file (given as file path, URL content, or BytesIO) into text chunks.
        """
        if isinstance(pdf_data, (str, bytes)):
            # If pdf_data is a path or raw bytes, open normally
            doc = (
                fitz.open(stream=pdf_data, filetype="pdf")
                if isinstance(pdf_data, bytes)
                else fitz.open(pdf_data)
            )
        elif isinstance(pdf_data, BytesIO):
            # If it's already a BytesIO object
            doc = fitz.open(stream=pdf_data.read(), filetype="pdf")
        else:
            raise ValueError("Unsupported pdf_data type.")

        full_text = ""
        for page in doc:
            full_text += page.get_text()

        # Split into chunks
        chunks = self._split_into_chunks(full_text)
        return chunks

    def _split_into_chunks(self, text):
        """
        Splits large text into smaller chunks based on chunk size.
        """
        return [
            text[i : i + self.chunk_size] for i in range(0, len(text), self.chunk_size)
        ]
