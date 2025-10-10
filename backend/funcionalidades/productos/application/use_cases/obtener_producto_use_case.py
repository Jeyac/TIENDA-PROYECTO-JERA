from funcionalidades.core.exceptions import NotFoundError
from funcionalidades.productos.domain.entities.producto_entity import Producto
from funcionalidades.productos.domain.repositories.producto_repository import ProductoRepository


class ObtenerProductoUseCase:
    def __init__(self, repo: ProductoRepository):
        self.repo = repo

    def ejecutar(self, producto_id: int) -> Producto:
        producto = self.repo.get_by_id(producto_id)
        if not producto:
            raise NotFoundError('Producto no encontrado')
        return producto






