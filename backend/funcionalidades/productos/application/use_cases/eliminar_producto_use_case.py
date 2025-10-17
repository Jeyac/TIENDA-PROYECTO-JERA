from funcionalidades.productos.domain.repositories.producto_repository import ProductoRepository
from funcionalidades.core.exceptions import NotFoundError


class EliminarProductoUseCase:
    def __init__(self, repo: ProductoRepository):
        self.repo = repo

    def ejecutar(self, producto_id: int) -> None:
        # Verificar si el producto existe antes de eliminarlo
        producto = self.repo.get_by_id(producto_id)
        if not producto:
            raise NotFoundError('Producto no encontrado')
        
        # Eliminar el producto
        self.repo.eliminar(producto_id)


