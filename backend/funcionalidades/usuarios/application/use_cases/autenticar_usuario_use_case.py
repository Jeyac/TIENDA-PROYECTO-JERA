from funcionalidades.core.exceptions import NotFoundError, BadRequestError
from funcionalidades.core.infraestructura.security import verify_password
from funcionalidades.usuarios.domain.repositories.usuario_repository import UsuarioRepository
from funcionalidades.usuarios.domain.entities.usuario_entity import Usuario


class AutenticarUsuarioUseCase:
    def __init__(self, repo: UsuarioRepository):
        self.repo = repo

    def ejecutar(self, username: str, password: str) -> Usuario:
        usuario = self.repo.get_by_username(username)
        if not usuario:
            raise NotFoundError('Usuario no encontrado')
        if not verify_password(password, usuario.password_hash):
            raise BadRequestError('Credenciales inválidas')
        return usuario


