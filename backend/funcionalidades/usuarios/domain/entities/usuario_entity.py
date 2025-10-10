from dataclasses import dataclass
from typing import Optional

from funcionalidades.core.exceptions import BadRequestError


@dataclass(frozen=True)
class Usuario:
    id: Optional[int]
    username: str
    email: str
    password_hash: str
    rol: str

    def __post_init__(self):
        if not self.username or not self.username.strip():
            raise BadRequestError('username es obligatorio')
        
        # Validación de email más estricta
        if not self.email or not self.email.strip():
            raise BadRequestError('email es obligatorio')
        if '@' not in self.email or '.' not in self.email.split('@')[-1]:
            raise BadRequestError('email inválido')
        
        if not self.password_hash:
            raise BadRequestError('password_hash es obligatorio')
        if self.rol not in {'cliente', 'administrador', 'atencion_cliente'}:
            raise BadRequestError('rol inválido')


