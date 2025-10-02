from typing import List


class RAGService:
    def __init__(self):
        # Stub: aquí iría carga de embeddings/índices
        self.docs = []

    def retrieve(self, query: str, k: int = 3) -> List[str]:
        # Stub simple: devolver documentación simulada
        return [
            'Politicas de envío: Envio en 24-48h.',
            'Devoluciones: 30 días con ticket.',
            'Soporte: Lunes a Viernes 9-18h.'
        ][:k]


