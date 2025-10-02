from dataclasses import dataclass
from typing import List, Optional

from funcionalidades.core.exceptions import BadRequestError


@dataclass(frozen=True)
class Producto:
    id: Optional[int]
    titulo: str
    precio: float
    descripcion: str
    imagenes: List[str]
    categoria_id: int
    activo: bool

    def __post_init__(self):
        if not self.titulo or not self.titulo.strip():
            raise BadRequestError('El título es obligatorio')
        if self.precio is None or self.precio < 0:
            raise BadRequestError('El precio debe ser >= 0')
        if not isinstance(self.imagenes, list):
            raise BadRequestError('Las imágenes deben ser una lista')
        if self.categoria_id is None or self.categoria_id <= 0:
            raise BadRequestError('categoria_id debe ser válido')

