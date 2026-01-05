# ai_engine/rag_engine.py
import uuid
from ai_engine.chunker import prepare_chunks_from_docling
from ai_engine.embedder import GTEEmbedder
from ai_engine.vector_store import ChromaStore
from ai_engine.bm25_store import BM25Store

class RAGEngine:
    def __init__(self, embed_model_name="thenlper/gte-base", persist_dir="chroma_db"):
        self.embedder = GTEEmbedder(model_name=embed_model_name)
        self.store = ChromaStore(persist_dir=persist_dir)
        self.store.create_collection("docs")
        self.bm25 = BM25Store()

    def index_document(self, doc_json: dict, doc_id: str = None):
        doc_id = doc_id or str(uuid.uuid4())
        chunks = prepare_chunks_from_docling(doc_json)
        texts = [c["text"] for c in chunks]
        ids = [f"{doc_id}_{i}" for i in range(len(texts))]
        embeddings = self.embedder.embed_texts(texts)
        metadatas = [{"source_doc": doc_id, "chunk_id": ids[i]} for i in range(len(ids))]
        self.store.add_documents(ids, texts, embeddings, metadatas)
        self.bm25.add_documents(ids, texts)
        return {"doc_id": doc_id, "n_chunks": len(texts)}

    def retrieve(self, query: str, k: int = 5):
        # ---- Dense retrieval ----
        q_embed = self.embedder.embed_texts([query])[0]
        dense_res = self.store.query(q_embed, n_results=k)

        dense_docs = {}
        for text, dist, cid in zip(
            dense_res["documents"][0],
            dense_res["distances"][0],
            dense_res["ids"][0]
        ):
            dense_docs[cid] = {
                "text": text,
                "score": 1 - dist   # convert distance to score
            }

        # Debug: Print Dense IDs
        print("Dense IDs:", list(dense_docs.keys()))

        # ---- Sparse (BM25) retrieval ----
        sparse_ids = self.bm25.query(query, k=k)
        
        # Debug: Print BM25 IDs
        print("BM25 IDs:", sparse_ids)

        # ---- Fusion ----
        final_docs = {}

        for cid, doc in dense_docs.items():
            final_docs[cid] = doc

        for cid in sparse_ids:
            if cid in final_docs:
                final_docs[cid]["score"] += 1.0
            else:
                final_docs[cid] = {
                    "text": None,
                    "score": 1.0
                }

        # ---- Sort by score ----
        ranked = sorted(
            final_docs.items(),
            key=lambda x: x[1]["score"],
            reverse=True
        )
        results = []
        for cid, data in ranked[:k]:
            if data["text"]:
                results.append({
                    "chunk_id": cid,
                    "text": data["text"]
                })

        return results


    def get_context_for_query(self, query: str, k: int = 5):
        docs = self.retrieve(query, k)

        context_blocks = []
        evidence = []

        for d in docs:
            context_blocks.append(d["text"])
            evidence.append(d["chunk_id"])

        return {
            "context": "\n\n".join(context_blocks),
            "evidence": evidence
        }

