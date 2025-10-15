from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from funcionalidades.core.exceptions import BadRequestError


@dataclass(frozen=True)
class ChatMessage:
    id: Optional[int]
    conversation_id: int
    user_id: Optional[int]
    role: str
    content: str
    created_at: Optional[datetime]

    def __post_init__(self):
        if not self.conversation_id:
            raise BadRequestError('El ID de la conversación es obligatorio')
        
        if not self.role or not self.role.strip():
            raise BadRequestError('El rol del mensaje es obligatorio')
        
        if self.role not in {'user', 'assistant', 'system'}:
            raise BadRequestError('Rol de mensaje inválido')
        
        if not self.content or not self.content.strip():
            raise BadRequestError('El contenido del mensaje es obligatorio')
        
        if len(self.content.strip()) > 10000:
            raise BadRequestError('El contenido del mensaje no puede exceder 10000 caracteres')
