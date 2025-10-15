from datetime import datetime
from funcionalidades.chatlog.domain.entities.conversation_entity import Conversation
from funcionalidades.chatlog.domain.repositories.conversation_repository import ConversationRepository
from funcionalidades.core.exceptions import NotFoundError


class CrearConversacionUseCase:
    def __init__(self, conversation_repo: ConversationRepository):
        self.conversation_repo = conversation_repo

    def ejecutar(
        self,
        user_id: int = None,
        session_id: str = None,
        title: str = None
    ) -> Conversation:
        """Crear una nueva conversación"""
        # Generar título si no se proporciona
        if not title:
            title = f"Conversación {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}"
        
        # Crear entidad del dominio
        conversation = Conversation(
            id=None,
            user_id=user_id,
            session_id=session_id,
            title=title,
            is_active=True,
            summary=None,
            created_at=None,
            updated_at=None
        )
        
        return self.conversation_repo.agregar(conversation)
