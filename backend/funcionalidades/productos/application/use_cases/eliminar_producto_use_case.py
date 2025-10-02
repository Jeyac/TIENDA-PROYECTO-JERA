from funcionalidades.productos.domain.repositories.producto_repository import ProductoRepository
from funcionalidades.core.exceptions import NotFoundError


class EliminarProductoUseCase:
    def __init__(self, repo: ProductoRepository):
        self.repo = repo

    def ejecutar(self, producto_id: int) -> None:
        if not self.repo.get_by_id(producto_id):
            raise NotFoundError('Producto no encontrado')
        self.repo.eliminar(producto_id)


