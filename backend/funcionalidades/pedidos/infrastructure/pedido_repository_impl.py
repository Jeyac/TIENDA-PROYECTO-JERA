from typing import List, Optional

from funcionalidades.core.infraestructura.database import db
from funcionalidades.pedidos.domain.entities.pedido_entity import Pedido, PedidoItem
from funcionalidades.pedidos.domain.repositories.pedido_repository import PedidoRepository
from funcionalidades.pedidos.infrastructure.pedido_model import PedidoModel, PedidoItemModel


def _to_entity(model: PedidoModel) -> Pedido:
    items = [PedidoItem(producto_id=i.producto_id, cantidad=i.cantidad, precio_unitario=i.precio_unitario) for i in model.items]
    return Pedido(id=model.id, usuario_id=model.usuario_id, items=items, total=model.total, datos_facturacion=model.datos_facturacion or {})


class PedidoRepositoryImpl(PedidoRepository):
    def agregar(self, pedido: Pedido) -> Pedido:
        m = PedidoModel(usuario_id=pedido.usuario_id, total=pedido.total, datos_facturacion=pedido.datos_facturacion)
        db.session.add(m)
        db.session.flush()
        for it in pedido.items:
            db.session.add(PedidoItemModel(pedido_id=m.id, producto_id=it.producto_id, cantidad=it.cantidad, precio_unitario=it.precio_unitario))
        db.session.commit()
        return _to_entity(m)

    def listar(self) -> List[Pedido]:
        return [_to_entity(m) for m in PedidoModel.query.all()]

    def get_by_id(self, pedido_id: int) -> Optional[Pedido]:
        m = PedidoModel.query.get(pedido_id)
        return _to_entity(m) if m else None

    def modificar(self, pedido_id: int, pedido: Pedido) -> Pedido:
        m = PedidoModel.query.get(pedido_id)
        if not m:
            return None
        m.total = pedido.total
        # Reemplazar items
        for i in list(m.items):
            db.session.delete(i)
        db.session.flush()
        for it in pedido.items:
            db.session.add(PedidoItemModel(pedido_id=m.id, producto_id=it.producto_id, cantidad=it.cantidad, precio_unitario=it.precio_unitario))
        db.session.commit()
        return _to_entity(m)

    def eliminar(self, pedido_id: int) -> None:
        m = PedidoModel.query.get(pedido_id)
        if m:
            db.session.delete(m)
            db.session.commit()


