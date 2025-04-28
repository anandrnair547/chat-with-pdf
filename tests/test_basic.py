import pytest
from chat_with_pdf import PDFChat
import os
from io import BytesIO


@pytest.fixture
def dummy_pdf(tmp_path):
    """Creates a temporary PDF file for local testing."""
    from fpdf import FPDF

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="This is a dummy PDF for testing.", ln=True, align="C")
    dummy_path = tmp_path / "test.pdf"
    pdf.output(str(dummy_path))
    return dummy_path


@pytest.fixture
def dummy_pdf_bytes(dummy_pdf):
    """Loads the dummy PDF into bytes."""
    with open(dummy_pdf, "rb") as f:
        return f.read()


def test_pdfchat_local_file(dummy_pdf):
    """Test initializing PDFChat with a local file path."""
    chat = PDFChat(str(dummy_pdf), openai_api_key="dummy-key")
    assert chat is not None
    assert isinstance(chat.chunks, list)
    assert len(chat.chunks) > 0


def test_pdfchat_binary_data(dummy_pdf_bytes):
    """Test initializing PDFChat with PDF binary data."""
    chat = PDFChat(dummy_pdf_bytes, openai_api_key="dummy-key")
    assert chat is not None
    assert isinstance(chat.chunks, list)
    assert len(chat.chunks) > 0


@pytest.mark.skip(
    reason="Requires internet access to test downloading PDFs from a URL."
)
def test_pdfchat_remote_url():
    """Test initializing PDFChat with a remote URL."""
    # You can use a small public PDF for testing.
    # Example URL: https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf
    pdf_url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
    chat = PDFChat(pdf_url, openai_api_key="dummy-key")
    assert chat is not None
    assert isinstance(chat.chunks, list)
    assert len(chat.chunks) > 0


def test_pdfchat_ask(monkeypatch, dummy_pdf):
    """Test the ask method with mocked OpenAI API."""

    def dummy_openai_chatcompletion_create(*args, **kwargs):
        return {"choices": [{"message": {"content": "Dummy Answer"}}]}

    import openai

    monkeypatch.setattr(
        openai.ChatCompletion, "create", dummy_openai_chatcompletion_create
    )

    chat = PDFChat(str(dummy_pdf), openai_api_key="dummy-key")
    response = chat.ask("What is in the document?")
    assert isinstance(response, str)
    assert "Dummy Answer" in response
