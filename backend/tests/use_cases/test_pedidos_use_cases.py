from funcionalidades.pedidos.application.use_cases.crear_pedido_use_case import CrearPedidoUseCase
from funcionalidades.pedidos.application.use_cases.listar_pedidos_use_case import ListarPedidoseSUseCase
from funcionalidades.pedidos.infrastructure.pedido_repository_impl import PedidoRepositoryImpl


def test_crear_y_listar_pedido(app):
    from funcionalidades.categorias.infrastructure.categoria_model import CategoriaModel
    from funcionalidades.productos.infrastructure.producto_model import ProductoModel
    from funcionalidades.usuarios.infrastructure.usuario_model import UsuarioModel
    from funcionalidades.core.infraestructura.database import db
    from funcionalidades.core.infraestructura.security import hash_password
    
    # Crear usuario, categoría y producto primero
    import uuid
    usuario = UsuarioModel(username=f'testuser_{uuid.uuid4().hex[:8]}', 
                          email=f'test_{uuid.uuid4().hex[:8]}@test.com',
                          password_hash=hash_password('test123'),
                          rol='cliente')
    db.session.add(usuario)
    
    categoria = CategoriaModel(nombre=f'Test Category {uuid.uuid4().hex[:8]}', descripcion='Test', activa=True)
    db.session.add(categoria)
    db.session.commit()
    
    producto = ProductoModel(titulo='Test Product', precio=5.0, descripcion='Test', 
                           imagenes=[], categoria_id=categoria.id, activo=True)
    db.session.add(producto)
    db.session.commit()
    
    repo = PedidoRepositoryImpl()
    datos_facturacion = {"nombre": "Juan", "email": "juan@test.com"}
    p = CrearPedidoUseCase(repo).ejecutar(
        usuario_id=usuario.id, 
        items=[{'producto_id': producto.id, 'cantidad': 1, 'precio_unitario': 5.0}],
        datos_facturacion=datos_facturacion
    )
    items = ListarPedidoseSUseCase(repo).ejecutar()
    assert any(x.id == p.id for x in items)


