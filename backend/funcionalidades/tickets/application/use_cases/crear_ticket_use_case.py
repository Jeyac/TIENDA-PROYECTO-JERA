from datetime import datetime
from funcionalidades.tickets.domain.entities.ticket_entity import Ticket, TicketActivity
from funcionalidades.tickets.domain.repositories.ticket_repository import TicketRepository


class CrearTicketUseCase:
    def __init__(self, ticket_repo: TicketRepository):
        self.ticket_repo = ticket_repo

    def ejecutar(
        self,
        user_id: int,
        title: str,
        description: str,
        priority: str = 'media',
        category: str = 'soporte'
    ) -> Ticket:
        """Crear ticket manualmente"""
        # Crear entidad del dominio
        ticket = Ticket(
            id=None,
            user_id=user_id,
            conversation_id=None,
            title=title,
            description=description,
            status='abierto',
            priority=priority,
            category=category,
            assigned_to=None,
            resolution=None,
            created_at=None,
            updated_at=None,
            closed_at=None
        )
        
        # Guardar ticket
        ticket_creado = self.ticket_repo.agregar(ticket)
        
        # Crear actividad de creación
        actividad = TicketActivity(
            id=None,
            ticket_id=ticket_creado.id,
            user_id=user_id,
            activity_type='created',
            description="Ticket creado manualmente",
            old_value=None,
            new_value=None,
            created_at=None
        )
        
        self.ticket_repo.agregar_actividad(actividad)
        
        return ticket_creado
