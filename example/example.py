"""
Example script demonstrating how to use the `chat-with-pdf` SDK.

Usage:
    python example.py --type file --source examples/sample.pdf
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
"""

import argparse
from chat_with_pdf import PDFChat


def main():
    parser = argparse.ArgumentParser(
        description="Chat with a PDF via file path, URL, or bytes"
    )
    parser.add_argument(
        "--type",
        choices=["file", "url", "bytes"],
        required=True,
        help="Type of PDF source: file, url, or bytes",
    )
    parser.add_argument(
        "--source",
        required=True,
        help="Path to local file or URL or path for bytes mode",
    )
    args = parser.parse_args()

    # Initialize PDFChat based on source type
    if args.type == "file":
        print("Using local file mode")
        chat = PDFChat(args.source)
    elif args.type == "url":
        print("Using URL mode")
        chat = PDFChat(args.source)
    elif args.type == "bytes":
        print("Using bytes mode")
        with open(args.source, "rb") as f:
            data = f.read()
        chat = PDFChat(data)
    else:
        raise ValueError("Unknown type")

    # Interactive chat loop
    print("\nChat with your PDF (type 'exit' to quit)")
    print("----------------------------------------")
    while True:
        query = input("\nEnter your question: ")
        if query.lower() == "exit":
            break

        response = chat.ask(query)
        print("\nResponse:")
        print(response)


if __name__ == "__main__":
    main()
