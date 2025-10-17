from typing import List, Optional

from funcionalidades.core.infraestructura.database import db
from funcionalidades.productos.domain.entities.producto_entity import Producto
from funcionalidades.productos.domain.repositories.producto_repository import ProductoRepository
from funcionalidades.productos.infrastructure.producto_model import ProductoModel


def _to_entity(model: ProductoModel) -> Producto:
    return Producto(
        id=model.id,
        titulo=model.titulo,
        precio=model.precio,
        descripcion=model.descripcion,
        imagenes=model.imagenes or [],
        categoria_id=model.categoria_id,
        activo=model.activo,
    )


class ProductoRepositoryImpl(ProductoRepository):
    def agregar(self, producto: Producto) -> Producto:
        model = ProductoModel(
            titulo=producto.titulo,
            precio=producto.precio,
            descripcion=producto.descripcion,
            imagenes=producto.imagenes,
            categoria_id=producto.categoria_id,
            activo=producto.activo,
        )
        db.session.add(model)
        db.session.commit()
        return _to_entity(model)

    def listar(self) -> List[Producto]:
        return [_to_entity(m) for m in ProductoModel.query.all()]

    def get_by_id(self, producto_id: int) -> Optional[Producto]:
        model = ProductoModel.query.get(producto_id)
        return _to_entity(model) if model else None

    def modificar(self, producto_id: int, producto: Producto) -> Producto:
        model = ProductoModel.query.get(producto_id)
        if not model:
            return None  # manejado en use case
        model.titulo = producto.titulo
        model.precio = producto.precio
        model.descripcion = producto.descripcion
        model.imagenes = producto.imagenes
        model.categoria_id = producto.categoria_id
        model.activo = producto.activo
        db.session.commit()
        return _to_entity(model)

    def eliminar(self, producto_id: int) -> None:
        model = ProductoModel.query.get(producto_id)
        if model:
            print(f"Eliminando producto {producto_id}: {model.titulo}")
            db.session.delete(model)
            db.session.commit()
            print(f"Producto {producto_id} eliminado exitosamente")
        else:
            print(f"Producto {producto_id} no encontrado para eliminar")


