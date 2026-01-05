# ai_engine/embedder.py
from typing import List
import torch
from transformers import AutoTokenizer, AutoModel
import numpy as np

class GTEEmbedder:
    """
    Embeds text using a model like 'thenlper/gte-base'.
    CPU-friendly but may be slow. You can change model_name to any sentence transformer.
    """
    def __init__(self, model_name: str = "thenlper/gte-base", device: str = None):
        self.model_name = model_name
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
        self.model = AutoModel.from_pretrained(model_name).to(self.device)
        self.model.eval()

    def _mean_pooling(self, token_embeddings, attention_mask):
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
        sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        return sum_embeddings / sum_mask

    @torch.no_grad()
    def embed_texts(self, texts: List[str], batch_size: int = 8) -> List[List[float]]:
        embeddings = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            encoded = self.tokenizer(batch, padding=True, truncation=True, max_length=512, return_tensors="pt")
            input_ids = encoded["input_ids"].to(self.device)
            attention_mask = encoded["attention_mask"].to(self.device)
            out = self.model(input_ids=input_ids, attention_mask=attention_mask, return_dict=True)
            token_embeds = out.last_hidden_state
            pooled = self._mean_pooling(token_embeds, attention_mask)
            pooled = torch.nn.functional.normalize(pooled, p=2, dim=1)
            embeddings.extend(pooled.cpu().numpy().tolist())
        return embeddings
