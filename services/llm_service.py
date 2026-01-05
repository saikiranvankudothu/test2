from utils.prompt_loader import load_prompt
from errors.exceptions import LLMServiceError
from utils.logger import logger

class LLMService:

    def __init__(self, groq_client):
        self.client = groq_client

    def answer_question(self, context_data: dict, question: str):
        try:
            template = load_prompt("qa.txt")

            prompt = template.format(
                context=context_data["context"],
                question=question,
                evidence=", ".join(context_data["evidence"])
            )

            return self.client.complete(
                prompt=prompt,
                max_tokens=300,
                temperature=0.1
            )

        except Exception as e:
            raise LLMServiceError(str(e))


    def summarize(self, text: str) -> str:
        try:
            template = load_prompt("summary.txt")
            prompt = template.format(text=text)

            return self.client.complete(
                prompt=prompt,
                max_tokens=400,
                temperature=0.2
            )
        except Exception as e:
            logger.exception("Summary prompt failed")
            raise LLMServiceError(str(e))

    def generate_mindmap(self, text: str) -> str:
        try:
            template = load_prompt("mindmap.txt")
            prompt = template.format(text=text)

            return self.client.complete(
                prompt=prompt,
                max_tokens=800,
                temperature=0.2
            )
        except Exception as e:
            logger.exception("Mindmap prompt failed")
            raise LLMServiceError(str(e))
        
    def verify_claim(self, claim: str, context: str):
        template = load_prompt("verify.txt")

        prompt = template.format(
            answer=claim,
            context=context
        )

        result = self.client.complete(
            prompt=prompt,
            max_tokens=150,
            temperature=0.0
        )
        print("----- VERIFY PROMPT OUTPUT -----")
        print(result)
        print("--------------------------------")

        result = result.strip().upper()

        if result == "SUPPORTED":
            return True

        return False



