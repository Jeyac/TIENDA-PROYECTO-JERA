from abc import ABC, abstractmethod
from typing import List, Optional

from funcionalidades.usuarios.domain.entities.usuario_entity import Usuario


class UsuarioRepository(ABC):
    @abstractmethod
    def agregar(self, usuario: Usuario) -> Usuario:
        raise NotImplementedError

    @abstractmethod
    def listar(self) -> List[Usuario]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, usuario_id: int) -> Optional[Usuario]:
        raise NotImplementedError

    @abstractmethod
    def modificar(self, usuario_id: int, usuario: Usuario) -> Usuario:
        raise NotImplementedError

    @abstractmethod
    def eliminar(self, usuario_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[Usuario]:
        raise NotImplementedError


