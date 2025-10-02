from typing import List

from funcionalidades.categorias.domain.entities.categoria_entity import Categoria
from funcionalidades.categorias.domain.repositories.categoria_repository import CategoriaRepository


class ListarCategoriasUseCase:
    def __init__(self, repo: CategoriaRepository):
        self.repo = repo

    def ejecutar(self) -> List[Categoria]:
        return self.repo.listar()