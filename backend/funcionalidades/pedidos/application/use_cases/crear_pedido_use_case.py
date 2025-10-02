from typing import List

from funcionalidades.pedidos.domain.entities.pedido_entity import Pedido, PedidoItem
from funcionalidades.pedidos.domain.repositories.pedido_repository import PedidoRepository


class CrearPedidoUseCase:
    def __init__(self, repo: PedidoRepository):
        self.repo = repo

    def ejecutar(self, usuario_id: int, items: List[dict], datos_facturacion: dict) -> Pedido:
        items_entities = [PedidoItem(producto_id=i['producto_id'], cantidad=i['cantidad'], precio_unitario=i['precio_unitario']) for i in items]
        total = sum(i.cantidad * i.precio_unitario for i in items_entities)
        pedido = Pedido(id=None, usuario_id=usuario_id, items=items_entities, total=total, datos_facturacion=datos_facturacion)
        return self.repo.agregar(pedido)


