from funcionalidades.auth.domain.entities.password_reset_entity import PasswordReset
from funcionalidades.auth.infrastructure.email_service import EmailService
from funcionalidades.core.exceptions import BadRequestError


class EnviarEmailResetPasswordUseCase:
    def __init__(self, email_service: EmailService):
        self.email_service = email_service

    def ejecutar(self, password_reset: PasswordReset, username: str, email: str) -> bool:
        """Enviar email de reset de contraseña"""
        if not password_reset:
            raise BadRequestError('El token de reset es requerido')
        
        if not username or not username.strip():
            raise BadRequestError('El nombre de usuario es requerido')
        
        if not email or not email.strip():
            raise BadRequestError('El email es requerido')
        
        return self.email_service.send_password_reset_email(
            to_email=email,
            username=username,
            reset_token=password_reset.token
        )
