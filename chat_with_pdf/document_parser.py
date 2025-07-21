import fitz  # PyMuPDF
from io import BytesIO
from PIL import Image
import pytesseract
from docx import Document
import os
import shutil
import tempfile


class DocumentParser:
    """Parser for various document types (PDF, DOCX, PNG, JPEG)."""

    def __init__(self, chunk_size=500):
        self.chunk_size = chunk_size
        # Check if tesseract is installed
        if not shutil.which("tesseract"):
            raise RuntimeError(
                "Tesseract OCR is not installed or not in PATH. "
                "Please install it:\n"
                "  - macOS: brew install tesseract\n"
                "  - Ubuntu: sudo apt-get install tesseract-ocr\n"
                "  - Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki"
            )

    def parse(self, document_data, file_type=None):
        """
        Parse a document into text chunks.

        Args:
            document_data: File path, URL content, or BytesIO
            file_type: Optional file type hint ('pdf', 'docx', 'png', 'jpeg')
        """
        if isinstance(document_data, (str, bytes)):
            # If document_data is a path or raw bytes
            if isinstance(document_data, str):
                if not os.path.exists(document_data):
                    raise FileNotFoundError(f"File not found: {document_data}")
                with open(document_data, "rb") as f:
                    document_data = f.read()

            # Determine file type from content if not provided
            if not file_type:
                file_type = self._detect_file_type(document_data)

            # Convert bytes to BytesIO
            document_data = BytesIO(document_data)

        # Parse based on file type
        if file_type == "pdf":
            text = self._parse_pdf(document_data)
        elif file_type in ["png", "jpeg", "jpg"]:
            text = self._parse_image(document_data)
        elif file_type == "docx":
            text = self._parse_docx(document_data)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

        # Check if we got any text
        if not text or not text.strip():
            raise ValueError(
                f"No text content found in the {file_type} document. "
                "The document might be empty, corrupted, or contain only images without text. "
                "If the document contains images with text, make sure Tesseract OCR is properly installed."
            )

        # Split into chunks and filter empty ones
        chunks = self._split_into_chunks(text)
        chunks = [chunk for chunk in chunks if chunk.strip()]

        if not chunks:
            raise ValueError(
                f"Could not extract any meaningful text chunks from the {file_type} document. "
                "The document might be empty or contain only images without text. "
                "If the document contains images with text, make sure Tesseract OCR is properly installed."
            )

        return chunks

    def _detect_file_type(self, data):
        """Detect file type from binary data."""
        if data.startswith(b"%PDF"):
            return "pdf"
        elif data.startswith(b"\x50\x4b\x03\x04"):  # DOCX signature
            return "docx"
        elif data.startswith(b"\xff\xd8\xff"):  # JPEG signature
            return "jpeg"
        elif data.startswith(b"\x89PNG"):  # PNG signature
            return "png"
        else:
            raise ValueError("Could not detect file type from content")

    def _parse_pdf(self, pdf_data):
        """Parse PDF document including embedded images."""
        doc = fitz.open(stream=pdf_data.read(), filetype="pdf")
        text = ""
        image_count = 0
        has_text = False
        has_images = False

        # Create a temporary directory for images
        with tempfile.TemporaryDirectory() as temp_dir:
            for page_num, page in enumerate(doc):
                # Extract text
                page_text = page.get_text()
                if page_text.strip():
                    has_text = True
                    text += page_text

                # Extract and process images
                image_list = page.get_images()
                if image_list:
                    has_images = True
                    for img_index, img in enumerate(image_list):
                        try:
                            xref = img[0]
                            base_image = doc.extract_image(xref)
                            image_bytes = base_image["image"]
                            image_ext = base_image["ext"]

                            # Save image to temporary file
                            temp_image_path = os.path.join(
                                temp_dir,
                                f"page_{page_num + 1}_img_{img_index + 1}.{image_ext}",
                            )
                            with open(temp_image_path, "wb") as img_file:
                                img_file.write(image_bytes)

                            # Process image with OCR
                            image_text = pytesseract.image_to_string(
                                Image.open(temp_image_path), lang="eng+ara"
                            )
                            if image_text.strip():
                                image_count += 1
                                text += f"\n[Image {image_count} on page {page_num + 1}]: {image_text}\n"
                        except Exception as e:
                            print(
                                f"Error processing image {img_index} on page {page_num + 1}: {e}"
                            )
                            continue

        if not has_text and not has_images:
            raise ValueError(
                "PDF document appears to be empty (no text or images found)."
            )
        elif not has_text and has_images:
            print(
                "Warning: PDF contains only images. Text extraction depends on OCR quality."
            )

        return text

    def _parse_image(self, image_data):
        """Parse image using OCR."""
        # Save image to temporary file for better OCR
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
            image = Image.open(image_data)
            image.save(temp_file.name)
            text = pytesseract.image_to_string(Image.open(temp_file.name))
            os.unlink(temp_file.name)  # Clean up temporary file

        if not text.strip():
            raise ValueError("No text could be extracted from the image using OCR.")
        return text

    def _parse_docx(self, docx_data):
        """Parse DOCX document."""
        doc = Document(docx_data)
        text = ""
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text += paragraph.text + "\n"
        return text

    def _split_into_chunks(self, text):
        """Split text into chunks of specified size."""
        if not text.strip():
            return []
        return [
            text[i : i + self.chunk_size] for i in range(0, len(text), self.chunk_size)
        ]
