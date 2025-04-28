"""
Example script demonstrating how to use the `chat-with-pdf` SDK.

Usage:
    python example_usage.py --type file --source examples/sample.pdf
    python example_usage.py --type url --source https://example.com/test.pdf
    python example_usage.py --type bytes --source examples/sample.pdf

Before running:
    pip install chat-with-pdf
    export OPENAI_API_KEY="your_openai_api_key"
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

    query = input("Enter your question: ")
    response = chat.ask(query)
    print("\n--- Response ---")
    print(response)

# python example/example_usage.py --type file --source examples/sample.pdf
if __name__ == "__main__":
    main()
