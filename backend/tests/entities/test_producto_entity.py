import pytest

from funcionalidades.productos.domain.entities.producto_entity import Producto
from funcionalidades.core.exceptions import BadRequestError


def test_producto_valido():
    p = Producto(id=None, titulo='A', precio=1.0, descripcion='desc', imagenes=['a.jpg'], categoria_id=1, activo=True)
    assert p.titulo == 'A'
    assert p.precio == 1.0


@pytest.mark.parametrize('titulo', ['', '   ', None])
def test_producto_titulo_invalido(titulo):
    with pytest.raises(BadRequestError):
        Producto(id=None, titulo=titulo, precio=1.0, descripcion='d', imagenes=[], categoria_id=1, activo=True)


@pytest.mark.parametrize('precio', [-1, -0.01])
def test_producto_precio_invalido(precio):
    with pytest.raises(BadRequestError):
        Producto(id=None, titulo='A', precio=precio, descripcion='d', imagenes=[], categoria_id=1, activo=True)


def test_producto_imagenes_debe_ser_lista():
    with pytest.raises(BadRequestError):
        Producto(id=None, titulo='A', precio=0, descripcion='d', imagenes='no-lista', categoria_id=1, activo=True)


