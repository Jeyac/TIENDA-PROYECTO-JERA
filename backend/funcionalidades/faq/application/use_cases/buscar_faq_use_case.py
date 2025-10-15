from typing import List
from funcionalidades.faq.domain.entities.faq_entity import FAQ
from funcionalidades.faq.domain.repositories.faq_repository import FAQRepository


class BuscarFAQUseCase:
    def __init__(self, faq_repo: FAQRepository):
        self.faq_repo = faq_repo

    def ejecutar(self, palabra_clave: str) -> List[FAQ]:
        """Buscar preguntas frecuentes por palabra clave"""
        if not palabra_clave or not palabra_clave.strip():
            return []
        
        return self.faq_repo.buscar_por_palabra_clave(palabra_clave.strip())
