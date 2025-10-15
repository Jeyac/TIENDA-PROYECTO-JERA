from datetime import datetime
from funcionalidades.tickets.domain.entities.ticket_entity import Ticket, TicketActivity
from funcionalidades.tickets.domain.repositories.ticket_repository import TicketRepository
from funcionalidades.core.exceptions import NotFoundError, BadRequestError


class ActualizarEstadoTicketUseCase:
    def __init__(self, ticket_repo: TicketRepository):
        self.ticket_repo = ticket_repo

    def ejecutar(
        self,
        ticket_id: int,
        new_status: str,
        user_id: int = None,
        resolution: str = None
    ) -> Ticket:
        """Actualizar estado de un ticket"""
        # Obtener ticket existente
        ticket = self.ticket_repo.get_by_id(ticket_id)
        if not ticket:
            raise NotFoundError("Ticket no encontrado")
        
        # Validar nuevo estado
        if new_status not in {'abierto', 'en_progreso', 'cerrado', 'resuelto'}:
            raise BadRequestError("Estado de ticket inválido")
        
        # Si el estado no cambió, no hacer nada
        if ticket.status == new_status:
            return ticket
        
        # Crear ticket actualizado
        ticket_actualizado = Ticket(
            id=ticket.id,
            user_id=ticket.user_id,
            conversation_id=ticket.conversation_id,
            title=ticket.title,
            description=ticket.description,
            status=new_status,
            priority=ticket.priority,
            category=ticket.category,
            assigned_to=ticket.assigned_to,
            resolution=resolution or ticket.resolution,
            created_at=ticket.created_at,
            updated_at=None,  # Se actualizará en el repositorio
            closed_at=datetime.utcnow() if new_status in {'cerrado', 'resuelto'} else ticket.closed_at
        )
        
        # Actualizar ticket
        ticket_modificado = self.ticket_repo.modificar(ticket_id, ticket_actualizado)
        
        # Crear actividad
        actividad = TicketActivity(
            id=None,
            ticket_id=ticket_id,
            user_id=user_id,
            activity_type='updated',
            description=f"Estado cambiado de '{ticket.status}' a '{new_status}'",
            old_value=ticket.status,
            new_value=new_status,
            created_at=None
        )
        
        self.ticket_repo.agregar_actividad(actividad)
        
        return ticket_modificado
