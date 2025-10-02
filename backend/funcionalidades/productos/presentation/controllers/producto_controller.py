from flask import Blueprint, jsonify, request

from funcionalidades.core.infraestructura.auth import jwt_required
from funcionalidades.core.exceptions import BadRequestError, NotFoundError
from funcionalidades.productos.application.use_cases.crear_producto_use_case import CrearProductoUseCase
from funcionalidades.productos.application.use_cases.listar_productos_use_case import ListarProductosesUseCase
from funcionalidades.productos.application.use_cases.obtener_producto_use_case import ObtenerProductoUseCase
from funcionalidades.productos.application.use_cases.actualizar_producto_use_case import ActualizarProductoUseCase
from funcionalidades.productos.application.use_cases.eliminar_producto_use_case import EliminarProductoUseCase
from funcionalidades.productos.infrastructure.producto_repository_impl import ProductoRepositoryImpl
from funcionalidades.core.infraestructura.database import db


productos_bp = Blueprint('productos', __name__)
repo = ProductoRepositoryImpl()


@productos_bp.post('/')
@jwt_required(roles={'administrador'})
def crear_producto():
    data = request.get_json(silent=True) or {}
    try:
        use_case = CrearProductoUseCase(repo)
        producto = use_case.ejecutar(
            titulo=data.get('titulo'),
            precio=data.get('precio'),
            descripcion=data.get('descripcion', ''),
            imagenes=data.get('imagenes', []),
            categoria_id=data.get('categoria_id'),
            activo=data.get('activo', True),
        )
        return jsonify(producto.__dict__), 201
    except BadRequestError as exc:
        return jsonify({'message': str(exc)}), 400


@productos_bp.get('/')
def listar_productos():
    # Público: solo productos activos
    from funcionalidades.productos.infrastructure.producto_model import ProductoModel
    categoria_id = request.args.get('categoria_id')
    busqueda = request.args.get('q')
    
    query = ProductoModel.query.filter_by(activo=True)
    if categoria_id:
        query = query.filter_by(categoria_id=categoria_id)
    if busqueda:
        query = query.filter(ProductoModel.titulo.ilike(f'%{busqueda}%'))
    
    items = []
    for p in query.all():
        from funcionalidades.categorias.infrastructure.categoria_model import CategoriaModel
        categoria = CategoriaModel.query.get(p.categoria_id)
        items.append({
            'id': p.id,
            'titulo': p.titulo,
            'precio': p.precio,
            'descripcion': p.descripcion,
            'imagenes': p.imagenes or [],
            'categoria_id': p.categoria_id,
            'categoria_nombre': categoria.nombre if categoria else 'Sin categoría',
            'activo': p.activo
        })
    return jsonify(items)


@productos_bp.get('/<int:producto_id>')
def obtener_producto(producto_id: int):
    # Público: solo productos activos
    from funcionalidades.productos.infrastructure.producto_model import ProductoModel
    p = ProductoModel.query.filter_by(id=producto_id, activo=True).first()
    if not p:
        return jsonify({'message': 'Producto no encontrado'}), 404
    from funcionalidades.categorias.infrastructure.categoria_model import CategoriaModel
    categoria = CategoriaModel.query.get(p.categoria_id)
    return jsonify({
        'id': p.id,
        'titulo': p.titulo,
        'precio': p.precio,
        'descripcion': p.descripcion,
        'imagenes': p.imagenes or [],
        'categoria_id': p.categoria_id,
        'categoria_nombre': categoria.nombre if categoria else 'Sin categoría',
        'activo': p.activo
    })


@productos_bp.put('/<int:producto_id>')
@jwt_required(roles={'administrador'})
def actualizar_producto(producto_id: int):
    data = request.get_json(silent=True) or {}
    try:
        use_case = ActualizarProductoUseCase(repo)
        p = use_case.ejecutar(
            producto_id, 
            data.get('titulo'), 
            data.get('precio'), 
            data.get('descripcion', ''), 
            data.get('imagenes', []),
            data.get('categoria_id'),
            data.get('activo', True)
        )
        return jsonify(p.__dict__)
    except NotFoundError as exc:
        return jsonify({'message': str(exc)}), 404
    except BadRequestError as exc:
        return jsonify({'message': str(exc)}), 400


@productos_bp.delete('/<int:producto_id>')
@jwt_required(roles={'administrador'})
def eliminar_producto(producto_id: int):
    try:
        use_case = EliminarProductoUseCase(repo)
        use_case.ejecutar(producto_id)
        return jsonify({'message': 'Eliminado'})
    except NotFoundError as exc:
        return jsonify({'message': str(exc)}), 404


@productos_bp.get('/categorias')
def listar_categorias():
    from funcionalidades.categorias.infrastructure.categoria_model import CategoriaModel
    categorias = CategoriaModel.query.filter_by(activa=True).all()
    return jsonify([{
        'id': c.id,
        'nombre': c.nombre,
        'descripcion': c.descripcion
    } for c in categorias])


