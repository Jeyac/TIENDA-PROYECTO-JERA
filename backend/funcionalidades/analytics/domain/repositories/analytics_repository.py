from abc import ABC, abstractmethod
from typing import Dict, Any
from datetime import datetime

from funcionalidades.analytics.domain.entities.conversation_analytics_entity import (
    ConversationAnalytics, TicketAnalytics, MessageAnalytics
)


class AnalyticsRepository(ABC):
    @abstractmethod
    def get_conversation_analytics(self, start_date: datetime, end_date: datetime) -> ConversationAnalytics:
        raise NotImplementedError

    @abstractmethod
    def get_ticket_analytics(self, start_date: datetime, end_date: datetime) -> TicketAnalytics:
        raise NotImplementedError

    @abstractmethod
    def get_message_analytics(self, start_date: datetime, end_date: datetime) -> MessageAnalytics:
        raise NotImplementedError

    @abstractmethod
    def get_combined_analytics(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        raise NotImplementedError
