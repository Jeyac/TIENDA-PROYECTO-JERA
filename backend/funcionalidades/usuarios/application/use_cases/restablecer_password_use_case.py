from funcionalidades.core.exceptions import NotFoundError, BadRequestError
from funcionalidades.core.infraestructura.security import hash_password
from funcionalidades.usuarios.domain.entities.usuario_entity import Usuario
from funcionalidades.usuarios.domain.repositories.usuario_repository import UsuarioRepository


class RestablecerPasswordUseCase:
    def __init__(self, repo: UsuarioRepository):
        self.repo = repo

    def ejecutar(self, username: str, new_password: str) -> Usuario:
        if not new_password:
            raise BadRequestError('Nueva contraseña requerida')
        user = self.repo.get_by_username(username)
        if not user:
            raise NotFoundError('Usuario no encontrado')
        actualizado = Usuario(
            id=user.id,
            username=user.username,
            email=user.email,
            password_hash=hash_password(new_password),
            rol=user.rol,
        )
        return self.repo.modificar(user.id, actualizado)


