from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from funcionalidades.core.exceptions import BadRequestError


@dataclass(frozen=True)
class Ticket:
    id: Optional[int]
    user_id: Optional[int]
    conversation_id: Optional[int]
    title: str
    description: Optional[str]
    status: str
    priority: str
    category: Optional[str]
    assigned_to: Optional[int]
    resolution: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    closed_at: Optional[datetime]

    def __post_init__(self):
        if not self.title or not self.title.strip():
            raise BadRequestError('El título del ticket es obligatorio')
        
        if len(self.title.strip()) > 255:
            raise BadRequestError('El título del ticket no puede exceder 255 caracteres')
        
        if self.status not in {'abierto', 'en_progreso', 'cerrado', 'resuelto'}:
            raise BadRequestError('Estado de ticket inválido')
        
        if self.priority not in {'baja', 'media', 'alta', 'urgente'}:
            raise BadRequestError('Prioridad de ticket inválida')
        
        if self.category and self.category not in {'soporte', 'ventas', 'tecnico', 'general'}:
            raise BadRequestError('Categoría de ticket inválida')


@dataclass(frozen=True)
class TicketActivity:
    id: Optional[int]
    ticket_id: int
    user_id: Optional[int]
    activity_type: str
    description: Optional[str]
    old_value: Optional[str]
    new_value: Optional[str]
    created_at: Optional[datetime]

    def __post_init__(self):
        if not self.ticket_id:
            raise BadRequestError('El ID del ticket es obligatorio')
        
        if not self.activity_type or not self.activity_type.strip():
            raise BadRequestError('El tipo de actividad es obligatorio')
        
        valid_activity_types = {'created', 'updated', 'assigned', 'closed', 'commented'}
        if self.activity_type not in valid_activity_types:
            raise BadRequestError('Tipo de actividad inválido')
        
        if len(self.activity_type.strip()) > 50:
            raise BadRequestError('El tipo de actividad no puede exceder 50 caracteres')
