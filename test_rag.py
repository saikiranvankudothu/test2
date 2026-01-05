# tests/test_rag.py
# import json
# from ai_engine.rag_engine import RAGEngine

# def load_doc(path):
#     with open(path, "r", encoding="utf-8") as f:
#         return json.load(f)

# if __name__ == "__main__":
#     # adjust path to one JSON you have from outputs/structured/
#     path = "outputs/structured/sample.json"
#     doc = load_doc(path)
#     rag = RAGEngine()
#     info = rag.index_document(doc, doc_id="sample_doc")
#     print("Indexed:", info)
#     query = "Summarize the main point"
#     context = rag.get_context_for_query(query, k=4)
#     print("Retrieved context:\n", context[:1000])


# tests/test_groq.py
from ai_engine.groq_llm import groq_completion

def main():
    prompt = "what are the steps in business analystics?"
    print("Sending prompt to Groq (short test)...")
    out = groq_completion(prompt, max_tokens=120, temperature=0.0)
    print("== Groq Response ==\n")
    print(out)

if __name__ == "__main__":
    main()

