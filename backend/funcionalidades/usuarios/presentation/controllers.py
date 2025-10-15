from flask import Blueprint, jsonify, request, make_response
from werkzeug.security import generate_password_hash

from funcionalidades.core.infraestructura.auth import jwt_required
from funcionalidades.core.infraestructura.security import hash_password
from funcionalidades.core.infraestructura.database import db
from funcionalidades.usuarios.infrastructure.usuario_model import UsuarioModel


usuarios_admin_bp = Blueprint('usuarios_admin', __name__)

@usuarios_admin_bp.before_request
def usuarios_preflight_handler():
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


@usuarios_admin_bp.route('/', methods=['GET', 'OPTIONS'])
@jwt_required(roles={'administrador'})
def listar_usuarios():
    items = UsuarioModel.query.all()
    return jsonify([
        {'id': u.id, 'username': u.username, 'email': u.email, 'rol': u.rol, 'activo': u.activo}
        for u in items
    ])


@usuarios_admin_bp.route('/atencion', methods=['GET', 'OPTIONS'])
@jwt_required(roles={'administrador'})
def listar_atencion_cliente():
    """Listar usuarios con rol de atención al cliente"""
    print("=== DEBUG: Listando usuarios de atención al cliente ===")
    items = UsuarioModel.query.filter_by(rol='atencion_cliente', activo=True).all()
    print(f"Usuarios encontrados: {len(items)}")
    for u in items:
        print(f"  - ID: {u.id}, Username: {u.username}, Email: {u.email}")
    
    result = [
        {'id': u.id, 'username': u.username, 'email': u.email}
        for u in items
    ]
    print(f"Resultado a enviar: {result}")
    return jsonify(result)


@usuarios_admin_bp.route('/', methods=['POST', 'OPTIONS'])
@jwt_required(roles={'administrador'})
def crear_usuario():
    data = request.get_json()
    
    # Validar datos requeridos
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Username, email y password son requeridos'}), 400
    
    # Verificar si el usuario ya existe
    if UsuarioModel.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'El username ya existe'}), 400
    
    if UsuarioModel.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'El email ya existe'}), 400
    
    try:
        # Crear nuevo usuario
        usuario = UsuarioModel(
            username=data['username'],
            email=data['email'],
            password_hash=hash_password(data['password']),
            rol=data.get('rol', 'usuario')
        )
        
        db.session.add(usuario)
        db.session.commit()
        
        return jsonify({
            'id': usuario.id,
            'username': usuario.username,
            'email': usuario.email,
            'rol': usuario.rol
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@usuarios_admin_bp.route('/<int:user_id>', methods=['PUT', 'OPTIONS'])
@jwt_required(roles={'administrador'})
def actualizar_usuario(user_id):
    print(f"=== Actualizando usuario {user_id} ===")
    try:
        usuario = UsuarioModel.query.get_or_404(user_id)
        data = request.get_json()
        print(f"Datos recibidos: {data}")
        
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        # Actualizar campos si se proporcionan
        if 'username' in data:
            # Verificar que el username no esté en uso por otro usuario
            existing = UsuarioModel.query.filter_by(username=data['username']).first()
            if existing and existing.id != user_id:
                return jsonify({'error': 'El username ya está en uso'}), 400
            usuario.username = data['username']
        
        if 'email' in data:
            # Verificar que el email no esté en uso por otro usuario
            existing = UsuarioModel.query.filter_by(email=data['email']).first()
            if existing and existing.id != user_id:
                return jsonify({'error': 'El email ya está en uso'}), 400
            usuario.email = data['email']
        
        if 'rol' in data:
            usuario.rol = data['rol']
        
        if 'activo' in data:
            print(f"Actualizando campo activo: {data['activo']} -> {bool(data['activo'])}")
            # Verificar que no se pueda desactivar un administrador
            if usuario.rol == 'administrador' and not bool(data['activo']):
                return jsonify({'error': 'No se puede desactivar un usuario administrador'}), 400
            usuario.activo = bool(data['activo'])
        
        if 'password' in data and data['password']:
            usuario.password_hash = hash_password(data['password'])
        
        print(f"Guardando cambios para usuario {user_id}...")
        db.session.commit()
        print(f"Cambios guardados exitosamente")
        
        return jsonify({
            'id': usuario.id,
            'username': usuario.username,
            'email': usuario.email,
            'rol': usuario.rol,
            'activo': usuario.activo
        })
        
    except Exception as e:
        print(f"Error actualizando usuario {user_id}: {e}")
        import traceback
        traceback.print_exc()
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@usuarios_admin_bp.route('/<int:user_id>', methods=['DELETE', 'OPTIONS'])
@jwt_required(roles={'administrador'})
def eliminar_usuario(user_id):
    print(f"=== Eliminando usuario {user_id} ===")
    usuario = UsuarioModel.query.get_or_404(user_id)
    
    try:
        db.session.delete(usuario)
        db.session.commit()
        
        return jsonify({'message': 'Usuario eliminado correctamente'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@usuarios_admin_bp.route('/<int:user_id>/toggle-status', methods=['PUT', 'OPTIONS'])
@jwt_required(roles={'administrador'})
def toggle_user_status(user_id: int):
    """Activar/desactivar usuario."""
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200
    
    try:
        user = UsuarioModel.query.get(user_id)
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        data = request.get_json()
        if not data or 'activo' not in data:
            return jsonify({'error': 'Campo activo requerido'}), 400
        
        # Verificar que no se pueda desactivar un administrador
        if user.rol == 'administrador' and not bool(data['activo']):
            return jsonify({'error': 'No se puede desactivar un usuario administrador'}), 400
        
        user.activo = bool(data['activo'])
        db.session.commit()
        
        return jsonify({
            'message': 'Estado del usuario actualizado correctamente',
            'usuario': {
                'id': user.id,
                'username': user.username,
                'activo': user.activo
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500


