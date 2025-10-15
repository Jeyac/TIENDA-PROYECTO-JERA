from funcionalidades.chatlog.domain.entities.conversation_entity import Conversation
from funcionalidades.chatlog.domain.repositories.conversation_repository import ConversationRepository
from funcionalidades.core.exceptions import NotFoundError


class ObtenerConversacionUseCase:
    def __init__(self, conversation_repo: ConversationRepository):
        self.conversation_repo = conversation_repo

    def ejecutar(self, conversation_id: int) -> Conversation:
        """Obtener una conversación por ID"""
        conversation = self.conversation_repo.get_by_id(conversation_id)
        if not conversation:
            raise NotFoundError("Conversación no encontrada")
        return conversation
