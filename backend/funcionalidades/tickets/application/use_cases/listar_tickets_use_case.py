from typing import List, Optional
from funcionalidades.tickets.domain.entities.ticket_entity import Ticket
from funcionalidades.tickets.domain.repositories.ticket_repository import TicketRepository


class ListarTicketsUseCase:
    def __init__(self, ticket_repo: TicketRepository):
        self.ticket_repo = ticket_repo

    def ejecutar(
        self,
        user_id: Optional[int] = None,
        status: Optional[str] = None,
        assigned_to: Optional[int] = None
    ) -> List[Ticket]:
        """Listar tickets con filtros opcionales"""
        if user_id:
            return self.ticket_repo.get_by_user_id(user_id)
        elif status:
            return self.ticket_repo.get_by_status(status)
        elif assigned_to:
            return self.ticket_repo.get_by_assigned_to(assigned_to)
        else:
            return self.ticket_repo.listar()
