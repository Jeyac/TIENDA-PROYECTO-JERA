from funcionalidades.core.infraestructura.security import hash_password
from funcionalidades.usuarios.domain.entities.usuario_entity import Usuario
from funcionalidades.usuarios.domain.repositories.usuario_repository import UsuarioRepository


class RegistrarUsuarioUseCase:
    def __init__(self, repo: UsuarioRepository):
        self.repo = repo

    def ejecutar(self, username: str, email: str, password: str, rol: str = 'cliente') -> Usuario:
        password_hash = hash_password(password)
        usuario = Usuario(id=None, username=username, email=email, password_hash=password_hash, rol=rol)
        return self.repo.agregar(usuario)






