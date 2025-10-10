from datetime import datetime

from funcionalidades.core.infraestructura.database import db


class ChatMessageModel(db.Model):
    __tablename__ = 'chat_messages'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'), nullable=True, default=None)
    role = db.Column(db.String(16), nullable=False)  # 'user' | 'assistant' | 'system'
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)



