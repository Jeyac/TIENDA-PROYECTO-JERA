from funcionalidades.core.exceptions import NotFoundError, BadRequestError
from funcionalidades.pedidos.domain.repositories.pedido_repository import PedidoRepository
from funcionalidades.productos.application.stock_service import StockService


class ActualizarEstadoPedidoUseCase:
    def __init__(self, repo: PedidoRepository):
        self.repo = repo

    def ejecutar(self, pedido_id: int, nuevo_estado: str) -> None:
        pedido = self.repo.get_by_id(pedido_id)
        if not pedido:
            raise NotFoundError('Pedido no encontrado')
        
        # Estados válidos
        estados_validos = ['pendiente', 'confirmado', 'enviado', 'entregado', 'cancelado']
        if nuevo_estado not in estados_validos:
            raise BadRequestError(f'Estado inválido. Estados válidos: {", ".join(estados_validos)}')
        
        # Obtener el estado anterior del pedido desde la base de datos
        from funcionalidades.pedidos.infrastructure.pedido_model import PedidoModel
        pedido_model = PedidoModel.query.get(pedido_id)
        estado_anterior = pedido_model.estado if pedido_model else 'pendiente'
        
        # Si el pedido se cancela, restaurar el stock (solo si no estaba ya cancelado)
        if nuevo_estado == 'cancelado' and estado_anterior != 'cancelado':
            StockService.restaurar_stock(pedido_id)
        
        # Actualizar el estado en la base de datos
        if pedido_model:
            pedido_model.estado = nuevo_estado
            from funcionalidades.core.infraestructura.database import db
            db.session.commit()
