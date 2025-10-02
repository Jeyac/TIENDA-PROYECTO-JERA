from funcionalidades.productos.domain.entities.producto_entity import Producto
from funcionalidades.productos.domain.repositories.producto_repository import ProductoRepository
from funcionalidades.core.exceptions import NotFoundError


class ActualizarProductoUseCase:
    def __init__(self, repo: ProductoRepository):
        self.repo = repo

    def ejecutar(self, producto_id: int, titulo: str, precio: float, descripcion: str, imagenes: list, categoria_id: int, activo: bool = True) -> Producto:
        if not self.repo.get_by_id(producto_id):
            raise NotFoundError('Producto no encontrado')
        producto = Producto(id=producto_id, titulo=titulo, precio=precio, descripcion=descripcion, imagenes=imagenes, categoria_id=categoria_id, activo=activo)
        return self.repo.modificar(producto_id, producto)


