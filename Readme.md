# 📄 Chat with PDF

**Chat with your PDF documents** easily using local embeddings and powerful LLMs like OpenAI's GPT models.

Upload any PDF and ask natural language questions about its content — powered by semantic search and AI.

---

## 🚀 Features

- 📚 Extract and understand PDF content
- 🔍 Embedding-based semantic search (local and efficient)
- 🤖 Query PDFs using OpenAI GPT models (or pluggable LLMs)
- 🛠️ Lightweight and fast, no heavy server needed
- 🔒 Fully local processing (except LLM call)

---

## 🛠️ Installation

```bash
pip install chat-with-pdf
```

Or, if you are using Poetry:

```bash
poetry add chat-with-pdf
```

---

## ✨ Quickstart Example

```python
from chat_with_pdf import PDFChat

# Initialize with your PDF file and OpenAI API key
chat = PDFChat('path/to/your/document.pdf', openai_api_key='your-openai-api-key')

# Ask questions
response = chat.ask("Summarize the introduction section.")
print(response)
```

---

## 📦 Requirements

- Python >= 3.8
- OpenAI API Key (for generation)
- Internet connection (for LLM calls)

**Major dependencies:**
- PyMuPDF
- sentence-transformers
- scikit-learn
- numpy
- openai
- torch (for sentence-transformers)

---

## 🧹 How It Works

1. 📄 Extracts text from the uploaded PDF using PyMuPDF.
2. 🔗 Splits text into manageable chunks.
3. 🧬 Creates semantic embeddings of the chunks using MiniLM or compatible models.
4. 🔍 Retrieves the most relevant chunks based on your question.
5. 🤖 Uses an LLM to generate a natural answer based on the relevant document pieces.

---

## 📈 Roadmap

- [x] MVP: Chat with PDF via OpenAI
- [ ] Local LLM support (for fully offline usage)
- [ ] Multi-file support (chat with multiple PDFs)
- [ ] Advanced chunking (by headings, semantic structure)
- [ ] CLI Tool for terminal use
- [ ] Django API wrapper (for web apps)

---

## 🤝 Contributing

Pull requests are welcome!
For major changes, please open an issue first to discuss what you would like to change.

### To run locally:

```bash
git clone https://github.com/yourusername/chat-with-pdf.git
cd chat-with-pdf
poetry install
poetry shell
pytest
```

---

## 📝 License

This project is licensed under the [MIT License](LICENSE).

---

## 🌟 Acknowledgements

- [OpenAI](https://openai.com/)
- [HuggingFace Sentence Transformers](https://www.sbert.net/)
- [PyMuPDF](https://pymupdf.readthedocs.io/)

