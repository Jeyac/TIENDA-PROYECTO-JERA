from datetime import datetime, timedelta
from funcionalidades.analytics.domain.entities.conversation_analytics_entity import ConversationAnalytics
from funcionalidades.analytics.domain.repositories.analytics_repository import AnalyticsRepository


class ObtenerAnalyticsConversacionesUseCase:
    def __init__(self, analytics_repo: AnalyticsRepository):
        self.analytics_repo = analytics_repo

    def ejecutar(self, days: int = 30) -> ConversationAnalytics:
        """Obtener analítica de conversaciones"""
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        return self.analytics_repo.get_conversation_analytics(start_date, end_date)
