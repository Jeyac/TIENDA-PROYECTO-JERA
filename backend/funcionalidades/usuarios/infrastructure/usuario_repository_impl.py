from typing import List, Optional

from funcionalidades.core.infraestructura.database import db
from funcionalidades.usuarios.domain.entities.usuario_entity import Usuario
from funcionalidades.usuarios.domain.repositories.usuario_repository import UsuarioRepository
from funcionalidades.usuarios.infrastructure.usuario_model import UsuarioModel


def _to_entity(model: UsuarioModel) -> Usuario:
    return Usuario(
        id=model.id,
        username=model.username,
        email=model.email,
        password_hash=model.password_hash,
        rol=model.rol,
    )


class UsuarioRepositoryImpl(UsuarioRepository):
    def agregar(self, usuario: Usuario) -> Usuario:
        model = UsuarioModel(
            username=usuario.username,
            email=usuario.email,
            password_hash=usuario.password_hash,
            rol=usuario.rol,
        )
        db.session.add(model)
        db.session.commit()
        return _to_entity(model)

    def listar(self) -> List[Usuario]:
        return [_to_entity(m) for m in UsuarioModel.query.all()]

    def get_by_id(self, usuario_id: int) -> Optional[Usuario]:
        m = UsuarioModel.query.get(usuario_id)
        return _to_entity(m) if m else None

    def modificar(self, usuario_id: int, usuario: Usuario) -> Usuario:
        m = UsuarioModel.query.get(usuario_id)
        if not m:
            return None
        m.username = usuario.username
        m.email = usuario.email
        m.password_hash = usuario.password_hash
        m.rol = usuario.rol
        db.session.commit()
        return _to_entity(m)

    def eliminar(self, usuario_id: int) -> None:
        m = UsuarioModel.query.get(usuario_id)
        if m:
            db.session.delete(m)
            db.session.commit()

    def get_by_username(self, username: str) -> Optional[Usuario]:
        m = UsuarioModel.query.filter_by(username=username).first()
        return _to_entity(m) if m else None


