from typing import List

from funcionalidades.rag.domain.repositories.documento_repository import DocumentoRepository


class RecuperarContextoUseCase:
    def __init__(self, repo: DocumentoRepository, embedder):
        self.repo = repo
        self.embedder = embedder

    def ejecutar(self, query: str, top_k: int = 3) -> List[str]:
        vector = self.embedder.embed(query)
        resultados = self.repo.buscar_similares(vector, top_k=top_k)
        return [chunk for _doc, _score, chunk in resultados]










