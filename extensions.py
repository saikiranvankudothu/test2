# extensions.py
from services.document_service import DocumentService
from services.rag_service import RAGService
from services.llm_service import LLMService
from ai_engine.groq_llm import GroqClient
from ai_engine.rag_engine import RAGEngine

def init_services(app):
    """
    Initialize and wire all long-lived services to the Flask app.
    """

    # Create Groq client
    groq_client = GroqClient(
        api_key=app.config["GROQ_API_KEY"],
        model=app.config["GROQ_MODEL"]
    )

    # Initialize LLM service FIRST
    llm_service = LLMService(groq_client)

    # Initialize RAG engine
    rag_engine = RAGEngine(
        embed_model_name=app.config.get("EMBED_MODEL", "thenlper/gte-base"),
        persist_dir=app.config.get("CHROMA_DIR", "chroma_db")
    )

    # Initialize RAG service WITH llm_service
    rag_service = RAGService(rag_engine, llm_service)

    # Attach to app
    app.document_service = DocumentService()
    app.llm_service = llm_service
    app.rag_service = rag_service

