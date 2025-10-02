from funcionalidades.core.exceptions import NotFoundError
from funcionalidades.categorias.domain.entities.categoria_entity import Categoria
from funcionalidades.categorias.domain.repositories.categoria_repository import CategoriaRepository


class ActualizarCategoriaUseCase:
    def __init__(self, repo: CategoriaRepository):
        self.repo = repo

    def ejecutar(self, categoria_id: int, nombre: str, descripcion: str, activa: bool = True) -> Categoria:
        if not self.repo.get_by_id(categoria_id):
            raise NotFoundError('Categoría no encontrada')
        categoria = Categoria(id=categoria_id, nombre=nombre, descripcion=descripcion, activa=activa)
        return self.repo.modificar(categoria_id, categoria)