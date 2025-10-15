from abc import ABC, abstractmethod
from typing import List, Optional

from funcionalidades.chatlog.domain.entities.chat_message_entity import ChatMessage


class ChatMessageRepository(ABC):
    @abstractmethod
    def agregar(self, message: ChatMessage) -> ChatMessage:
        raise NotImplementedError

    @abstractmethod
    def listar(self) -> List[ChatMessage]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, message_id: int) -> Optional[ChatMessage]:
        raise NotImplementedError

    @abstractmethod
    def get_by_conversation_id(self, conversation_id: int) -> List[ChatMessage]:
        raise NotImplementedError

    @abstractmethod
    def get_by_conversation_id_ordered(self, conversation_id: int, limit: Optional[int] = None) -> List[ChatMessage]:
        raise NotImplementedError

    @abstractmethod
    def get_recent_messages(self, conversation_id: int, limit: int = 10) -> List[ChatMessage]:
        raise NotImplementedError

    @abstractmethod
    def count_messages_in_conversation(self, conversation_id: int) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_messages_by_role(self, conversation_id: int, role: str) -> List[ChatMessage]:
        raise NotImplementedError
