from typing import List, Optional
from datetime import datetime

from funcionalidades.core.infraestructura.database import db
from funcionalidades.tickets.domain.entities.ticket_entity import Ticket, TicketActivity
from funcionalidades.tickets.domain.repositories.ticket_repository import TicketRepository
from funcionalidades.tickets.infrastructure.ticket_model import TicketModel, TicketActivityModel


def _to_ticket_entity(model: TicketModel) -> Ticket:
    return Ticket(
        id=model.id,
        user_id=model.user_id,
        conversation_id=model.conversation_id,
        title=model.title,
        description=model.description,
        status=model.status,
        priority=model.priority,
        category=model.category,
        assigned_to=model.assigned_to,
        resolution=model.resolution,
        created_at=model.created_at,
        updated_at=model.updated_at,
        closed_at=model.closed_at
    )


def _to_ticket_activity_entity(model: TicketActivityModel) -> TicketActivity:
    return TicketActivity(
        id=model.id,
        ticket_id=model.ticket_id,
        user_id=model.user_id,
        activity_type=model.activity_type,
        description=model.description,
        old_value=model.old_value,
        new_value=model.new_value,
        created_at=model.created_at
    )


def _to_ticket_model(ticket: Ticket) -> TicketModel:
    return TicketModel(
        id=ticket.id,
        user_id=ticket.user_id,
        conversation_id=ticket.conversation_id,
        title=ticket.title,
        description=ticket.description,
        status=ticket.status,
        priority=ticket.priority,
        category=ticket.category,
        assigned_to=ticket.assigned_to,
        resolution=ticket.resolution,
        created_at=ticket.created_at,
        updated_at=ticket.updated_at,
        closed_at=ticket.closed_at
    )


def _to_ticket_activity_model(actividad: TicketActivity) -> TicketActivityModel:
    return TicketActivityModel(
        id=actividad.id,
        ticket_id=actividad.ticket_id,
        user_id=actividad.user_id,
        activity_type=actividad.activity_type,
        description=actividad.description,
        old_value=actividad.old_value,
        new_value=actividad.new_value,
        created_at=actividad.created_at
    )


class TicketRepositoryImpl(TicketRepository):
    def agregar(self, ticket: Ticket) -> Ticket:
        model = _to_ticket_model(ticket)
        db.session.add(model)
        db.session.commit()
        return _to_ticket_entity(model)

    def listar(self) -> List[Ticket]:
        models = TicketModel.query.all()
        return [_to_ticket_entity(model) for model in models]

    def get_by_id(self, ticket_id: int) -> Optional[Ticket]:
        model = TicketModel.query.get(ticket_id)
        return _to_ticket_entity(model) if model else None

    def modificar(self, ticket_id: int, ticket: Ticket) -> Ticket:
        model = TicketModel.query.get(ticket_id)
        if not model:
            return None
        
        # Actualizar campos
        model.user_id = ticket.user_id
        model.conversation_id = ticket.conversation_id
        model.title = ticket.title
        model.description = ticket.description
        model.status = ticket.status
        model.priority = ticket.priority
        model.category = ticket.category
        model.assigned_to = ticket.assigned_to
        model.resolution = ticket.resolution
        model.updated_at = datetime.utcnow()
        model.closed_at = ticket.closed_at
        
        db.session.commit()
        return _to_ticket_entity(model)

    def eliminar(self, ticket_id: int) -> None:
        model = TicketModel.query.get(ticket_id)
        if model:
            db.session.delete(model)
            db.session.commit()

    def get_by_user_id(self, user_id: int) -> List[Ticket]:
        models = TicketModel.query.filter_by(user_id=user_id).all()
        return [_to_ticket_entity(model) for model in models]

    def get_by_status(self, status: str) -> List[Ticket]:
        models = TicketModel.query.filter_by(status=status).all()
        return [_to_ticket_entity(model) for model in models]

    def get_by_assigned_to(self, assigned_to: int) -> List[Ticket]:
        models = TicketModel.query.filter_by(assigned_to=assigned_to).all()
        return [_to_ticket_entity(model) for model in models]

    def get_by_conversation_id(self, conversation_id: int) -> Optional[Ticket]:
        model = TicketModel.query.filter_by(conversation_id=conversation_id).first()
        return _to_ticket_entity(model) if model else None

    def agregar_actividad(self, actividad: TicketActivity) -> TicketActivity:
        model = _to_ticket_activity_model(actividad)
        db.session.add(model)
        db.session.commit()
        return _to_ticket_activity_entity(model)

    def get_actividades_by_ticket_id(self, ticket_id: int) -> List[TicketActivity]:
        models = TicketActivityModel.query.filter_by(ticket_id=ticket_id).order_by(TicketActivityModel.created_at.asc()).all()
        return [_to_ticket_activity_entity(model) for model in models]
