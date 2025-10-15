from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from funcionalidades.core.exceptions import BadRequestError


@dataclass(frozen=True)
class PasswordReset:
    id: Optional[int]
    user_id: int
    token: str
    expires_at: datetime
    used: bool
    created_at: Optional[datetime]

    def __post_init__(self):
        if not self.user_id:
            raise BadRequestError('El ID del usuario es obligatorio')
        
        if not self.token or not self.token.strip():
            raise BadRequestError('El token es obligatorio')
        
        if len(self.token.strip()) < 16:
            raise BadRequestError('El token debe tener al menos 16 caracteres')
        
        if not isinstance(self.used, bool):
            raise BadRequestError('El estado usado debe ser un valor booleano')
        
        if self.expires_at <= datetime.utcnow():
            raise BadRequestError('El token no puede estar expirado al momento de creación')
    
    def is_expired(self) -> bool:
        """Verificar si el token está expirado"""
        return self.expires_at <= datetime.utcnow()
    
    def is_valid(self) -> bool:
        """Verificar si el token es válido (no usado y no expirado)"""
        return not self.used and not self.is_expired()
