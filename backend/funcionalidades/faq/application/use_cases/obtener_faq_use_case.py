from funcionalidades.faq.domain.entities.faq_entity import FAQ
from funcionalidades.faq.domain.repositories.faq_repository import FAQRepository
from funcionalidades.core.exceptions import NotFoundError


class ObtenerFAQUseCase:
    def __init__(self, faq_repo: FAQRepository):
        self.faq_repo = faq_repo

    def ejecutar(self, faq_id: int) -> FAQ:
        """Obtener una pregunta frecuente por ID"""
        faq = self.faq_repo.get_by_id(faq_id)
        if not faq:
            raise NotFoundError("FAQ no encontrado")
        return faq
