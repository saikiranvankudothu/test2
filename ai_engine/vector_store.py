# ai_engine/vector_store.py
import os
import chromadb

class ChromaStore:
    def __init__(self, persist_dir: str = "chroma_db"):
        os.makedirs(persist_dir, exist_ok=True)
        # Use PersistentClient for local persistence
        try:
            self.client = chromadb.PersistentClient(path=persist_dir)
        except Exception:
            # fallback to legacy client if PersistentClient isn't available
            self.client = chromadb.Client()
        self.collection = None

    def create_collection(self, name: str = "docs"):
        # get or create collection
        self.collection = self.client.get_or_create_collection(
            name=name,
            metadata={"hnsw:space": "cosine"}
        )

    def add_documents(self, ids, texts, embeddings, metadatas=None):
        if self.collection is None:
            self.create_collection()
        self.collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas
        )

    def query(self, query_embedding, n_results=5):
        if self.collection is None:
            self.create_collection()
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=["documents", "distances", "metadatas"]
        )

