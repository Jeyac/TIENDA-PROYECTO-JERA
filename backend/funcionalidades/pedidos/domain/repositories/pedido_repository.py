from abc import ABC, abstractmethod
from typing import List, Optional

from funcionalidades.pedidos.domain.entities.pedido_entity import Pedido


class PedidoRepository(ABC):
    @abstractmethod
    def agregar(self, pedido: Pedido) -> Pedido:
        raise NotImplementedError

    @abstractmethod
    def listar(self) -> List[Pedido]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, pedido_id: int) -> Optional[Pedido]:
        raise NotImplementedError

    @abstractmethod
    def modificar(self, pedido_id: int, pedido: Pedido) -> Pedido:
        raise NotImplementedError

    @abstractmethod
    def eliminar(self, pedido_id: int) -> None:
        raise NotImplementedError










