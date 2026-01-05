# services/rag_service.py
# services/rag_service.py

from utils.logger import logger
from errors.exceptions import RAGIndexingError


class RAGService:
    def __init__(self, rag_engine, llm_service):
        # IMPORTANT: store the INSTANCE, not the class
        self.rag = rag_engine
        self.llm = llm_service

    def index(self, doc_json: dict, doc_id: str):
        try:
            return self.rag.index_document(doc_json, doc_id)
        except Exception as e:
            logger.exception("RAG indexing failed")
            raise RAGIndexingError(str(e))

    def get_context(self, question, k=5):
        context_data = self.rag.get_context_for_query(question, k)

        # Ensure consistent structure for LLMService
        if isinstance(context_data, str):
            return {
                "context": context_data,
                "evidence": []
            }

        if "context" not in context_data:
            context_data["context"] = ""

        if "evidence" not in context_data:
            context_data["evidence"] = []

        return context_data

    def split_into_claims(self, answer: str):
        lines = answer.split("\n")
        claims = []

        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.lower().startswith("answer"):
                continue
            if line.startswith("-"):
                claims.append(line[1:].strip())
            else:
                claims.append(line)

        return claims

    def answer_question(self, question: str):
        # 1. Retrieve context
        context_data = self.get_context(question)

        # 2. Generate raw answer
        raw_answer = self.llm.answer_question(context_data, question)

        # 3. Split into claims
        claims = self.split_into_claims(raw_answer)

        verified_claims = []
        verification_log = []

        # 4. Verify each claim
        for claim in claims:
            is_supported = self.llm.verify_claim(
                claim=claim,
                context=context_data["context"]
            )

            verification_log.append({
                "claim": claim,
                "supported": is_supported
            })

            if is_supported:
                verified_claims.append(claim)

        # 5. Rebuild final answer
        if not verified_claims:
            final_answer = "The document does not support a confident answer."
        else:
            final_answer = "Answer:\n" + "\n".join(
                f"- {c}" for c in verified_claims
            )

        return {
            "answer": final_answer,
            "verification": verification_log
        }






# from ai_engine.rag_engine import RAGEngine
# from utils.logger import logger
# from errors.exceptions import RAGIndexingError

# class RAGService:
#     def __init__(self,RAGEngine, llm_service):
#         self.rag = RAGEngine
#         self.llm = llm_service

#     def index(self, doc_json: dict, doc_id: str):
#         return self.rag.index_document(doc_json, doc_id)

#     def get_context(self, question, k=5):
#         context_data = self.rag.get_context_for_query(question, k)

#         # Ensure consistent structure
#         if isinstance(context_data, str):
#             return {
#                 "context": context_data,
#                 "evidence": []
#             }

#         if "context" not in context_data:
#             return {
#                 "context": "",
#                 "evidence": []
#             }

#         if "evidence" not in context_data:
#             context_data["evidence"] = []

#         return context_data


#     def index(self, doc_json: dict, doc_id: str):
#         try:
#             return self.rag.index_document(doc_json, doc_id)
#         except Exception as e:
#             logger.exception("RAG indexing failed")
#             raise RAGIndexingError(str(e))
        
#     def split_into_claims(answer: str):
#         lines = answer.split("\n")
#         claims = []

#         for line in lines:
#             line = line.strip()
#             if not line:
#                 continue
#             if line.lower().startswith("answer"):
#                 continue
#             if line.startswith("-"):
#                 claims.append(line[1:].strip())
#             else:
#                 claims.append(line)

#         return claims
    
#     def answer_question(self, question):
#         # 1. Retrieve explainable context
#         context_data = self.get_context(question)

#         # 2. Generate raw answer
#         raw_answer = self.llm.answer_question(context_data, question)

#         # 3. Split into claims
#         claims = split_into_claims(raw_answer)

#         verified_claims = []
#         verification_log = []

#         # 4. Verify each claim
#         for claim in claims:
#             is_supported = self.llm.verify_claim(
#                 claim=claim,
#                 context=context_data["context"]
#             )

#             verification_log.append({
#                 "claim": claim,
#                 "supported": is_supported
#             })

#             if is_supported:
#                 verified_claims.append(claim)

#         # 5. Rebuild final answer
#         if not verified_claims:
#             final_answer = "The document does not support a confident answer."
#         else:
#             final_answer = "Answer:\n" + "\n".join(
#                 f"- {c}" for c in verified_claims
#             )

#         return {
#             "answer": final_answer,
#             "verification": verification_log
#         }
