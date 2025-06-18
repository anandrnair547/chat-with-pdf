"""
Example script demonstrating how to use the `chat-with-pdf` SDK.

Usage:
    python example.py --type file --source examples/sample.pdf
    python example.py --type file --source examples/sample.docx
    python example.py --type file --source examples/sample.png
    python example.py --type url --source https://example.com/test.pdf
    python example.py --type bytes --source examples/sample.pdf

Before running:
    1. Create a .env file in the project root with:
        OPENAI_API_KEY=your_openai_api_key
        OPENAI_MODEL=gpt-4
        LLM_PROVIDER=openai
        DEFAULT_CHUNK_SIZE=500
        EMBEDDING_MODEL=all-MiniLM-L6-v2
        TOP_K_RETRIEVAL=5

    2. Install dependencies:
        pip install chat-with-pdf
        pip install pytesseract
        # On macOS:
        brew install tesseract
        # On Ubuntu:
        sudo apt-get install tesseract-ocr
"""

import argparse
from chat_with_pdf import DocumentChat


def get_file_type(filename):
    """Determine file type from extension."""
    ext = filename.lower().split(".")[-1]
    if ext == "pdf":
        return "pdf"
    elif ext == "docx":
        return "docx"
    elif ext in ["png", "jpg", "jpeg"]:
        return ext
    else:
        raise ValueError(f"Unsupported file type: {ext}")


def main():
    parser = argparse.ArgumentParser(
        description="Chat with documents (PDF, DOCX, PNG, JPEG) via file path, URL, or bytes"
    )
    parser.add_argument(
        "--type",
        choices=["file", "url", "bytes"],
        required=True,
        help="Type of document source: file, url, or bytes",
    )
    parser.add_argument(
        "--source",
        required=True,
        help="Path to local file or URL or path for bytes mode",
    )
    args = parser.parse_args()

    # Determine file type if it's a local file
    file_type = None
    if args.type == "file":
        file_type = get_file_type(args.source)

    # Initialize DocumentChat based on source type
    if args.type == "file":
        print(f"Using local file mode ({file_type})")
        chat = DocumentChat(args.source, file_type=file_type)
    elif args.type == "url":
        print("Using URL mode")
        chat = DocumentChat(args.source)
    elif args.type == "bytes":
        print("Using bytes mode")
        with open(args.source, "rb") as f:
            data = f.read()
        chat = DocumentChat(data)
    else:
        raise ValueError("Unknown type")

    # Interactive chat loop
    print("\nChat with your document (type 'exit' to quit)")
    print("----------------------------------------")
    while True:
        query = input("\nEnter your question: ")
        if query.lower() == "exit":
            break

        response = chat.ask(query)
        print("\nResponse:")
        print(response)

# python example/example.py --type file --source example/file_1.pdf
if __name__ == "__main__":
    main()
