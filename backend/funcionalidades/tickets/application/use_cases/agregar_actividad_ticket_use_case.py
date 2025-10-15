from funcionalidades.tickets.domain.entities.ticket_entity import TicketActivity
from funcionalidades.tickets.domain.repositories.ticket_repository import TicketRepository
from funcionalidades.core.exceptions import NotFoundError


class AgregarActividadTicketUseCase:
    def __init__(self, ticket_repo: TicketRepository):
        self.ticket_repo = ticket_repo

    def ejecutar(
        self,
        ticket_id: int,
        user_id: int,
        activity_type: str,
        description: str = None,
        old_value: str = None,
        new_value: str = None
    ) -> TicketActivity:
        """Agregar actividad a un ticket"""
        # Verificar que el ticket existe
        ticket = self.ticket_repo.get_by_id(ticket_id)
        if not ticket:
            raise NotFoundError("Ticket no encontrado")
        
        # Crear actividad
        actividad = TicketActivity(
            id=None,
            ticket_id=ticket_id,
            user_id=user_id,
            activity_type=activity_type,
            description=description,
            old_value=old_value,
            new_value=new_value,
            created_at=None
        )
        
        # Guardar actividad
        return self.ticket_repo.agregar_actividad(actividad)
