import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- API KEYS ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing in .env file! Please add it.")

# --- PATHS ---
# Base directory (contra-rag folder)
BASE_DIR = Path(__file__).resolve().parent.parent

# Data paths
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
CHROMA_DB_DIR = PROCESSED_DATA_DIR / "chroma_db"

# Models path
MODELS_DIR = BASE_DIR / "models"

# Create folders automatically if they don't exist
for path in [RAW_DATA_DIR, PROCESSED_DATA_DIR, CHROMA_DB_DIR, MODELS_DIR]:
    path.mkdir(parents=True, exist_ok=True)

# --- MODEL SETTINGS ---
# Groq Model (Llama 3 70B is fast and free)
GROQ_MODEL_NAME = "openai/gpt-oss-120b"  

# HuggingFace Embedding Model (for RAG)
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"