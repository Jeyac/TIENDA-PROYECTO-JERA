from abc import ABC, abstractmethod
from typing import List, Optional

from funcionalidades.categorias.domain.entities.categoria_entity import Categoria


class CategoriaRepository(ABC):
    @abstractmethod
    def agregar(self, categoria: Categoria) -> Categoria:
        raise NotImplementedError

    @abstractmethod
    def listar(self) -> List[Categoria]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, categoria_id: int) -> Optional[Categoria]:
        raise NotImplementedError

    @abstractmethod
    def modificar(self, categoria_id: int, categoria: Categoria) -> Categoria:
        raise NotImplementedError

    @abstractmethod
    def eliminar(self, categoria_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_by_nombre(self, nombre: str) -> Optional[Categoria]:
        raise NotImplementedError