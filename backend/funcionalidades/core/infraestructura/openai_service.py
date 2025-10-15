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

    def chat_with_functions(self, messages: List[dict], functions: List[dict], model: str = 'gpt-4o-mini') -> dict:
        """Chat con function calling"""
        if not self.client:
            return {'content': 'OpenAI API key no configurada.'}
        
        completion = self.client.chat.completions.create(
            model=model,
            messages=messages,
            functions=functions,
            function_call="auto",
            temperature=0.3,
        )
        
        message = completion.choices[0].message
        
        # Si hay function call, devolver la información completa
        if message.function_call:
            return {
                'function_call': {
                    'name': message.function_call.name,
                    'arguments': message.function_call.arguments
                }
            }
        else:
            # Respuesta normal
            return {'content': message.content}


