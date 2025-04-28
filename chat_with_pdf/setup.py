from setuptools import setup, find_packages

setup(
    name="chat-with-pdf",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "PyMuPDF",
        "sentence-transformers",
        "scikit-learn",
        "numpy",
        "openai",
    ],
    description="Chat with your PDFs using local embedding search and OpenAI.",
    author="Anand R Nair",
    license="MIT",
)
