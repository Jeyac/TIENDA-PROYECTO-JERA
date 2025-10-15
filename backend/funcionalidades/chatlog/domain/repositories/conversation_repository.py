from abc import ABC, abstractmethod
from typing import List, Optional

from funcionalidades.chatlog.domain.entities.conversation_entity import Conversation


class ConversationRepository(ABC):
    @abstractmethod
    def agregar(self, conversation: Conversation) -> Conversation:
        raise NotImplementedError

    @abstractmethod
    def listar(self) -> List[Conversation]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, conversation_id: int) -> Optional[Conversation]:
        raise NotImplementedError

    @abstractmethod
    def modificar(self, conversation_id: int, conversation: Conversation) -> Conversation:
        raise NotImplementedError

    @abstractmethod
    def eliminar(self, conversation_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_by_user_id(self, user_id: int) -> List[Conversation]:
        raise NotImplementedError

    @abstractmethod
    def get_by_session_id(self, session_id: str) -> List[Conversation]:
        raise NotImplementedError

    @abstractmethod
    def get_active_conversation(self, user_id: Optional[int] = None, session_id: Optional[str] = None) -> Optional[Conversation]:
        raise NotImplementedError

    @abstractmethod
    def get_conversations_with_message_count(self, limit: int = 50) -> List[dict]:
        raise NotImplementedError
