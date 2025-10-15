import pytest

from funcionalidades.usuarios.domain.entities.usuario_entity import Usuario
from funcionalidades.core.exceptions import BadRequestError


def test_usuario_valido():
    u = Usuario(id=None, username='user', email='user@mail.com', password_hash='hash', rol='cliente')
    assert u.username == 'user'


@pytest.mark.parametrize('email', ['mail', 'user@mail', ''])
def test_usuario_email_invalido(email):
    with pytest.raises(BadRequestError):
        Usuario(id=None, username='u', email=email, password_hash='h', rol='cliente')


@pytest.mark.parametrize('rol', ['admin', 'root', ''])
def test_usuario_rol_invalido(rol):
    with pytest.raises(BadRequestError):
        Usuario(id=None, username='u', email='u@mail.com', password_hash='h', rol=rol)










