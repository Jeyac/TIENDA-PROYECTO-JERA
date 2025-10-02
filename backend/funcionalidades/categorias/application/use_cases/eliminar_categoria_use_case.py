from funcionalidades.core.exceptions import NotFoundError
from funcionalidades.categorias.domain.repositories.categoria_repository import CategoriaRepository


class EliminarCategoriaUseCase:
    def __init__(self, repo: CategoriaRepository):
        self.repo = repo

    def ejecutar(self, categoria_id: int) -> None:
        if not self.repo.get_by_id(categoria_id):
            raise NotFoundError('Categoría no encontrada')
        self.repo.eliminar(categoria_id)