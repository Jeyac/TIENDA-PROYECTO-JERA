from funcionalidades.tickets.domain.entities.ticket_entity import Ticket, TicketActivity
from funcionalidades.tickets.domain.repositories.ticket_repository import TicketRepository
from funcionalidades.core.exceptions import NotFoundError


class CrearTicketDesdeConversacionUseCase:
    def __init__(self, ticket_repo: TicketRepository):
        self.ticket_repo = ticket_repo

    def ejecutar(
        self,
        conversation_id: int,
        user_id: int = None,
        title: str = None,
        description: str = None,
        priority: str = 'media',
        category: str = 'soporte'
    ) -> Ticket:
        """Crear ticket desde una conversación"""
        # Verificar si ya existe un ticket para esta conversación
        ticket_existente = self.ticket_repo.get_by_conversation_id(conversation_id)
        if ticket_existente:
            raise ValueError("Ya existe un ticket para esta conversación")
        
        # Generar título si no se proporciona
        if not title:
            title = f"Ticket de conversación {conversation_id}"
        
        # Crear entidad del dominio
        ticket = Ticket(
            id=None,
            user_id=user_id,
            conversation_id=conversation_id,
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
            description=f"Ticket creado automáticamente desde conversación {conversation_id}",
            old_value=None,
            new_value=None,
            created_at=None
        )
        
        self.ticket_repo.agregar_actividad(actividad)
        
        return ticket_creado
