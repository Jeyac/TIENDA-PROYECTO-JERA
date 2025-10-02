from typing import List

from funcionalidades.pedidos.domain.entities.pedido_entity import Pedido
from funcionalidades.pedidos.domain.repositories.pedido_repository import PedidoRepository


class ListarPedidoseSUseCase:
    def __init__(self, repo: PedidoRepository):
        self.repo = repo

    def ejecutar(self) -> List[Pedido]:
        return self.repo.listar()


