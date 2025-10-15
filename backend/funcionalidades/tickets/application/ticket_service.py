from datetime import datetime
from typing import Optional, List, Dict, Any
from funcionalidades.core.infraestructura.database import db
from funcionalidades.tickets.infrastructure.ticket_model import TicketModel, TicketActivityModel
from funcionalidades.chatlog.infrastructure.conversation_model import ConversationModel


class TicketService:
    """Servicio para manejo de tickets con seguimiento"""
    
    def __init__(self):
        pass
    
    def create_ticket_from_conversation(
        self, 
        conversation_id: int, 
        user_id: Optional[int] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: str = 'media',
        category: str = 'soporte'
    ) -> TicketModel:
        """Crear ticket desde una conversación"""
        try:
            conversation = ConversationModel.query.get(conversation_id)
            if not conversation:
                raise ValueError("Conversación no encontrada")
            
            # Generar título si no se proporciona
            if not title:
                title = f"Ticket de {conversation.title or 'conversación'}"
            
            # Crear ticket
            ticket = TicketModel(
                user_id=user_id,
                conversation_id=conversation_id,
                title=title,
                description=description,
                priority=priority,
                category=category,
                status='abierto'
            )
            
            db.session.add(ticket)
            db.session.commit()
            
            # Crear actividad de creación
            self._create_activity(
                ticket_id=ticket.id,
                user_id=user_id,
                activity_type='created',
                description=f"Ticket creado automáticamente desde conversación {conversation_id}"
            )
            
            return ticket
            
        except Exception as e:
            db.session.rollback()
            raise e
    
    def create_manual_ticket(
        self,
        user_id: int,
        title: str,
        description: str,
        priority: str = 'media',
        category: str = 'soporte'
    ) -> TicketModel:
        """Crear ticket manualmente"""
        try:
            ticket = TicketModel(
                user_id=user_id,
                title=title,
                description=description,
                priority=priority,
                category=category,
                status='abierto'
            )
            
            db.session.add(ticket)
            db.session.commit()
            
            # Crear actividad
            self._create_activity(
                ticket_id=ticket.id,
                user_id=user_id,
                activity_type='created',
                description="Ticket creado manualmente"
            )
            
            return ticket
            
        except Exception as e:
            db.session.rollback()
            raise e
    
    def update_ticket_status(
        self, 
        ticket_id: int, 
        new_status: str, 
        user_id: Optional[int] = None,
        resolution: Optional[str] = None
    ) -> TicketModel:
        """Actualizar estado de ticket"""
        try:
            ticket = TicketModel.query.get(ticket_id)
            if not ticket:
                raise ValueError("Ticket no encontrado")
            
            old_status = ticket.status
            ticket.status = new_status
            
            if new_status in ['cerrado', 'resuelto']:
                ticket.closed_at = datetime.utcnow()
                if resolution:
                    ticket.resolution = resolution
            
            db.session.commit()
            
            # Crear actividad
            self._create_activity(
                ticket_id=ticket_id,
                user_id=user_id,
                activity_type='updated',
                description=f"Estado cambiado de {old_status} a {new_status}",
                old_value=old_status,
                new_value=new_status
            )
            
            return ticket
            
        except Exception as e:
            db.session.rollback()
            raise e
    
    def assign_ticket(
        self, 
        ticket_id: int, 
        assignee_id: int, 
        user_id: Optional[int] = None
    ) -> TicketModel:
        """Asignar ticket a un administrador"""
        try:
            ticket = TicketModel.query.get(ticket_id)
            if not ticket:
                raise ValueError("Ticket no encontrado")
            
            old_assignee = ticket.assigned_to
            ticket.assigned_to = assignee_id
            
            db.session.commit()
            
            # Crear actividad
            self._create_activity(
                ticket_id=ticket_id,
                user_id=user_id,
                activity_type='assigned',
                description=f"Ticket asignado a usuario {assignee_id}",
                old_value=str(old_assignee) if old_assignee else None,
                new_value=str(assignee_id)
            )
            
            return ticket
            
        except Exception as e:
            db.session.rollback()
            raise e
    
    def get_user_tickets(self, user_id: int) -> List[Dict[str, Any]]:
        """Obtener tickets de un usuario"""
        tickets = TicketModel.query.filter_by(user_id=user_id).order_by(TicketModel.created_at.desc()).all()
        
        return [
            {
                'id': ticket.id,
                'title': ticket.title,
                'description': ticket.description,
                'status': ticket.status,
                'priority': ticket.priority,
                'category': ticket.category,
                'assigned_to': ticket.assigned_to,
                'assignee_name': ticket.assignee.username if ticket.assignee and hasattr(ticket.assignee, 'username') else None,
                'created_at': ticket.created_at.isoformat(),
                'updated_at': ticket.updated_at.isoformat(),
                'closed_at': ticket.closed_at.isoformat() if ticket.closed_at else None,
                'resolution': ticket.resolution,
                'activities': [
                    {
                        'id': activity.id,
                        'activity_type': activity.activity_type,
                        'description': activity.description,
                        'created_at': activity.created_at.isoformat(),
                        'user_rol': activity.user.rol if activity.user else 'cliente'
                    }
                    for activity in ticket.activities
                ]
            }
            for ticket in tickets
        ]
    
    def get_assigned_tickets(self, assignee_id: int, status_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """Obtener tickets asignados a un usuario (para atención al cliente)"""
        query = TicketModel.query.filter_by(assigned_to=assignee_id)
        
        if status_filter:
            query = query.filter_by(status=status_filter)
        
        tickets = query.order_by(TicketModel.created_at.desc()).all()
        
        return [
            {
                'id': ticket.id,
                'user_id': ticket.user_id,
                'title': ticket.title,
                'description': ticket.description,
                'status': ticket.status,
                'priority': ticket.priority,
                'category': ticket.category,
                'assigned_to': ticket.assigned_to,
                'created_at': ticket.created_at.isoformat(),
                'updated_at': ticket.updated_at.isoformat(),
                'closed_at': ticket.closed_at.isoformat() if ticket.closed_at else None,
                'resolution': ticket.resolution,
                'user_name': ticket.user.username if ticket.user else 'Usuario anónimo',
                'user_email': ticket.user.email if ticket.user else None,
                'activities': [
                    {
                        'id': activity.id,
                        'activity_type': activity.activity_type,
                        'description': activity.description,
                        'created_at': activity.created_at.isoformat(),
                        'user_rol': activity.user.rol if activity.user else 'cliente'
                    }
                    for activity in ticket.activities
                ]
            }
            for ticket in tickets
        ]
    
    def get_all_tickets(self, status_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """Obtener todos los tickets (para administradores)"""
        query = TicketModel.query
        
        if status_filter:
            query = query.filter_by(status=status_filter)
        
        tickets = query.order_by(TicketModel.created_at.desc()).all()
        
        return [
            {
                'id': ticket.id,
                'user_id': ticket.user_id,
                'title': ticket.title,
                'description': ticket.description,
                'status': ticket.status,
                'priority': ticket.priority,
                'category': ticket.category,
                'assigned_to': ticket.assigned_to,
                'created_at': ticket.created_at.isoformat(),
                'updated_at': ticket.updated_at.isoformat(),
                'closed_at': ticket.closed_at.isoformat() if ticket.closed_at else None,
                'resolution': ticket.resolution,
                'user_name': ticket.user.username if ticket.user else 'Usuario anónimo',
                'assignee_name': ticket.assignee.username if ticket.assignee else None
            }
            for ticket in tickets
        ]
    
    def get_ticket_activities(self, ticket_id: int) -> List[Dict[str, Any]]:
        """Obtener actividades de un ticket"""
        activities = TicketActivityModel.query.filter_by(ticket_id=ticket_id).order_by(TicketActivityModel.created_at.asc()).all()
        
        return [
            {
                'id': activity.id,
                'activity_type': activity.activity_type,
                'description': activity.description,
                'old_value': activity.old_value,
                'new_value': activity.new_value,
                'user_id': activity.user_id,
                'created_at': activity.created_at.isoformat(),
                'user_name': activity.user.username if activity.user else 'Sistema',
                'user_rol': activity.user.rol if activity.user else None
            }
            for activity in activities
        ]
    
    def _create_activity(
        self, 
        ticket_id: int, 
        user_id: Optional[int], 
        activity_type: str, 
        description: str,
        old_value: Optional[str] = None,
        new_value: Optional[str] = None
    ):
        """Crear actividad de ticket"""
        activity = TicketActivityModel(
            ticket_id=ticket_id,
            user_id=user_id,
            activity_type=activity_type,
            description=description,
            old_value=old_value,
            new_value=new_value
        )
        
        db.session.add(activity)
        db.session.commit()
