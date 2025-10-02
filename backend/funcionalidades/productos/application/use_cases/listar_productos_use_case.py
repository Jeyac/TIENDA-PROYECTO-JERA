from typing import List

from funcionalidades.productos.domain.entities.producto_entity import Producto
from funcionalidades.productos.domain.repositories.producto_repository import ProductoRepository


class ListarProductosesUseCase:
    def __init__(self, repo: ProductoRepository):
        self.repo = repo

    def ejecutar(self) -> List[Producto]:
        return self.repo.listar()


