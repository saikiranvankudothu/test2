# errors/exceptions.py

class DocumentProcessingError(Exception):
    """Raised when document extraction or OCR fails"""


class RAGIndexingError(Exception):
    """Raised when RAG indexing fails"""


class LLMServiceError(Exception):
    """Raised when LLM response generation fails"""
