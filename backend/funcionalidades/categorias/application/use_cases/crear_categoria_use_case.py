from funcionalidades.categorias.domain.entities.categoria_entity import Categoria
from funcionalidades.categorias.domain.repositories.categoria_repository import CategoriaRepository


class CrearCategoriaUseCase:
    def __init__(self, repo: CategoriaRepository):
        self.repo = repo

    def ejecutar(self, nombre: str, descripcion: str, activa: bool = True) -> Categoria:
        categoria = Categoria(id=None, nombre=nombre, descripcion=descripcion, activa=activa)
        return self.repo.agregar(categoria)