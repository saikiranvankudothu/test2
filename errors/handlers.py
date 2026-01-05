# errors/handlers.py
from flask import jsonify
from errors.exceptions import (
    DocumentProcessingError,
    RAGIndexingError,
    LLMServiceError
)
from utils.logger import logger

def register_error_handlers(app):

    @app.errorhandler(DocumentProcessingError)
    def handle_doc_error(e):
        logger.error(f"Document error: {e}")
        return jsonify({"error": "Document processing failed"}), 500

    @app.errorhandler(RAGIndexingError)
    def handle_rag_error(e):
        logger.error(f"RAG error: {e}")
        return jsonify({"error": "Document indexing failed"}), 500

    @app.errorhandler(LLMServiceError)
    def handle_llm_error(e):
        logger.error(f"LLM error: {e}")
        return jsonify({"error": "AI generation failed"}), 500

    @app.errorhandler(404)
    def not_found(_):
        return jsonify({"error": "Route not found"}), 404

    @app.errorhandler(500)
    def internal_error(_):
        return jsonify({"error": "Internal server error"}), 500
