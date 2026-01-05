# extractors/text_pdf_extractor.py
from extractors.base import BaseExtractor
from ai_engine.docling_extractor import DoclingExtractor

class TextPDFExtractor(BaseExtractor):

    def __init__(self):
        self.extractor = DoclingExtractor()

    def extract(self, pdf_path: str) -> dict:
        # Docling handles text PDFs well
        return self.extractor.extract(pdf_path)
