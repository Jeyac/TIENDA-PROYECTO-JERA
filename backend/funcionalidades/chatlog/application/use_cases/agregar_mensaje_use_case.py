from funcionalidades.chatlog.domain.entities.chat_message_entity import ChatMessage
from funcionalidades.chatlog.domain.repositories.chat_message_repository import ChatMessageRepository
from funcionalidades.chatlog.domain.repositories.conversation_repository import ConversationRepository
from funcionalidades.core.exceptions import NotFoundError


class AgregarMensajeUseCase:
    def __init__(self, message_repo: ChatMessageRepository, conversation_repo: ConversationRepository):
        self.message_repo = message_repo
        self.conversation_repo = conversation_repo

    def ejecutar(
        self,
        conversation_id: int,
        role: str,
        content: str,
        user_id: int = None
    ) -> ChatMessage:
        """Agregar un mensaje a una conversación"""
        # Verificar que la conversación existe
        conversation = self.conversation_repo.get_by_id(conversation_id)
        if not conversation:
            raise NotFoundError("Conversación no encontrada")
        
        # Crear entidad del dominio
        message = ChatMessage(
            id=None,
            conversation_id=conversation_id,
            user_id=user_id,
            role=role,
            content=content,
            created_at=None
        )
        
        return self.message_repo.agregar(message)
