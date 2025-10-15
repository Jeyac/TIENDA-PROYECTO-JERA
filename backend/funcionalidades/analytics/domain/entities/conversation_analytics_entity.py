from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime


@dataclass(frozen=True)
class ConversationAnalytics:
    total_conversations: int
    active_conversations: int
    total_messages: int
    user_messages: int
    bot_messages: int
    avg_messages_per_conversation: float
    most_common_topics: List[Dict[str, Any]]
    most_common_responses: List[Dict[str, Any]]
    conversations_by_day: List[Dict[str, Any]]
    response_time_stats: Dict[str, Any]


@dataclass(frozen=True)
class TicketAnalytics:
    total_tickets: int
    open_tickets: int
    closed_tickets: int
    resolved_tickets: int
    tickets_by_priority: Dict[str, int]
    tickets_by_category: Dict[str, int]
    tickets_by_status: Dict[str, int]
    avg_resolution_time: float
    tickets_by_day: List[Dict[str, Any]]


@dataclass(frozen=True)
class MessageAnalytics:
    total_messages: int
    messages_by_role: Dict[str, int]
    messages_by_day: List[Dict[str, Any]]
    avg_message_length: float
    most_common_words: List[Dict[str, Any]]
