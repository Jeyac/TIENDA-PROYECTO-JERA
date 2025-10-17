from funcionalidades.core.infraestructura.security import hash_password
from funcionalidades.usuarios.domain.entities.usuario_entity import Usuario
from funcionalidades.usuarios.domain.repositories.usuario_repository import UsuarioRepository
from funcionalidades.core.exceptions import BadRequestError


class RegistrarUsuarioUseCase:
    def __init__(self, repo: UsuarioRepository):
        self.repo = repo

    def ejecutar(self, username: str, email: str, password: str, rol: str = 'cliente') -> Usuario:
        # Validaciones adicionales en el caso de uso
        username = username.strip()
        email = email.strip().lower()
        
        # Verificar si el usuario ya existe
        existing_user = self.repo.get_by_username(username)
        if existing_user:
            raise BadRequestError('El nombre de usuario ya está en uso')
        
        existing_email = self.repo.get_by_email(email)
        if existing_email:
            raise BadRequestError('El correo electrónico ya está registrado')
        
        # Crear el usuario
        password_hash = hash_password(password)
        usuario = Usuario(id=None, username=username, email=email, password_hash=password_hash, rol=rol)
        return self.repo.agregar(usuario)










