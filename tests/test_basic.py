import pytest
from chat_with_pdf import PDFChat


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    # Ensure the OpenAI API key and default provider/model are set
    monkeypatch.setenv("OPENAI_API_KEY", "dummy-key")
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.setenv("OPENAI_MODEL", "gpt-3.5-turbo")


@pytest.fixture
def dummy_pdf(tmp_path):
    """Creates a temporary PDF file for local testing."""
    from fpdf import FPDF

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="This is a dummy PDF for testing.", ln=True, align="C")
    path = tmp_path / "test.pdf"
    pdf.output(str(path))
    return path


@pytest.fixture
def dummy_pdf_bytes(dummy_pdf):
    """Loads the dummy PDF into bytes."""
    with open(dummy_pdf, "rb") as f:
        return f.read()


def test_pdfchat_local_file(dummy_pdf):
    """Test initializing PDFChat with a local file path."""
    chat = PDFChat(str(dummy_pdf))
    assert chat is not None
    assert isinstance(chat.chunks, list)
    assert len(chat.chunks) > 0


def test_pdfchat_binary_data(dummy_pdf_bytes):
    """Test initializing PDFChat with PDF binary data."""
    chat = PDFChat(dummy_pdf_bytes)
    assert chat is not None
    assert isinstance(chat.chunks, list)
    assert len(chat.chunks) > 0


@pytest.mark.skip(
    reason="Requires internet access to test downloading PDFs from a URL."
)
def test_pdfchat_remote_url():
    """Test initializing PDFChat with a remote URL."""
    url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
    chat = PDFChat(url)
    assert chat is not None
    assert isinstance(chat.chunks, list)
    assert len(chat.chunks) > 0


def test_pdfchat_ask(monkeypatch, dummy_pdf):
    """Test the ask method with a dummy LLM response."""
    # Monkeypatch ask_llm in chat_engine to return a fixed answer
    import chat_with_pdf.chat_engine as engine_module

    monkeypatch.setattr(
        engine_module, "ask_llm", lambda *args, **kwargs: "Dummy Answer"
    )

    chat = PDFChat(str(dummy_pdf))
    response = chat.ask("What is in the document?")
    assert isinstance(response, str)
    assert response == "Dummy Answer"
