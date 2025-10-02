from typing import List, Optional

from funcionalidades.core.infraestructura.database import db
from funcionalidades.categorias.domain.entities.categoria_entity import Categoria
from funcionalidades.categorias.domain.repositories.categoria_repository import CategoriaRepository
from funcionalidades.categorias.infrastructure.categoria_model import CategoriaModel


def _to_entity(model: CategoriaModel) -> Categoria:
    return Categoria(
        id=model.id,
        nombre=model.nombre,
        descripcion=model.descripcion,
        activa=model.activa,
    )


class CategoriaRepositoryImpl(CategoriaRepository):
    def agregar(self, categoria: Categoria) -> Categoria:
        model = CategoriaModel(
            nombre=categoria.nombre,
            descripcion=categoria.descripcion,
            activa=categoria.activa,
        )
        db.session.add(model)
        db.session.commit()
        return _to_entity(model)

    def listar(self) -> List[Categoria]:
        return [_to_entity(m) for m in CategoriaModel.query.all()]

    def get_by_id(self, categoria_id: int) -> Optional[Categoria]:
        m = CategoriaModel.query.get(categoria_id)
        return _to_entity(m) if m else None

    def modificar(self, categoria_id: int, categoria: Categoria) -> Categoria:
        m = CategoriaModel.query.get(categoria_id)
        if not m:
            return None
        m.nombre = categoria.nombre
        m.descripcion = categoria.descripcion
        m.activa = categoria.activa
        db.session.commit()
        return _to_entity(m)

    def eliminar(self, categoria_id: int) -> None:
        m = CategoriaModel.query.get(categoria_id)
        if m:
            db.session.delete(m)
            db.session.commit()

    def get_by_nombre(self, nombre: str) -> Optional[Categoria]:
        m = CategoriaModel.query.filter_by(nombre=nombre).first()
        return _to_entity(m) if m else None