from typing import List, Optional
from funcionalidades.chatlog.domain.entities.chat_message_entity import ChatMessage
from funcionalidades.chatlog.domain.repositories.chat_message_repository import ChatMessageRepository
from funcionalidades.chatlog.domain.repositories.conversation_repository import ConversationRepository
from funcionalidades.core.exceptions import NotFoundError


class ObtenerMensajesConversacionUseCase:
    def __init__(self, message_repo: ChatMessageRepository, conversation_repo: ConversationRepository):
        self.message_repo = message_repo
        self.conversation_repo = conversation_repo

    def ejecutar(
        self,
        conversation_id: int,
        limit: Optional[int] = None
    ) -> List[ChatMessage]:
        """Obtener mensajes de una conversación"""
        # Verificar que la conversación existe
        conversation = self.conversation_repo.get_by_id(conversation_id)
        if not conversation:
            raise NotFoundError("Conversación no encontrada")
        
        return self.message_repo.get_by_conversation_id_ordered(conversation_id, limit)
