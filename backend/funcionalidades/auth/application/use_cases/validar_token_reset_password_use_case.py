from funcionalidades.auth.domain.entities.password_reset_entity import PasswordReset
from funcionalidades.auth.domain.repositories.password_reset_repository import PasswordResetRepository
from funcionalidades.core.exceptions import NotFoundError, BadRequestError


class ValidarTokenResetPasswordUseCase:
    def __init__(self, password_reset_repo: PasswordResetRepository):
        self.password_reset_repo = password_reset_repo

    def ejecutar(self, token: str) -> PasswordReset:
        """Validar token de reset de contraseña"""
        if not token or not token.strip():
            raise BadRequestError('El token es requerido')
        
        password_reset = self.password_reset_repo.get_by_token(token)
        if not password_reset:
            raise NotFoundError('Token no encontrado')
        
        if not password_reset.is_valid():
            if password_reset.used:
                raise BadRequestError('El token ya ha sido utilizado')
            elif password_reset.is_expired():
                raise BadRequestError('El token ha expirado')
        
        return password_reset
