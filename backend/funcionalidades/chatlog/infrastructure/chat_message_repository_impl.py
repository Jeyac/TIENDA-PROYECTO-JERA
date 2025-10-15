from typing import List, Optional

from funcionalidades.core.infraestructura.database import db
from funcionalidades.chatlog.domain.entities.chat_message_entity import ChatMessage
from funcionalidades.chatlog.domain.repositories.chat_message_repository import ChatMessageRepository
from funcionalidades.chatlog.infrastructure.chat_message_model import ChatMessageModel


def _to_chat_message_entity(model: ChatMessageModel) -> ChatMessage:
    return ChatMessage(
        id=model.id,
        conversation_id=model.conversation_id,
        user_id=model.user_id,
        role=model.role,
        content=model.content,
        created_at=model.created_at
    )


def _to_chat_message_model(message: ChatMessage) -> ChatMessageModel:
    return ChatMessageModel(
        id=message.id,
        conversation_id=message.conversation_id,
        user_id=message.user_id,
        role=message.role,
        content=message.content,
        created_at=message.created_at
    )


class ChatMessageRepositoryImpl(ChatMessageRepository):
    def agregar(self, message: ChatMessage) -> ChatMessage:
        model = _to_chat_message_model(message)
        db.session.add(model)
        db.session.commit()
        return _to_chat_message_entity(model)

    def listar(self) -> List[ChatMessage]:
        models = ChatMessageModel.query.order_by(ChatMessageModel.created_at.desc()).all()
        return [_to_chat_message_entity(model) for model in models]

    def get_by_id(self, message_id: int) -> Optional[ChatMessage]:
        model = ChatMessageModel.query.get(message_id)
        return _to_chat_message_entity(model) if model else None

    def get_by_conversation_id(self, conversation_id: int) -> List[ChatMessage]:
        models = ChatMessageModel.query.filter_by(conversation_id=conversation_id).order_by(ChatMessageModel.created_at.asc()).all()
        return [_to_chat_message_entity(model) for model in models]

    def get_by_conversation_id_ordered(self, conversation_id: int, limit: Optional[int] = None) -> List[ChatMessage]:
        query = ChatMessageModel.query.filter_by(conversation_id=conversation_id).order_by(ChatMessageModel.created_at.asc())
        
        if limit:
            query = query.limit(limit)
        
        models = query.all()
        return [_to_chat_message_entity(model) for model in models]

    def get_recent_messages(self, conversation_id: int, limit: int = 10) -> List[ChatMessage]:
        models = ChatMessageModel.query.filter_by(conversation_id=conversation_id).order_by(ChatMessageModel.created_at.desc()).limit(limit).all()
        return [_to_chat_message_entity(model) for model in reversed(models)]

    def count_messages_in_conversation(self, conversation_id: int) -> int:
        return ChatMessageModel.query.filter_by(conversation_id=conversation_id).count()

    def get_messages_by_role(self, conversation_id: int, role: str) -> List[ChatMessage]:
        models = ChatMessageModel.query.filter_by(conversation_id=conversation_id, role=role).order_by(ChatMessageModel.created_at.asc()).all()
        return [_to_chat_message_entity(model) for model in models]
