from chat_with_pdf import PDFChat
import pytest
import os


@pytest.fixture
def dummy_pdf(tmp_path):
    # Create a temporary PDF file for testing
    from fpdf import FPDF  # Tiny dependency, or you can skip real file creation

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="This is a dummy PDF for testing.", ln=True, align="C")
    dummy_path = tmp_path / "test.pdf"
    pdf.output(str(dummy_path))
    return dummy_path


def test_pdfchat_initialization(dummy_pdf):
    # Check if PDFChat initializes without errors
    chat = PDFChat(str(dummy_pdf), openai_api_key="dummy-key")
    assert chat is not None


def test_pdfchat_ask_method(monkeypatch, dummy_pdf):
    # Mock OpenAI call
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
