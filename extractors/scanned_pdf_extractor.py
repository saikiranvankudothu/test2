# extractors/scanned_pdf_extractor.py
from extractors.base import BaseExtractor
from ai_engine.hybrid_ocr import HybridOCR
import json
import os

class ScannedPDFExtractor(BaseExtractor):

    def __init__(self):
        self.ocr = HybridOCR()

    def extract(self, pdf_path: str) -> dict:
        text = self.ocr.extract_text(pdf_path)

        json_path = pdf_path.replace(".pdf", "_ocr.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump({"text": text}, f, ensure_ascii=False, indent=2)

        return {
            "text": text,
            "json_path": json_path
        }
