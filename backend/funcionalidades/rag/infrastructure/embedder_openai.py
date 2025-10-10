import os
from typing import List

from openai import OpenAI


class OpenAIEmbedder:
    def __init__(self, model: str = 'text-embedding-3-small'):
        api_key = os.getenv('OPENAI_API_KEY')
        try:
            # Solo inicializar si hay API key
            if api_key:
                self.client = OpenAI(api_key=api_key)
            else:
                self.client = None
        except Exception as e:
            print(f"Warning: OpenAI client initialization failed: {e}")
            self.client = None
        self.model = model

    def embed(self, text: str) -> List[float]:
        if not self.client:
            # Fallback determinista para demo sin API key
            import hashlib
            h = hashlib.sha256(text.encode('utf-8')).digest()
            return [x/255.0 for x in h[:64]]
        res = self.client.embeddings.create(model=self.model, input=text)
        return res.data[0].embedding


