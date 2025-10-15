from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime

from funcionalidades.core.exceptions import BadRequestError


@dataclass(frozen=True)
class Conversation:
    id: Optional[int]
    user_id: Optional[int]
    session_id: Optional[str]
    title: str
    is_active: bool
    summary: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    def __post_init__(self):
        if not self.title or not self.title.strip():
            raise BadRequestError('El título de la conversación es obligatorio')
        
        if len(self.title.strip()) > 255:
            raise BadRequestError('El título de la conversación no puede exceder 255 caracteres')
        
        if not isinstance(self.is_active, bool):
            raise BadRequestError('El estado activo debe ser un valor booleano')
