from funcionalidades.core.exceptions import NotFoundError
from funcionalidades.pedidos.domain.entities.pedido_entity import Pedido
from funcionalidades.pedidos.domain.repositories.pedido_repository import PedidoRepository


class ObtenerPedidoUseCase:
    def __init__(self, repo: PedidoRepository):
        self.repo = repo

    def ejecutar(self, pedido_id: int) -> Pedido:
        p = self.repo.get_by_id(pedido_id)
        if not p:
            raise NotFoundError('Pedido no encontrado')
        return p


