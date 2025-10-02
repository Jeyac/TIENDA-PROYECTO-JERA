from dataclasses import dataclass
from typing import List, Optional

from funcionalidades.core.exceptions import BadRequestError


@dataclass(frozen=True)
class PedidoItem:
    producto_id: int
    cantidad: int
    precio_unitario: float

    def __post_init__(self):
        if self.cantidad <= 0:
            raise BadRequestError('cantidad debe ser > 0')
        if self.precio_unitario < 0:
            raise BadRequestError('precio_unitario debe ser >= 0')


@dataclass(frozen=True)
class Pedido:
    id: Optional[int]
    usuario_id: int
    items: List[PedidoItem]
    total: float
    datos_facturacion: dict

    def __post_init__(self):
        if self.usuario_id is None:
            raise BadRequestError('usuario_id es obligatorio')
        if not isinstance(self.items, list) or len(self.items) == 0:
            raise BadRequestError('items no puede ser vacío')
        if self.total < 0:
            raise BadRequestError('total debe ser >= 0')
        if not isinstance(self.datos_facturacion, dict):
            raise BadRequestError('datos_facturacion debe ser un objeto')

