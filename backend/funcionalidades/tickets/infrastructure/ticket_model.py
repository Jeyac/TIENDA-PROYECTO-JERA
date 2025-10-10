from datetime import datetime
from funcionalidades.core.infraestructura.database import db
from funcionalidades.core.infraestructura.timezone import get_guatemala_time_utc


class TicketModel(db.Model):
    __tablename__ = 'tickets'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'), nullable=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), nullable=False, default='abierto')  # abierto, en_progreso, cerrado, resuelto
    priority = db.Column(db.String(20), nullable=False, default='media')  # baja, media, alta, urgente
    category = db.Column(db.String(100), nullable=True)  # soporte, ventas, tecnico, general
    assigned_to = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)  # admin asignado
    resolution = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=get_guatemala_time_utc, nullable=False)
    updated_at = db.Column(db.DateTime, default=get_guatemala_time_utc, onupdate=get_guatemala_time_utc, nullable=False)
    closed_at = db.Column(db.DateTime, nullable=True)
    
    # Relaciones
    user = db.relationship('UsuarioModel', foreign_keys=[user_id], backref='tickets_created')
    assignee = db.relationship('UsuarioModel', foreign_keys=[assigned_to], backref='tickets_assigned')
    conversation = db.relationship('ConversationModel', backref='ticket')

    def __repr__(self):
        return f'<Ticket {self.id}: {self.title}>'


class TicketActivityModel(db.Model):
    __tablename__ = 'ticket_activities'

    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    activity_type = db.Column(db.String(50), nullable=False)  # created, updated, assigned, closed, commented
    description = db.Column(db.Text, nullable=True)
    old_value = db.Column(db.String(255), nullable=True)
    new_value = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=get_guatemala_time_utc, nullable=False)
    
    # Relaciones
    ticket = db.relationship('TicketModel', backref='activities')
    user = db.relationship('UsuarioModel', backref='ticket_activities')

    def __repr__(self):
        return f'<TicketActivity {self.id}: {self.activity_type}>'
