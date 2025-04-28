
# 📄 Chat with PDF

[![PyPI version](https://badge.fury.io/py/chat-with-pdf.svg)](https://badge.fury.io/py/chat-with-pdf)
[![Build Status](https://github.com/anandrnair547/chat-with-pdf/actions/workflows/ci.yml/badge.svg)](https://github.com/anandrnair547/chat-with-pdf/actions)

Chat with your PDF documents easily using local embeddings and powerful LLMs like OpenAI's GPT models.


**Chat with your PDF documents** easily using local embeddings and powerful LLMs like OpenAI's GPT models.

Upload any PDF and ask natural language questions about its content — powered by semantic search and AI.

---

## 🛠️ Installation

```bash
pip install chat-with-pdf
```

Or using Poetry:

```bash
poetry add chat-with-pdf
```

---

## ✨ Quickstart Example

```python
from chat_with_pdf import PDFChat

chat = PDFChat('path/to/your/document.pdf')


response = chat.ask("Summarize the introduction section.")
print(response)


```

You can pass a **file path**, **URL**, or **binary bytes** of the PDF to `PDFChat`.

Example:

```python
chat = PDFChat("path/to/file.pdf")
chat = PDFChat("https://example.com/file.pdf")
chat = PDFChat(binary_pdf_data)

```

---

## ⚙️ Configuration Options

You can configure your usage via **arguments**, **environment variables**, or let it fallback to defaults.

### Priority:

1. Arguments passed to `PDFChat`
2. Environment Variables
3. Library defaults

### Supported Environment Variables:

| Variable             | Purpose                                           | Default            |
| :------------------- | :------------------------------------------------ | :----------------- |
| `OPENAI_API_KEY`     | Your OpenAI API key                               | "" (empty)         |
| `OPENAI_MODEL`       | GPT model name to use                             | "gpt-3.5-turbo"    |
| `EMBEDDING_MODEL`    | Embedding model for vector search                 | "all-MiniLM-L6-v2" |
| `DEFAULT_CHUNK_SIZE` | Number of characters per text chunk               | 500                |
| `TOP_K_RETRIEVAL`    | Number of similar chunks to retrieve per question | 5                  |

### Example `.env` file:

```plaintext
OPENAI_API_KEY=sk-xxxxx
OPENAI_MODEL=gpt-4
DEFAULT_CHUNK_SIZE=600
TOP_K_RETRIEVAL=8
EMBEDDING_MODEL=all-mpnet-base-v2
```

If you have a `.env` file at your project root, `chat-with-pdf` will automatically load it.

---

## 🔥 Advanced Usage Example

Explicitly passing all settings:

```python
from chat_with_pdf import PDFChat

chat = PDFChat(
    'path/to/your/document.pdf',
    openai_api_key="sk-your-openai-key",
    model="gpt-4",
    embedding_model="all-mpnet-base-v2",
    chunk_size=600,
    top_k_retrieval=8
)

response = chat.ask("Summarize the key points.")
print(response)
```

---

## 📝 License

This project is licensed under the [MIT License](LICENSE).

---

## 🌟 Acknowledgements

- [OpenAI](https://openai.com/)
- [HuggingFace Sentence Transformers](https://www.sbert.net/)
- [PyMuPDF](https://pymupdf.readthedocs.io/)

