from abc import ABC, abstractmethod
from typing import List, Optional

from funcionalidades.faq.domain.entities.faq_entity import FAQ


class FAQRepository(ABC):
    @abstractmethod
    def listar(self) -> List[FAQ]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, faq_id: int) -> Optional[FAQ]:
        raise NotImplementedError

    @abstractmethod
    def buscar_por_palabra_clave(self, palabra_clave: str) -> List[FAQ]:
        raise NotImplementedError
