from typing import List

from funcionalidades.core.exceptions import NotFoundError
from funcionalidades.pedidos.domain.entities.pedido_entity import Pedido, PedidoItem
from funcionalidades.pedidos.domain.repositories.pedido_repository import PedidoRepository


class ActualizarPedidoUseCase:
    def __init__(self, repo: PedidoRepository):
        self.repo = repo

    def ejecutar(self, pedido_id: int, items: List[dict]) -> Pedido:
        if not self.repo.get_by_id(pedido_id):
            raise NotFoundError('Pedido no encontrado')
        items_entities = [PedidoItem(producto_id=i['producto_id'], cantidad=i['cantidad'], precio_unitario=i['precio_unitario']) for i in items]
        total = sum(i.cantidad * i.precio_unitario for i in items_entities)
        pedido = Pedido(id=pedido_id, usuario_id=0, items=items_entities, total=total)  # usuario_id no cambia aquí
        return self.repo.modificar(pedido_id, pedido)






