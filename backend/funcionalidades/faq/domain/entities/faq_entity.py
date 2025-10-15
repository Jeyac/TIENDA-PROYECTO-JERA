from dataclasses import dataclass
from typing import Optional

from funcionalidades.core.exceptions import BadRequestError


@dataclass(frozen=True)
class FAQ:
    id: Optional[int]
    pregunta: str
    respuesta: str

    def __post_init__(self):
        if not self.pregunta or not self.pregunta.strip():
            raise BadRequestError('La pregunta es obligatoria')
        
        if not self.respuesta or not self.respuesta.strip():
            raise BadRequestError('La respuesta es obligatoria')
        
        if len(self.pregunta.strip()) > 500:
            raise BadRequestError('La pregunta no puede exceder 500 caracteres')
        
        if len(self.respuesta.strip()) > 2000:
            raise BadRequestError('La respuesta no puede exceder 2000 caracteres')
