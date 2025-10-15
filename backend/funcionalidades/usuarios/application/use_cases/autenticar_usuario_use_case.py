from funcionalidades.core.exceptions import NotFoundError, BadRequestError
from funcionalidades.core.infraestructura.security import verify_password
from funcionalidades.usuarios.domain.repositories.usuario_repository import UsuarioRepository
from funcionalidades.usuarios.domain.entities.usuario_entity import Usuario


class AutenticarUsuarioUseCase:
    def __init__(self, repo: UsuarioRepository):
        self.repo = repo

    def ejecutar(self, username_or_email: str, password: str) -> Usuario:
        print(f"DEBUG: Autenticando usuario: {username_or_email}")
        
        # Intentar buscar por username primero
        usuario = self.repo.get_by_username(username_or_email)
        print(f"DEBUG: Usuario encontrado por username: {usuario}")
        
        # Si no se encuentra por username, intentar por email
        if not usuario:
            usuario = self.repo.get_by_email(username_or_email)
            print(f"DEBUG: Usuario encontrado por email: {usuario}")
        
        if not usuario:
            print("DEBUG: Usuario no encontrado")
            raise NotFoundError('Usuario no encontrado')
        
        print(f"DEBUG: Usuario encontrado - ID: {usuario.id}, Username: {usuario.username}, Activo: {usuario.activo}")
        
        # Verificar que el usuario esté activo
        if not usuario.activo:
            print("DEBUG: Usuario inactivo")
            raise BadRequestError('Usuario inactivo. Contacta al administrador.')
        
        print(f"DEBUG: Verificando contraseña...")
        if not verify_password(password, usuario.password_hash):
            print("DEBUG: Contraseña incorrecta")
            raise BadRequestError('Credenciales inválidas')
        
        print("DEBUG: Autenticación exitosa")
        return usuario


