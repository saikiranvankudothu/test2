# ai_engine/groq_llm.py
from groq import Groq

class GroqClient:
    def __init__(self, api_key: str, model: str):
        self.client = Groq(api_key=api_key)
        self.model = model

    def complete(self, prompt, max_tokens, temperature):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message.content
class LLMService:
    def __init__(self, groq_client: GroqClient):
        self.client = groq_client
