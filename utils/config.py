import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
    DEFAULT_MODEL = os.getenv("DEFAULT_MODEL")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")