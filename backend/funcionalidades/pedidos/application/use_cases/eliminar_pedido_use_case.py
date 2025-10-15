from funcionalidades.core.exceptions import NotFoundError
from funcionalidades.pedidos.domain.repositories.pedido_repository import PedidoRepository
from funcionalidades.productos.application.stock_service import StockService


class EliminarPedidoUseCase:
    def __init__(self, repo: PedidoRepository):
        self.repo = repo

    def ejecutar(self, pedido_id: int) -> None:
        pedido = self.repo.get_by_id(pedido_id)
        if not pedido:
            raise NotFoundError('Pedido no encontrado')
        
        # Restaurar stock antes de eliminar el pedido
        StockService.restaurar_stock(pedido_id)
        
        # Eliminar el pedido
        self.repo.eliminar(pedido_id)


