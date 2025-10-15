from typing import List, Optional, Tuple

from funcionalidades.core.infraestructura.database import db
from funcionalidades.rag.domain.entities.documento_entity import Documento
from funcionalidades.rag.domain.repositories.documento_repository import DocumentoRepository
from funcionalidades.rag.infrastructure.documento_model import DocumentoModel, DocumentoChunkModel


def _to_entity(m: DocumentoModel) -> Documento:
    return Documento(id=m.id, titulo=m.titulo, contenido=m.contenido)


class DocumentoRepositoryImpl(DocumentoRepository):
    def agregar(self, documento: Documento) -> Documento:
        m = DocumentoModel(titulo=documento.titulo, contenido=documento.contenido)
        db.session.add(m)
        db.session.commit()
        return _to_entity(m)

    def listar(self) -> List[Documento]:
        return [_to_entity(m) for m in DocumentoModel.query.all()]

    def get_by_id(self, documento_id: int) -> Optional[Documento]:
        m = DocumentoModel.query.get(documento_id)
        return _to_entity(m) if m else None

    def modificar(self, documento_id: int, documento: Documento) -> Documento:
        m = DocumentoModel.query.get(documento_id)
        if not m:
            return None
        m.titulo = documento.titulo
        m.contenido = documento.contenido
        db.session.commit()
        return _to_entity(m)

    def eliminar(self, documento_id: int) -> None:
        m = DocumentoModel.query.get(documento_id)
        if m:
            db.session.delete(m)
            db.session.commit()

    def upsert_embedding(self, documento_id: int, chunk: str, vector: list) -> None:
        db.session.add(DocumentoChunkModel(documento_id=documento_id, texto=chunk, embedding=vector))
        db.session.commit()

    def buscar_similares(self, vector: list, top_k: int = 3) -> List[Tuple[Documento, float, str]]:
        # Similaridad coseno simple en Python (ineficiente pero suficiente para demo)
        import math

        def cosine(a, b):
            dot = sum(x*y for x, y in zip(a, b))
            na = math.sqrt(sum(x*x for x in a))
            nb = math.sqrt(sum(y*y for y in b))
            return dot / (na * nb + 1e-9)

        resultados = []
        for ch in DocumentoChunkModel.query.all():
            score = cosine(vector, ch.embedding)
            doc = DocumentoModel.query.get(ch.documento_id)
            resultados.append((_to_entity(doc), score, ch.texto))
        resultados.sort(key=lambda x: x[1], reverse=True)
        return resultados[:top_k]










