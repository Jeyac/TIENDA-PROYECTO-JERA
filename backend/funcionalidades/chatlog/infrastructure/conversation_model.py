from datetime import datetime
from funcionalidades.core.infraestructura.database import db


class ConversationModel(db.Model):
    __tablename__ = 'conversations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    session_id = db.Column(db.String(255), nullable=True)  # Para usuarios anónimos
    title = db.Column(db.String(255), nullable=True)  # Título de la conversación
    summary = db.Column(db.Text, nullable=True)  # Resumen de la conversación
    message_count = db.Column(db.Integer, default=0)  # Contador de mensajes
    last_message_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_active = db.Column(db.Boolean, default=True)  # Si la conversación está activa

    # Relación con mensajes
    messages = db.relationship('ChatMessageModel', backref='conversation', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Conversation {self.id}: {self.title or "Sin título"}>'



