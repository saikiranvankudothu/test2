# services/document_service.py
from extractors.extractor_router import ExtractorRouter
import json

class DocumentService:

    def __init__(self):
        self.router = ExtractorRouter()

    def process_pdf(self, pdf_path: str) -> dict:
        result = self.router.extract(pdf_path)

        with open(result["json_path"], "r", encoding="utf-8") as f:
            doc_json = json.load(f)

        return {
            "text": result["text"],
            "json": doc_json
        }
