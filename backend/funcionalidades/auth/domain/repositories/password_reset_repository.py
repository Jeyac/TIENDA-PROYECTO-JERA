from abc import ABC, abstractmethod
from typing import Optional

from funcionalidades.auth.domain.entities.password_reset_entity import PasswordReset


class PasswordResetRepository(ABC):
    @abstractmethod
    def agregar(self, password_reset: PasswordReset) -> PasswordReset:
        raise NotImplementedError

    @abstractmethod
    def get_by_token(self, token: str) -> Optional[PasswordReset]:
        raise NotImplementedError

    @abstractmethod
    def get_by_user_id(self, user_id: int) -> list[PasswordReset]:
        raise NotImplementedError

    @abstractmethod
    def invalidar_tokens_usuario(self, user_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def marcar_como_usado(self, token: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def eliminar_tokens_expirados(self) -> int:
        raise NotImplementedError
