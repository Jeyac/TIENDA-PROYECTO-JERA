from typing import Optional
from funcionalidades.tickets.domain.entities.ticket_entity import Ticket
from funcionalidades.tickets.domain.repositories.ticket_repository import TicketRepository
from funcionalidades.core.exceptions import NotFoundError


class ObtenerTicketUseCase:
    def __init__(self, ticket_repo: TicketRepository):
        self.ticket_repo = ticket_repo

    def ejecutar(self, ticket_id: int) -> Ticket:
        """Obtener un ticket por ID"""
        ticket = self.ticket_repo.get_by_id(ticket_id)
        if not ticket:
            raise NotFoundError("Ticket no encontrado")
        return ticket
