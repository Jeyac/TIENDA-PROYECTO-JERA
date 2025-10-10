from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from funcionalidades.rag.domain.entities.documento_entity import Documento


class DocumentoRepository(ABC):
    @abstractmethod
    def agregar(self, documento: Documento) -> Documento:
        raise NotImplementedError

    @abstractmethod
    def listar(self) -> List[Documento]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, documento_id: int) -> Optional[Documento]:
        raise NotImplementedError

    @abstractmethod
    def modificar(self, documento_id: int, documento: Documento) -> Documento:
        raise NotImplementedError

    @abstractmethod
    def eliminar(self, documento_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def upsert_embedding(self, documento_id: int, chunk: str, vector: list) -> None:
        raise NotImplementedError

    @abstractmethod
    def buscar_similares(self, vector: list, top_k: int = 3) -> List[Tuple[Documento, float, str]]:
        """Devuelve lista de (documento, score, chunk)"""
        raise NotImplementedError






