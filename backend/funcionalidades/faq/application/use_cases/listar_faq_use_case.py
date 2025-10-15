from typing import List
from funcionalidades.faq.domain.entities.faq_entity import FAQ
from funcionalidades.faq.domain.repositories.faq_repository import FAQRepository


class ListarFAQUseCase:
    def __init__(self, faq_repo: FAQRepository):
        self.faq_repo = faq_repo

    def ejecutar(self) -> List[FAQ]:
        """Listar todas las preguntas frecuentes"""
        return self.faq_repo.listar()
