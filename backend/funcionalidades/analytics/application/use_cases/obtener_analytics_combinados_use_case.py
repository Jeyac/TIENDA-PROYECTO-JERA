from datetime import datetime, timedelta
from typing import Dict, Any
from funcionalidades.analytics.domain.repositories.analytics_repository import AnalyticsRepository


class ObtenerAnalyticsCombinadosUseCase:
    def __init__(self, analytics_repo: AnalyticsRepository):
        self.analytics_repo = analytics_repo

    def ejecutar(self, days: int = 30) -> Dict[str, Any]:
        """Obtener analítica combinada de conversaciones, tickets y mensajes"""
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        return self.analytics_repo.get_combined_analytics(start_date, end_date)
