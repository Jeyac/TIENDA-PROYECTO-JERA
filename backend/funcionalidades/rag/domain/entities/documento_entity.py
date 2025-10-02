from dataclasses import dataclass
from typing import Optional

from funcionalidades.core.exceptions import BadRequestError


@dataclass(frozen=True)
class Documento:
    id: Optional[int]
    titulo: str
    contenido: str

    def __post_init__(self):
        if not self.titulo or not self.titulo.strip():
            raise BadRequestError('titulo obligatorio')
        if not self.contenido or not self.contenido.strip():
            raise BadRequestError('contenido obligatorio')


