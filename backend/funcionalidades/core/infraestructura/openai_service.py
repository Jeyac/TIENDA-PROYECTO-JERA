import os
from typing import List

from openai import OpenAI


class OpenAIService:
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        try:
            # No fallamos si no hay API key; el caller decidirá
            self.client = OpenAI(api_key=api_key) if api_key else None
        except Exception as e:
            print(f"Warning: OpenAI client initialization failed: {e}")
            self.client = None

    def chat(self, messages: List[dict], model: str = 'gpt-4o-mini') -> str:
        if not self.client:
            return 'OpenAI API key no configurada.'
        completion = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.3,
        )
        return completion.choices[0].message.content


