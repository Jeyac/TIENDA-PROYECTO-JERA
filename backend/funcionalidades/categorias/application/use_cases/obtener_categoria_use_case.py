from funcionalidades.core.exceptions import NotFoundError
from funcionalidades.categorias.domain.entities.categoria_entity import Categoria
from funcionalidades.categorias.domain.repositories.categoria_repository import CategoriaRepository


class ObtenerCategoriaUseCase:
    def __init__(self, repo: CategoriaRepository):
        self.repo = repo

    def ejecutar(self, categoria_id: int) -> Categoria:
        categoria = self.repo.get_by_id(categoria_id)
        if not categoria:
            raise NotFoundError('Categoría no encontrada')
        return categoria