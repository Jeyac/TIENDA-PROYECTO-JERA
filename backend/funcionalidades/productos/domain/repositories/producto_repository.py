from abc import ABC, abstractmethod
from typing import List, Optional

from funcionalidades.productos.domain.entities.producto_entity import Producto


class ProductoRepository(ABC):
    @abstractmethod
    def agregar(self, producto: Producto) -> Producto:
        raise NotImplementedError

    @abstractmethod
    def listar(self) -> List[Producto]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, producto_id: int) -> Optional[Producto]:
        raise NotImplementedError

    @abstractmethod
    def modificar(self, producto_id: int, producto: Producto) -> Producto:
        raise NotImplementedError

    @abstractmethod
    def eliminar(self, producto_id: int) -> None:
        raise NotImplementedError





