# ai_engine/chunker.py
import re
from typing import List, Dict

def clean_text(t: str) -> str:
    if not isinstance(t, str):
        return ""
    # Basic cleanup
    t = re.sub(r"'[^']+':\s*[^,{}\[\]]+", " ", t)  # remove simple metadata-like patterns
    t = re.sub(r"\[[^\]]*\]", " ", t)
    t = re.sub(r"[{}\[\]']", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t

def chunk_text(text: str, chunk_size: int = 250, overlap: int = 50) -> List[Dict]:
    words = text.split()
    if not words:
        return []
    chunks = []
    i = 0
    idx = 0
    while i < len(words):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append({"id": f"chunk_{idx}", "text": chunk})
        idx += 1
        i += chunk_size - overlap
    return chunks

def prepare_chunks_from_docling(doc_json: dict, chunk_size:int=250, overlap:int=50):
    extracted = []
    # Prefer elements[] if available (docling output)
    elements = doc_json.get("elements", [])
    for el in elements:
        txt = el.get("text", "")
        txt = clean_text(txt)
        if txt and len(txt) > 5:
            extracted.append(txt)
    # fallbacks
    if not extracted and isinstance(doc_json.get("text"), str):
        extracted.append(clean_text(doc_json["text"]))
    if not extracted and isinstance(doc_json.get("markdown"), str):
        extracted.append(clean_text(doc_json["markdown"]))
    if not extracted:
        extracted.append(clean_text(str(doc_json)))
    merged = "\n".join(extracted)
    return chunk_text(merged, chunk_size=chunk_size, overlap=overlap)
