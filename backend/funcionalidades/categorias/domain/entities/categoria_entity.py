from dataclasses import dataclass
from typing import Optional

from funcionalidades.core.exceptions import BadRequestError


@dataclass(frozen=True)
class Categoria:
    id: Optional[int]
    nombre: str
    descripcion: str
    activa: bool

    def __post_init__(self):
        if not self.nombre or not self.nombre.strip():
            raise BadRequestError('El nombre es obligatorio')
        if not self.descripcion or not self.descripcion.strip():
            raise BadRequestError('La descripción es obligatoria')