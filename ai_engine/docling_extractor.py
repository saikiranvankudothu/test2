# docling_extractor.py
import os
import json
import fitz  # PyMuPDF
from docling.document_converter import DocumentConverter
from ai_engine.hybrid_ocr import HybridOCR

class DoclingExtractor:
    def __init__(self, save_dir="outputs/structured"):
        self.save_dir = save_dir
        os.makedirs(self.save_dir, exist_ok=True)
        self.converter = DocumentConverter()
        self.ocr_engine = HybridOCR()

    # Detect if PDF contains selectable text
    def _is_text_pdf(self, pdf_path):
        try:
            doc = fitz.open(pdf_path)
            for page in doc:
                if len(page.get_text().strip()) > 10:
                    return True
            return False
        except:
            return False

    def extract(self, pdf_path):
        print("[Extractor] Checking PDF type…")

        if self._is_text_pdf(pdf_path):
            print("[Extractor] Text PDF → Using Docling")
            result = self.converter.convert(pdf_path)
            doc = result.document
            text = doc.export_to_text()
            markdown = doc.export_to_markdown()
            json_data = doc.export_to_dict()

        else:
            print("[Extractor] Scanned PDF → Using OCR")
            text = self.ocr_engine.extract_text(pdf_path)
            markdown = f"# OCR Extracted Document\n\n{text}"
            json_data = {"text": text}

        # Save JSON
        base = os.path.splitext(os.path.basename(pdf_path))[0]
        json_path = os.path.join(self.save_dir, f"{base}.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=2)

        return {
            "text": text,
            "markdown": markdown,
            "json_path": json_path
        }
