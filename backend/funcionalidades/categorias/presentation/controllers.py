from flask import Blueprint, jsonify, request, make_response

from funcionalidades.core.infraestructura.auth import jwt_required
from funcionalidades.core.exceptions import BadRequestError, NotFoundError
from funcionalidades.categorias.application.use_cases.crear_categoria_use_case import CrearCategoriaUseCase
from funcionalidades.categorias.application.use_cases.listar_categorias_use_case import ListarCategoriasUseCase
from funcionalidades.categorias.application.use_cases.obtener_categoria_use_case import ObtenerCategoriaUseCase
from funcionalidades.categorias.application.use_cases.actualizar_categoria_use_case import ActualizarCategoriaUseCase
from funcionalidades.categorias.application.use_cases.eliminar_categoria_use_case import EliminarCategoriaUseCase
from funcionalidades.categorias.infrastructure.categoria_repository_impl import CategoriaRepositoryImpl


categorias_bp = Blueprint('categorias', __name__)
repo = CategoriaRepositoryImpl()

@categorias_bp.before_request
def categorias_preflight_handler():
    """Manejador de preflight CORS para categorías"""
    if request.method == 'OPTIONS':
        resp = make_response('', 200)
        origin = request.headers.get('Origin')
        if origin:
            resp.headers['Access-Control-Allow-Origin'] = origin
            resp.headers['Vary'] = 'Origin'
        req_headers = request.headers.get('Access-Control-Request-Headers') or 'Content-Type, Authorization'
        resp.headers['Access-Control-Allow-Headers'] = req_headers
        resp.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
        resp.headers['Access-Control-Allow-Credentials'] = 'true'
        resp.headers['Access-Control-Max-Age'] = '600'
        return resp


@categorias_bp.route('/', methods=['POST', 'OPTIONS'])
@jwt_required(roles={'administrador'})
def crear_categoria():
    print("=== Creando nueva categoría ===")
    data = request.get_json(silent=True) or {}
    print(f"Datos recibidos: {data}")
    
    try:
        # Validar datos requeridos
        if not data.get('nombre') or not data.get('nombre').strip():
            return jsonify({'message': 'El nombre es obligatorio'}), 400
        
        if not data.get('descripcion') or not data.get('descripcion').strip():
            return jsonify({'message': 'La descripción es obligatoria'}), 400
        
        # Verificar si ya existe una categoría con ese nombre
        from funcionalidades.categorias.infrastructure.categoria_model import CategoriaModel
        existing = CategoriaModel.query.filter_by(nombre=data['nombre'].strip()).first()
        if existing:
            return jsonify({'message': 'Ya existe una categoría con ese nombre'}), 400
        
        use_case = CrearCategoriaUseCase(repo)
        categoria = use_case.ejecutar(
            nombre=data.get('nombre').strip(),
            descripcion=data.get('descripcion').strip(),
            activa=data.get('activa', True)
        )
        
        print(f"Categoría creada exitosamente: {categoria.nombre}")
        return jsonify({
            'id': categoria.id,
            'nombre': categoria.nombre,
            'descripcion': categoria.descripcion,
            'activa': categoria.activa
        }), 201
        
    except BadRequestError as exc:
        print(f"BadRequestError: {exc}")
        return jsonify({'message': str(exc)}), 400
    except Exception as exc:
        print(f"Error creando categoría: {exc}")
        import traceback
        traceback.print_exc()
        return jsonify({'message': f'Error interno del servidor: {str(exc)}'}), 500


@categorias_bp.route('/', methods=['GET', 'OPTIONS'])
def listar_categorias():
    # Público: solo categorías activas
    from funcionalidades.categorias.infrastructure.categoria_model import CategoriaModel
    categorias = CategoriaModel.query.filter_by(activa=True).all()
    return jsonify([{
        'id': c.id,
        'nombre': c.nombre,
        'descripcion': c.descripcion,
        'activa': c.activa
    } for c in categorias])


@categorias_bp.route('/<int:categoria_id>', methods=['GET', 'OPTIONS'])
def obtener_categoria(categoria_id: int):
    try:
        use_case = ObtenerCategoriaUseCase(repo)
        c = use_case.ejecutar(categoria_id)
        return jsonify(c.__dict__)
    except NotFoundError as exc:
        return jsonify({'message': str(exc)}), 404


@categorias_bp.put('/<int:categoria_id>')
@jwt_required(roles={'administrador'})
def actualizar_categoria(categoria_id: int):
    data = request.get_json(silent=True) or {}
    try:
        use_case = ActualizarCategoriaUseCase(repo)
        c = use_case.ejecutar(
            categoria_id,
            data.get('nombre'),
            data.get('descripcion'),
            data.get('activa', True)
        )
        return jsonify(c.__dict__)
    except NotFoundError as exc:
        return jsonify({'message': str(exc)}), 404
    except BadRequestError as exc:
        return jsonify({'message': str(exc)}), 400


@categorias_bp.delete('/<int:categoria_id>')
@jwt_required(roles={'administrador'})
def eliminar_categoria(categoria_id: int):
    try:
        use_case = EliminarCategoriaUseCase(repo)
        use_case.ejecutar(categoria_id)
        return jsonify({'message': 'Eliminado'})
    except NotFoundError as exc:
        return jsonify({'message': str(exc)}), 404



