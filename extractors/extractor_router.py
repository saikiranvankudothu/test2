# extractors/extractor_router.py
import fitz  # PyMuPDF
from extractors.text_pdf_extractor import TextPDFExtractor
from extractors.scanned_pdf_extractor import ScannedPDFExtractor

class ExtractorRouter:

    def __init__(self):
        self.text_extractor = TextPDFExtractor()
        self.ocr_extractor = ScannedPDFExtractor()

    def is_scanned_pdf(self, pdf_path: str) -> bool:
        doc = fitz.open(pdf_path)
        for page in doc:
            if page.get_text().strip():
                return False
        return True

    def extract(self, pdf_path: str) -> dict:
        if self.is_scanned_pdf(pdf_path):
            return self.ocr_extractor.extract(pdf_path)
        return self.text_extractor.extract(pdf_path)
