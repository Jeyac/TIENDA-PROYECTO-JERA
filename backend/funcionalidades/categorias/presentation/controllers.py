from flask import Blueprint, jsonify, request

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


@categorias_bp.route('/', methods=['POST', 'OPTIONS'])
@jwt_required(roles={'administrador'})
def crear_categoria():
    data = request.get_json(silent=True) or {}
    try:
        use_case = CrearCategoriaUseCase(repo)
        categoria = use_case.ejecutar(
            nombre=data.get('nombre'),
            descripcion=data.get('descripcion'),
            activa=data.get('activa', True)
        )
        return jsonify(categoria.__dict__), 201
    except BadRequestError as exc:
        return jsonify({'message': str(exc)}), 400


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



