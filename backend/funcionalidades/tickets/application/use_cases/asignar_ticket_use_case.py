from funcionalidades.tickets.domain.entities.ticket_entity import Ticket, TicketActivity
from funcionalidades.tickets.domain.repositories.ticket_repository import TicketRepository
from funcionalidades.core.exceptions import NotFoundError


class AsignarTicketUseCase:
    def __init__(self, ticket_repo: TicketRepository):
        self.ticket_repo = ticket_repo

    def ejecutar(
        self,
        ticket_id: int,
        assigned_to: int,
        user_id: int = None
    ) -> Ticket:
        """Asignar ticket a un usuario"""
        # Obtener ticket existente
        ticket = self.ticket_repo.get_by_id(ticket_id)
        if not ticket:
            raise NotFoundError("Ticket no encontrado")
        
        # Si ya está asignado al mismo usuario, no hacer nada
        if ticket.assigned_to == assigned_to:
            return ticket
        
        # Crear ticket actualizado
        ticket_actualizado = Ticket(
            id=ticket.id,
            user_id=ticket.user_id,
            conversation_id=ticket.conversation_id,
            title=ticket.title,
            description=ticket.description,
            status=ticket.status,
            priority=ticket.priority,
            category=ticket.category,
            assigned_to=assigned_to,
            resolution=ticket.resolution,
            created_at=ticket.created_at,
            updated_at=None,  # Se actualizará en el repositorio
            closed_at=ticket.closed_at
        )
        
        # Actualizar ticket
        ticket_modificado = self.ticket_repo.modificar(ticket_id, ticket_actualizado)
        
        # Crear actividad
        actividad = TicketActivity(
            id=None,
            ticket_id=ticket_id,
            user_id=user_id,
            activity_type='assigned',
            description=f"Ticket asignado al usuario {assigned_to}",
            old_value=str(ticket.assigned_to) if ticket.assigned_to else None,
            new_value=str(assigned_to),
            created_at=None
        )
        
        self.ticket_repo.agregar_actividad(actividad)
        
        return ticket_modificado
