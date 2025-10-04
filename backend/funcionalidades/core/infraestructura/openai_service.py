import os
from typing import List

from openai import OpenAI


class OpenAIService:
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        try:
            # Usar constructor por defecto; toma la key desde el entorno.
            # Evita problemas con parámetros no soportados (p.ej. proxies).
            self.client = OpenAI() if api_key else None
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


