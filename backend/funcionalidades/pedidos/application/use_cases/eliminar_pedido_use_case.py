from funcionalidades.core.exceptions import NotFoundError
from funcionalidades.pedidos.domain.repositories.pedido_repository import PedidoRepository


class EliminarPedidoUseCase:
    def __init__(self, repo: PedidoRepository):
        self.repo = repo

    def ejecutar(self, pedido_id: int) -> None:
        if not self.repo.get_by_id(pedido_id):
            raise NotFoundError('Pedido no encontrado')
        self.repo.eliminar(pedido_id)


