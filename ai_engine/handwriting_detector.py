import torch
from torchvision import transforms
from PIL import Image
from transformers import AutoModelForImageClassification, AutoFeatureExtractor

class HandwritingDetector:
    """
    Predicts whether a page contains PRINTED text or HANDWRITTEN text.
    Model: microsoft/dit-base-finetuned-handwritten
    """

    def __init__(self, model_name="microsoft/dit-base-finetuned-handwritten"):
        print("[HandwritingDetector] Initializing handwriting classifier…")

        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.extractor = AutoFeatureExtractor.from_pretrained(model_name)
        self.model = AutoModelForImageClassification.from_pretrained(model_name).to(self.device)

        # label map from HF
        self.id2label = self.model.config.id2label

    def predict(self, image: Image.Image):
        """
        Returns:
            'handwritten' OR 'printed'
        """

        img_tensor = self.extractor(images=image, return_tensors="pt").pixel_values.to(self.device)

        with torch.no_grad():
            outputs = self.model(img_tensor)
            logits = outputs.logits
            pred_id = logits.argmax(dim=1).item()
            label = self.id2label[pred_id]

        # HF labels: handwriting / printed
        return label.lower()
