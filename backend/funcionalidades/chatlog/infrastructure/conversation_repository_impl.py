from typing import List, Optional
from datetime import datetime

from funcionalidades.core.infraestructura.database import db
from funcionalidades.chatlog.domain.entities.conversation_entity import Conversation
from funcionalidades.chatlog.domain.repositories.conversation_repository import ConversationRepository
from funcionalidades.chatlog.infrastructure.conversation_model import ConversationModel


def _to_conversation_entity(model: ConversationModel) -> Conversation:
    return Conversation(
        id=model.id,
        user_id=model.user_id,
        session_id=model.session_id,
        title=model.title or "Sin título",
        is_active=model.is_active,
        summary=model.summary,
        created_at=model.created_at,
        updated_at=model.last_message_at
    )


def _to_conversation_model(conversation: Conversation) -> ConversationModel:
    return ConversationModel(
        id=conversation.id,
        user_id=conversation.user_id,
        session_id=conversation.session_id,
        title=conversation.title,
        is_active=conversation.is_active,
        summary=conversation.summary,
        created_at=conversation.created_at,
        last_message_at=conversation.updated_at
    )


class ConversationRepositoryImpl(ConversationRepository):
    def agregar(self, conversation: Conversation) -> Conversation:
        model = _to_conversation_model(conversation)
        db.session.add(model)
        db.session.commit()
        return _to_conversation_entity(model)

    def listar(self) -> List[Conversation]:
        models = ConversationModel.query.order_by(ConversationModel.created_at.desc()).all()
        return [_to_conversation_entity(model) for model in models]

    def get_by_id(self, conversation_id: int) -> Optional[Conversation]:
        model = ConversationModel.query.get(conversation_id)
        return _to_conversation_entity(model) if model else None

    def modificar(self, conversation_id: int, conversation: Conversation) -> Conversation:
        model = ConversationModel.query.get(conversation_id)
        if not model:
            return None
        
        # Actualizar campos
        model.user_id = conversation.user_id
        model.session_id = conversation.session_id
        model.title = conversation.title
        model.is_active = conversation.is_active
        model.summary = conversation.summary
        model.last_message_at = datetime.utcnow()
        
        db.session.commit()
        return _to_conversation_entity(model)

    def eliminar(self, conversation_id: int) -> None:
        model = ConversationModel.query.get(conversation_id)
        if model:
            db.session.delete(model)
            db.session.commit()

    def get_by_user_id(self, user_id: int) -> List[Conversation]:
        models = ConversationModel.query.filter_by(user_id=user_id).order_by(ConversationModel.created_at.desc()).all()
        return [_to_conversation_entity(model) for model in models]

    def get_by_session_id(self, session_id: str) -> List[Conversation]:
        models = ConversationModel.query.filter_by(session_id=session_id).order_by(ConversationModel.created_at.desc()).all()
        return [_to_conversation_entity(model) for model in models]

    def get_active_conversation(self, user_id: Optional[int] = None, session_id: Optional[str] = None) -> Optional[Conversation]:
        query = ConversationModel.query.filter_by(is_active=True)
        
        if user_id:
            query = query.filter_by(user_id=user_id)
        if session_id:
            query = query.filter_by(session_id=session_id)
        
        model = query.first()
        return _to_conversation_entity(model) if model else None

    def get_conversations_with_message_count(self, limit: int = 50) -> List[dict]:
        # Obtener conversaciones con conteo de mensajes
        conversations = db.session.query(
            ConversationModel,
            db.func.count().label('message_count')
        ).outerjoin(
            ConversationModel.messages
        ).group_by(ConversationModel.id).order_by(
            ConversationModel.created_at.desc()
        ).limit(limit).all()
        
        result = []
        for conversation, message_count in conversations:
            result.append({
                'conversation': _to_conversation_entity(conversation),
                'message_count': message_count
            })
        
        return result
