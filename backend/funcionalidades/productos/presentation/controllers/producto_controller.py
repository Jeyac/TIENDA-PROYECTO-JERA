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


@productos_bp.route('/', methods=['POST', 'OPTIONS'])
@jwt_required(roles={'administrador'})
def crear_producto():
    data = request.get_json(silent=True) or {}
    try:
        # Crear producto directamente en la base de datos para manejar campos adicionales
        from funcionalidades.productos.infrastructure.producto_model import ProductoModel
        from funcionalidades.core.infraestructura.database import db
        
        producto = ProductoModel(
            titulo=data.get('titulo'),
            precio=data.get('precio'),
            descripcion=data.get('descripcion', ''),
            imagenes=data.get('imagenes', []),
            imagen_url=data.get('imagen_url', ''),
            stock=data.get('stock', 0),
            categoria_id=data.get('categoria_id'),
            activo=data.get('activo', True)
        )
        
        db.session.add(producto)
        db.session.commit()
        
        return jsonify({
            'id': producto.id,
            'titulo': producto.titulo,
            'descripcion': producto.descripcion,
            'precio': float(producto.precio),
            'stock': producto.stock,
            'categoria_id': producto.categoria_id,
            'activo': producto.activo,
            'imagen_url': producto.imagen_url
        }), 201
    except Exception as exc:
        db.session.rollback()
        return jsonify({'message': str(exc)}), 400


@productos_bp.route('/', methods=['GET', 'OPTIONS'])
def listar_productos():
    from funcionalidades.productos.infrastructure.producto_model import ProductoModel
    from funcionalidades.categorias.infrastructure.categoria_model import CategoriaModel
    
    try:
        categoria_id = request.args.get('categoria_id')
        busqueda = request.args.get('q')
        all_products = request.args.get('all') == '1'  # Para admin ver todos los productos
        
        # Si es admin y pide todos los productos, no filtrar por activo
        if all_products:
            query = ProductoModel.query
        else:
            # Público: solo productos activos
            query = ProductoModel.query.filter_by(activo=True)
        
        # Validar categoría si se proporciona
        if categoria_id:
            try:
                categoria_id = int(categoria_id)
                # Verificar que la categoría existe y está activa
                categoria = CategoriaModel.query.filter_by(id=categoria_id, activa=True).first()
                if not categoria:
                    return jsonify({'error': f'Categoría con ID {categoria_id} no encontrada o inactiva'}), 404
                query = query.filter_by(categoria_id=categoria_id)
            except ValueError:
                return jsonify({'error': 'categoria_id debe ser un número válido'}), 400
        
        if busqueda:
            query = query.filter(ProductoModel.titulo.ilike(f'%{busqueda}%'))
        
        items = []
        for p in query.all():
            categoria = CategoriaModel.query.get(p.categoria_id)
            
            # Calcular cantidad total pedida de este producto
            from funcionalidades.pedidos.infrastructure.pedido_model import PedidoItemModel
            from sqlalchemy import func
            cantidad_pedida = db.session.query(func.coalesce(func.sum(PedidoItemModel.cantidad), 0)).filter(
                PedidoItemModel.producto_id == p.id
            ).scalar() or 0
            
            # Construir URLs completas para las imágenes
            imagenes_urls = []
            if p.imagenes:
                for img in p.imagenes:
                    if img:  # Verificar que no esté vacío
                        # Si ya es una URL completa, usarla tal como está
                        if img.startswith('http://') or img.startswith('https://'):
                            imagenes_urls.append(img)
                        else:
                            # Si es solo un nombre de archivo, construir la URL completa
                            imagenes_urls.append(f"/uploads/{img}")
            
            items.append({
                'id': p.id,
                'titulo': p.titulo,
                'precio': p.precio,
                'descripcion': p.descripcion,
                'imagenes': imagenes_urls,
                'imagen_url': p.imagen_url,
                'stock': p.stock or 0,
                'categoria_id': p.categoria_id,
                'categoria_nombre': categoria.nombre if categoria else 'Sin categoría',
                'activo': p.activo,
                'cantidad_pedida': int(cantidad_pedida)
            })
        return jsonify(items)
    
    except Exception as e:
        print(f"Error en listar_productos: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Error interno del servidor'}), 500


@productos_bp.route('/<int:producto_id>', methods=['GET', 'OPTIONS'])
def obtener_producto(producto_id: int):
    # Público: solo productos activos
    from funcionalidades.productos.infrastructure.producto_model import ProductoModel
    p = ProductoModel.query.filter_by(id=producto_id, activo=True).first()
    if not p:
        return jsonify({'message': 'Producto no encontrado'}), 404
    from funcionalidades.categorias.infrastructure.categoria_model import CategoriaModel
    categoria = CategoriaModel.query.get(p.categoria_id)
    
    # Construir URLs completas para las imágenes
    imagenes_urls = []
    if p.imagenes:
        for img in p.imagenes:
            if img:  # Verificar que no esté vacío
                # Si ya es una URL completa, usarla tal como está
                if img.startswith('http://') or img.startswith('https://'):
                    imagenes_urls.append(img)
                else:
                    # Si es solo un nombre de archivo, construir la URL completa
                    imagenes_urls.append(f"/uploads/{img}")
    
    return jsonify({
        'id': p.id,
        'titulo': p.titulo,
        'precio': p.precio,
        'descripcion': p.descripcion,
        'imagenes': imagenes_urls,
        'categoria_id': p.categoria_id,
        'categoria_nombre': categoria.nombre if categoria else 'Sin categoría',
        'activo': p.activo
    })


@productos_bp.route('/<int:producto_id>', methods=['PUT', 'OPTIONS'])
@jwt_required(roles={'administrador'})
def actualizar_producto(producto_id: int):
    data = request.get_json(silent=True) or {}
    try:
        # Actualizar producto directamente en la base de datos
        from funcionalidades.productos.infrastructure.producto_model import ProductoModel
        from funcionalidades.core.infraestructura.database import db
        
        producto = ProductoModel.query.get(producto_id)
        if not producto:
            return jsonify({'message': 'Producto no encontrado'}), 404
        
        # Actualizar campos
        if 'titulo' in data:
            producto.titulo = data['titulo']
        if 'precio' in data:
            producto.precio = data['precio']
        if 'descripcion' in data:
            producto.descripcion = data['descripcion']
        if 'imagenes' in data:
            producto.imagenes = data['imagenes']
        if 'imagen_url' in data:
            producto.imagen_url = data['imagen_url']
        if 'stock' in data:
            producto.stock = data['stock']
        if 'categoria_id' in data:
            producto.categoria_id = data['categoria_id']
        if 'activo' in data:
            producto.activo = data['activo']
        
        db.session.commit()
        
        return jsonify({
            'id': producto.id,
            'titulo': producto.titulo,
            'descripcion': producto.descripcion,
            'precio': float(producto.precio),
            'stock': producto.stock,
            'categoria_id': producto.categoria_id,
            'activo': producto.activo,
            'imagen_url': producto.imagen_url
        })
    except Exception as exc:
        db.session.rollback()
        return jsonify({'message': str(exc)}), 400


@productos_bp.route('/<int:producto_id>', methods=['DELETE', 'OPTIONS'])
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




