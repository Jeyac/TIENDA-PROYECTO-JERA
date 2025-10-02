import pytest

from funcionalidades.pedidos.domain.entities.pedido_entity import Pedido, PedidoItem
from funcionalidades.core.exceptions import BadRequestError


def test_pedido_valido():
    items = [PedidoItem(producto_id=1, cantidad=2, precio_unitario=5.0)]
    datos_facturacion = {"nombre": "Juan", "email": "juan@test.com"}
    p = Pedido(id=None, usuario_id=1, items=items, total=10.0, datos_facturacion=datos_facturacion)
    assert p.total == 10.0


def test_pedido_sin_items():
    with pytest.raises(BadRequestError):
        datos_facturacion = {"nombre": "Juan", "email": "juan@test.com"}
        Pedido(id=None, usuario_id=1, items=[], total=0, datos_facturacion=datos_facturacion)


def test_item_invalido_cantidad():
    with pytest.raises(BadRequestError):
        PedidoItem(producto_id=1, cantidad=0, precio_unitario=1.0)


