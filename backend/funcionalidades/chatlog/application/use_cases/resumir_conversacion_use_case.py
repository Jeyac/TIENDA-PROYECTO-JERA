from funcionalidades.chatlog.domain.entities.conversation_entity import Conversation
from funcionalidades.chatlog.domain.repositories.conversation_repository import ConversationRepository
from funcionalidades.chatlog.domain.repositories.chat_message_repository import ChatMessageRepository
from funcionalidades.core.exceptions import NotFoundError


class ResumirConversacionUseCase:
    def __init__(self, conversation_repo: ConversationRepository, message_repo: ChatMessageRepository):
        self.conversation_repo = conversation_repo
        self.message_repo = message_repo

    def ejecutar(self, conversation_id: int, summary: str) -> Conversation:
        """Resumir una conversación"""
        # Verificar que la conversación existe
        conversation = self.conversation_repo.get_by_id(conversation_id)
        if not conversation:
            raise NotFoundError("Conversación no encontrada")
        
        # Crear conversación actualizada con resumen
        updated_conversation = Conversation(
            id=conversation.id,
            user_id=conversation.user_id,
            session_id=conversation.session_id,
            title=conversation.title,
            is_active=conversation.is_active,
            summary=summary,
            created_at=conversation.created_at,
            updated_at=None  # Se actualizará en el repositorio
        )
        
        return self.conversation_repo.modificar(conversation_id, updated_conversation)
