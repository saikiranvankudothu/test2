# ai_engine/bm25_store.py

from rank_bm25 import BM25Okapi

class BM25Store:
    def __init__(self):
        self.texts = []
        self.ids = []
        self.bm25 = None

    def add_documents(self, ids, texts):
        """
        Store documents for keyword search
        """
        self.ids.extend(ids)
        self.texts.extend(texts)

        tokenized = [text.split() for text in self.texts]
        self.bm25 = BM25Okapi(tokenized)

    def query(self, query, k=5):
        """
        Return top-k document IDs based on keyword match
        """
        if not self.bm25:
            return []

        scores = self.bm25.get_scores(query.split())
        ranked = sorted(
            zip(self.ids, scores),
            key=lambda x: x[1],
            reverse=True
        )
        return [doc_id for doc_id, _ in ranked[:k]]
