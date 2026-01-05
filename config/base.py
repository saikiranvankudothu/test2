# config/base.py
import os
# config/base.py
from dotenv import load_dotenv
load_dotenv()

class BaseConfig:
    # Core Flask
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-secret")

    # Paths
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")
    STRUCTURED_OUTPUT = os.getenv("STRUCTURED_OUTPUT", "outputs/structured")

    # Groq
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    # Server
    PORT = int(os.getenv("PORT", 5000))

    @classmethod
    def validate(cls):
        if not cls.GROQ_API_KEY:
            raise RuntimeError("GROQ_API_KEY must be set")
