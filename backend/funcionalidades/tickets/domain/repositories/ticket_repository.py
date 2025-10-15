from abc import ABC, abstractmethod
from typing import List, Optional

from funcionalidades.tickets.domain.entities.ticket_entity import Ticket, TicketActivity


class TicketRepository(ABC):
    @abstractmethod
    def agregar(self, ticket: Ticket) -> Ticket:
        raise NotImplementedError

    @abstractmethod
    def listar(self) -> List[Ticket]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, ticket_id: int) -> Optional[Ticket]:
        raise NotImplementedError

    @abstractmethod
    def modificar(self, ticket_id: int, ticket: Ticket) -> Ticket:
        raise NotImplementedError

    @abstractmethod
    def eliminar(self, ticket_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_by_user_id(self, user_id: int) -> List[Ticket]:
        raise NotImplementedError

    @abstractmethod
    def get_by_status(self, status: str) -> List[Ticket]:
        raise NotImplementedError

    @abstractmethod
    def get_by_assigned_to(self, assigned_to: int) -> List[Ticket]:
        raise NotImplementedError

    @abstractmethod
    def get_by_conversation_id(self, conversation_id: int) -> Optional[Ticket]:
        raise NotImplementedError

    @abstractmethod
    def agregar_actividad(self, actividad: TicketActivity) -> TicketActivity:
        raise NotImplementedError

    @abstractmethod
    def get_actividades_by_ticket_id(self, ticket_id: int) -> List[TicketActivity]:
        raise NotImplementedError
