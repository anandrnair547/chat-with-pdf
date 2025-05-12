import os
from pathlib import Path
from dotenv import load_dotenv

# Get the base directory (where settings.py is located)
BASE_DIR = Path(__file__).resolve().parent.parent


def get_env_var(key, default=None, type_cast=str):
    """Get environment variable with type casting and force reload."""
    # Force reload .env file
    load_dotenv(BASE_DIR / ".env", override=True)
    value = os.getenv(key, default)
    if value is not None and type_cast is not None:
        try:
            return type_cast(value)
        except (ValueError, TypeError):
            return default
    return value


# Load environment variables with type casting
OPENAI_API_KEY = get_env_var("OPENAI_API_KEY", "")
DEFAULT_MODEL = get_env_var("OPENAI_MODEL")
LLM_PROVIDER = get_env_var("LLM_PROVIDER")
DEFAULT_CHUNK_SIZE = get_env_var("DEFAULT_CHUNK_SIZE", "500", int)
DEFAULT_EMBEDDING_MODEL = get_env_var("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
TOP_K_RETRIEVAL = get_env_var("TOP_K_RETRIEVAL", "5", int)
