import torch
from PIL import Image
from transformers import VisionEncoderDecoderModel, TrOCRProcessor

class TrOCREngine:
    def __init__(self, model_name="microsoft/trocr-base-handwritten"):
        print("[TrOCR] Initializing model...")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.processor = TrOCRProcessor.from_pretrained(model_name)
        self.model = VisionEncoderDecoderModel.from_pretrained(model_name).to(self.device)

    def extract_text(self, image):
        try:
            pixel_values = self.processor(image, return_tensors="pt").pixel_values.to(self.device)
            generated_ids = self.model.generate(pixel_values)
            text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            return text.strip()
        except Exception as e:
            print("[TrOCR ERROR]:", e)
            return ""
