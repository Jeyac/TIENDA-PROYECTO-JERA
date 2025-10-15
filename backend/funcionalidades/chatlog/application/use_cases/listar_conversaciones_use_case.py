from typing import List, Optional
from funcionalidades.chatlog.domain.entities.conversation_entity import Conversation
from funcionalidades.chatlog.domain.repositories.conversation_repository import ConversationRepository


class ListarConversacionesUseCase:
    def __init__(self, conversation_repo: ConversationRepository):
        self.conversation_repo = conversation_repo

    def ejecutar(
        self,
        user_id: Optional[int] = None,
        session_id: Optional[str] = None,
        limit: int = 50
    ) -> List[Conversation]:
        """Listar conversaciones con filtros opcionales"""
        if user_id:
            return self.conversation_repo.get_by_user_id(user_id)
        elif session_id:
            return self.conversation_repo.get_by_session_id(session_id)
        else:
            return self.conversation_repo.listar()[:limit]
