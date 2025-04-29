# 📄 Chat with PDF

[![PyPI version](https://badge.fury.io/py/chat-with-pdf.svg)](https://badge.fury.io/py/chat-with-pdf)
[![Build Status](https://github.com/anandrnair547/chat-with-pdf/actions/workflows/ci.yml/badge.svg)](https://github.com/anandrnair547/chat-with-pdf/actions)

Chat with your PDF documents easily using local embeddings and powerful LLMs through a unified SDK.
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

1. **Set your credentials** and optionally choose a model/provider:

```bash
# Default provider key
export OPENAI_API_KEY="sk-your-openai-key"

# The model for the provider
export OPENAI_MODEL="gpt-4"

# Switch to another provider (e.g., perplexity, openai or deepseek)
export LLM_PROVIDER="perplexity"

```

2. **Use the SDK** to chat with any PDF:

```python
from chat_with_pdf import PDFChat

# Local PDF file
chat = PDFChat("path/to/your/document.pdf")
print(chat.ask("Summarize the introduction section."))

# Remote URL
chat = PDFChat("https://example.com/sample.pdf")
print(chat.ask("What is the main point of this document?"))

# PDF in memory
with open("path/to/your/document.pdf", "rb") as f:
    data = f.read()
chat = PDFChat(data)
print(chat.ask("Give me a brief overview."))
```

---

## ⚙️ Configuration Options

Configure via **environment variables** (in order of precedence):

| Variable             | Purpose                                              | Default            |
| :------------------- | :--------------------------------------------------- | :----------------- |
| `LLM_PROVIDER`       | Provider to use (`openai`, `perplexity`, `deepseek`) | `openai`           |
| `OPENAI_API_KEY`     | Your OpenAI API key                                  | —                  |
| `OPENAI_MODEL`       | GPT model name (used for all providers)              | `gpt-3.5-turbo`    |
| `EMBEDDING_MODEL`    | Embedding model                                      | `all-MiniLM-L6-v2` |
| `DEFAULT_CHUNK_SIZE` | Characters per text chunk                            | `500`              |
| `TOP_K_RETRIEVAL`    | Number of chunks to retrieve per query               | `5`                |

> 💡 For local development, you can also create a `.env` file with these variables and the SDK will load it automatically.

--------------------- | :------------------------------------------------ | :------------------------ |
| `LLM_PROVIDER`         | Provider to use (`openai`, `perplexity`, `deepseek`) | `openai`                  |
| `OPENAI_API_KEY`       | Your OpenAI API key                               | —                         |
| `OPENAI_MODEL`         | GPT model name (OpenAI)                           | `gpt-3.5-turbo`           |
| `PERPLEXITY_API_KEY`   | Your Perplexity API key                           | —                         |
| `PERPLEXITY_MODEL`     | Model name (Perplexity)                           | `perplexity-v1`           |
| `DEEPSEEK_API_KEY`     | Your DeepSeek API key                             | —                         |
| `DEEPSEEK_MODEL`       | Model name (DeepSeek)                             | `deepseek-v1`             |
| `EMBEDDING_MODEL`      | Embedding model                                  | `all-MiniLM-L6-v2`        |
| `DEFAULT_CHUNK_SIZE`   | Characters per text chunk                         | `500`                     |
| `TOP_K_RETRIEVAL`      | Number of chunks to retrieve per query            | `5`                       |

> 💡 For local development, you can also create a `.env` file with these variables and the SDK will load it automatically.

---

## 🔥 Advanced Usage

Override provider/model at runtime:

```python
from chat_with_pdf import PDFChat

# Use GPT-4 on OpenAI
chat = PDFChat("doc.pdf")
print(chat.ask("What are the key findings?", provider="openai", model="gpt-4"))

# Use DeepSeek
print(chat.ask("Summarize", provider="deepseek"))
```

---

## 📝 License

This project is licensed under the [MIT License](LICENSE).

---

## 🌟 Acknowledgements

- [OpenAI](https://openai.com/)
- [HuggingFace Sentence Transformers](https://www.sbert.net/)
- [PyMuPDF](https://pymupdf.readthedocs.io/)
