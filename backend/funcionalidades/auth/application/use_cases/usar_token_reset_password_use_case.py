from funcionalidades.auth.domain.repositories.password_reset_repository import PasswordResetRepository
from funcionalidades.core.exceptions import NotFoundError


class UsarTokenResetPasswordUseCase:
    def __init__(self, password_reset_repo: PasswordResetRepository):
        self.password_reset_repo = password_reset_repo

    def ejecutar(self, token: str) -> None:
        """Marcar token como usado"""
        password_reset = self.password_reset_repo.get_by_token(token)
        if not password_reset:
            raise NotFoundError('Token no encontrado')
        
        self.password_reset_repo.marcar_como_usado(token)
