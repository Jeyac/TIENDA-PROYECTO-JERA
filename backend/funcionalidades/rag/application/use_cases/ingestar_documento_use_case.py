from typing import List

from funcionalidades.rag.domain.entities.documento_entity import Documento
from funcionalidades.rag.domain.repositories.documento_repository import DocumentoRepository


class IngestarDocumentoUseCase:
    def __init__(self, repo: DocumentoRepository, embedder):
        self.repo = repo
        self.embedder = embedder

    def _chunk(self, texto: str, max_len: int = 500) -> List[str]:
        chunks = []
        t = texto.strip()
        while t:
            chunks.append(t[:max_len])
            t = t[max_len:]
        return chunks

    def ejecutar(self, titulo: str, contenido: str) -> Documento:
        d = Documento(id=None, titulo=titulo, contenido=contenido)
        d = self.repo.agregar(d)
        for ch in self._chunk(contenido):
            vector = self.embedder.embed(ch)
            self.repo.upsert_embedding(d.id, ch, vector)
        return d


