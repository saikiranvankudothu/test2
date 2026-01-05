# hybrid_ocr.py
import os
import re
import numpy as np
from pdf2image import convert_from_path
import easyocr
from PIL import Image
from ai_engine.trocr_ocr import TrOCREngine


class HybridOCR:
    def __init__(self, lang="en", dpi=300, save_dir="outputs/ocr", poppler_path=None):
        print("[HybridOCR] EasyOCR + TrOCR Initialized")

        self.easyocr = easyocr.Reader([lang], gpu=False)
        self.trocr = TrOCREngine()  # NEW: TrOCR engine

        self.dpi = dpi
        self.save_dir = save_dir
        self.poppler_path = poppler_path
        os.makedirs(save_dir, exist_ok=True)


    # Convert PDF → Images
    def _pdf_to_images(self, pdf_path):
        try:
            return convert_from_path(
                pdf_path,
                dpi=self.dpi,
                poppler_path=self.poppler_path
            )
        except Exception as e:
            print(f"[HybridOCR ERROR] PDF to image error: {e}")
            return []


    # EasyOCR extraction
    def _ocr_easy(self, image):
        try:
            arr = np.array(image)
            results = self.easyocr.readtext(arr)

            text = " ".join([item[1] for item in results])
            text = re.sub(r'\s+', ' ', text).strip()

            return text

        except Exception as e:
            print(f"[HybridOCR ERROR] EasyOCR error: {e}")
            return ""


    # TrOCR extraction
    def _ocr_trocr(self, image):
        try:
            return self.trocr.extract_text(image)
        except Exception as e:
            print(f"[HybridOCR ERROR] TrOCR error: {e}")
            return ""


    # Main pipeline
    def extract_text(self, pdf_path):
        pages = self._pdf_to_images(pdf_path)
        if not pages:
            return ""

        final_text = ""

        for i, page in enumerate(pages):
            print(f"[HybridOCR] Processing page {i+1}/{len(pages)}")

            # Step 1 — run EasyOCR
            easy_text = self._ocr_easy(page)

            # Step 2 — If EasyOCR result is too short → use TrOCR
            if len(easy_text.strip()) < 15:  # threshold for handwriting
                print("[HybridOCR] EasyOCR detected weak text → Switching to TrOCR")
                trocr_text = self._ocr_trocr(page)
                final_text += f"\n\n--- OCR Page {i+1} (TrOCR) ---\n{trocr_text}"
            else:
                final_text += f"\n\n--- OCR Page {i+1} (EasyOCR) ---\n{easy_text}"

        return final_text

































# # hybrid_ocr.py
# import os
# import re
# import numpy as np
# from pdf2image import convert_from_path
# import easyocr

# class HybridOCR:
#     def __init__(self, lang="en", dpi=300, save_dir="outputs/ocr", poppler_path=None):
#         print("[HybridOCR] EasyOCR Initialized")

#         # EasyOCR supports many languages: "en", "hi", "fr", "de", etc.
#         self.ocr = easyocr.Reader([lang], gpu=False)

#         self.dpi = dpi
#         self.save_dir = save_dir
#         self.poppler_path = poppler_path
#         os.makedirs(save_dir, exist_ok=True)

#     # Convert PDF → Images
#     def _pdf_to_images(self, pdf_path):
#         try:
#             return convert_from_path(
#                 pdf_path,
#                 dpi=self.dpi,
#                 poppler_path=self.poppler_path
#             )
#         except Exception as e:
#             print(f"[HybridOCR ERROR] PDF to image error: {e}")
#             return []

#     # Run OCR on a single image page
#     def _ocr_image(self, image):
#         try:
#             arr = np.array(image)

#             results = self.ocr.readtext(arr)

#             text = " ".join([item[1] for item in results])
#             text = re.sub(r'\s+', ' ', text).strip()

#             return text

#         except Exception as e:
#             print(f"[HybridOCR ERROR] OCR error: {e}")
#             return ""

#     # Main OCR pipeline
#     def extract_text(self, pdf_path):
#         pages = self._pdf_to_images(pdf_path)
#         if not pages:
#             return ""

#         final_text = ""

#         for i, page in enumerate(pages):
#             print(f"[HybridOCR] Processing page {i+1}/{len(pages)}")
#             page_text = self._ocr_image(page)
#             final_text += f"\n\n--- OCR Page {i+1} ---\n{page_text}"

#         return final_text
