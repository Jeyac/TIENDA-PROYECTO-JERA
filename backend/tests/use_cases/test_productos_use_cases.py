from funcionalidades.productos.application.use_cases.crear_producto_use_case import CrearProductoUseCase
from funcionalidades.productos.application.use_cases.listar_productos_use_case import ListarProductosesUseCase
from funcionalidades.productos.infrastructure.producto_repository_impl import ProductoRepositoryImpl


def test_crear_y_listar_producto(app):
    from funcionalidades.categorias.infrastructure.categoria_model import CategoriaModel
    from funcionalidades.core.infraestructura.database import db
    
    # Crear categoría primero
    import uuid
    categoria = CategoriaModel(nombre=f'Test Category {uuid.uuid4().hex[:8]}', descripcion='Test', activa=True)
    db.session.add(categoria)
    db.session.commit()
    
    repo = ProductoRepositoryImpl()
    # Notar: estos tests son de integración ligera, requieren DB (SQLite fallback)
    p = CrearProductoUseCase(repo).ejecutar('Prod', 10.0, 'desc', [], categoria_id=categoria.id)
    items = ListarProductosesUseCase(repo).ejecutar()
    assert any(x.titulo == 'Prod' for x in items)


