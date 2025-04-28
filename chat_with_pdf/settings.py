import os
from dotenv import load_dotenv

load_dotenv()

# Load API Key from environment variable or default to empty
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Default GPT model to use
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

# Default chunk size for PDF splitting
DEFAULT_CHUNK_SIZE = int(os.getenv("DEFAULT_CHUNK_SIZE", "500"))

# Embedding model name (for sentence-transformers)
DEFAULT_EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

# Number of similar chunks to retrieve
TOP_K_RETRIEVAL = int(os.getenv("TOP_K_RETRIEVAL", "5"))
