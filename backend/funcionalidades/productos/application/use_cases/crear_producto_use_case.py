from funcionalidades.productos.domain.entities.producto_entity import Producto
from funcionalidades.productos.domain.repositories.producto_repository import ProductoRepository


class CrearProductoUseCase:
    def __init__(self, repo: ProductoRepository):
        self.repo = repo

    def ejecutar(self, titulo: str, precio: float, descripcion: str, imagenes: list, categoria_id: int, activo: bool = True) -> Producto:
        producto = Producto(id=None, titulo=titulo, precio=precio, descripcion=descripcion, imagenes=imagenes, categoria_id=categoria_id, activo=activo)
        return self.repo.agregar(producto)


