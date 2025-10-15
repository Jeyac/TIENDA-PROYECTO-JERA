from flask import Blueprint, jsonify, request, make_response, current_app
from funcionalidades.core.infraestructura.auth import jwt_required
from funcionalidades.tickets.application.use_cases.crear_ticket_use_case import CrearTicketUseCase
from funcionalidades.tickets.application.use_cases.crear_ticket_desde_conversacion_use_case import CrearTicketDesdeConversacionUseCase
from funcionalidades.tickets.application.use_cases.actualizar_estado_ticket_use_case import ActualizarEstadoTicketUseCase
from funcionalidades.tickets.application.use_cases.asignar_ticket_use_case import AsignarTicketUseCase
from funcionalidades.tickets.application.use_cases.obtener_ticket_use_case import ObtenerTicketUseCase
from funcionalidades.tickets.application.use_cases.listar_tickets_use_case import ListarTicketsUseCase
from funcionalidades.tickets.application.use_cases.agregar_actividad_ticket_use_case import AgregarActividadTicketUseCase
from funcionalidades.tickets.infrastructure.ticket_repository_impl import TicketRepositoryImpl
from funcionalidades.tickets.infrastructure.ticket_model import TicketModel

ticket_bp = Blueprint('tickets', __name__)

# Inicializar casos de uso
ticket_repository = TicketRepositoryImpl()
crear_ticket_use_case = CrearTicketUseCase(ticket_repository)
crear_ticket_desde_conversacion_use_case = CrearTicketDesdeConversacionUseCase(ticket_repository)
actualizar_estado_ticket_use_case = ActualizarEstadoTicketUseCase(ticket_repository)
asignar_ticket_use_case = AsignarTicketUseCase(ticket_repository)
obtener_ticket_use_case = ObtenerTicketUseCase(ticket_repository)
listar_tickets_use_case = ListarTicketsUseCase(ticket_repository)
agregar_actividad_ticket_use_case = AgregarActividadTicketUseCase(ticket_repository)

@ticket_bp.before_request
def tickets_preflight_handler():
    # Permitir preflight CORS sin exigir autenticación
    if request.method == 'OPTIONS':
        try:
            current_app.logger.info(
                f"[TICKETS] CORS preflight OPTIONS {request.path} | Origin={request.headers.get('Origin')} | "
                f"AC-Req-Method={request.headers.get('Access-Control-Request-Method')} | "
                f"AC-Req-Headers={request.headers.get('Access-Control-Request-Headers')}"
            )
        except Exception:
            pass
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
        try:
            current_app.logger.info(
                f"[TICKETS] CORS preflight RESP 200 | ACO={resp.headers.get('Access-Control-Allow-Origin')} | "
                f"ACH={resp.headers.get('Access-Control-Allow-Headers')} | ACM={resp.headers.get('Access-Control-Allow-Methods')}"
            )
        except Exception:
            pass
        return resp


@ticket_bp.route('/', methods=['GET', 'OPTIONS'])
@ticket_bp.route('', methods=['GET', 'OPTIONS'])
@jwt_required(roles={'administrador'})
def get_all_tickets():
    """Obtener todos los tickets (admin)"""
    try:
        status_filter = request.args.get('status')
        with current_app.app_context():
            tickets = listar_tickets_use_case.ejecutar(status=status_filter)
        
        # Convertir entidades a diccionarios para JSON
        tickets_data = []
        for ticket in tickets:
            tickets_data.append({
                'id': ticket.id,
                'user_id': ticket.user_id,
                'conversation_id': ticket.conversation_id,
                'title': ticket.title,
                'description': ticket.description,
                'status': ticket.status,
                'priority': ticket.priority,
                'category': ticket.category,
                'assigned_to': ticket.assigned_to,
                'resolution': ticket.resolution,
                'created_at': ticket.created_at.isoformat() if ticket.created_at else None,
                'updated_at': ticket.updated_at.isoformat() if ticket.updated_at else None,
                'closed_at': ticket.closed_at.isoformat() if ticket.closed_at else None
            })
        
        return jsonify(tickets_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@ticket_bp.route('/my', methods=['GET', 'OPTIONS'])
@jwt_required(roles={'cliente', 'administrador', 'atencion_cliente'})
def get_my_tickets():
    """Obtener tickets del usuario actual"""
    try:
        from funcionalidades.core.infraestructura.auth import get_current_user_id
        user_id = get_current_user_id()
        
        # Ejecutar dentro del contexto de la aplicación
        with current_app.app_context():
            tickets = listar_tickets_use_case.ejecutar(user_id=user_id)
            
            # Convertir entidades a diccionarios para JSON
            tickets_data = []
            for ticket in tickets:
                # Obtener información adicional del modelo para nombres de usuario
                ticket_model = TicketModel.query.get(ticket.id)
                
                tickets_data.append({
                    'id': ticket.id,
                    'user_id': ticket.user_id,
                    'conversation_id': ticket.conversation_id,
                    'title': ticket.title,
                    'description': ticket.description,
                    'status': ticket.status,
                    'priority': ticket.priority,
                    'category': ticket.category,
                    'assigned_to': ticket.assigned_to,
                    'resolution': ticket.resolution,
                    'created_at': ticket.created_at.isoformat() if ticket.created_at else None,
                    'updated_at': ticket.updated_at.isoformat() if ticket.updated_at else None,
                    'closed_at': ticket.closed_at.isoformat() if ticket.closed_at else None,
                    'assignee_name': ticket_model.assignee.username if ticket_model and ticket_model.assignee else None
                })
        
        return jsonify(tickets_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@ticket_bp.route('/assigned', methods=['GET', 'OPTIONS'])
@jwt_required(roles={'atencion_cliente', 'administrador'})
def get_assigned_tickets():
    """Obtener tickets asignados al usuario actual (para atención al cliente)"""
    try:
        from funcionalidades.core.infraestructura.auth import get_current_user_id
        user_id = get_current_user_id()
        
        status_filter = request.args.get('status')
        with current_app.app_context():
            if status_filter:
                # Filtrar por estado y asignado
                all_tickets = listar_tickets_use_case.ejecutar(status=status_filter)
                tickets = [t for t in all_tickets if t.assigned_to == user_id]
            else:
                tickets = listar_tickets_use_case.ejecutar(assigned_to=user_id)
            
            # Convertir entidades a diccionarios para JSON
            tickets_data = []
            for ticket in tickets:
                # Obtener información adicional del modelo para nombres de usuario
                ticket_model = TicketModel.query.get(ticket.id)
                
                tickets_data.append({
                    'id': ticket.id,
                    'user_id': ticket.user_id,
                    'conversation_id': ticket.conversation_id,
                    'title': ticket.title,
                    'description': ticket.description,
                    'status': ticket.status,
                    'priority': ticket.priority,
                    'category': ticket.category,
                    'assigned_to': ticket.assigned_to,
                    'resolution': ticket.resolution,
                    'created_at': ticket.created_at.isoformat() if ticket.created_at else None,
                    'updated_at': ticket.updated_at.isoformat() if ticket.updated_at else None,
                    'closed_at': ticket.closed_at.isoformat() if ticket.closed_at else None,
                    'assignee_name': ticket_model.assignee.username if ticket_model and ticket_model.assignee else None,
                    'user_name': ticket_model.user.username if ticket_model and ticket_model.user else 'Usuario anónimo'
                })
        
        return jsonify(tickets_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@ticket_bp.route('/', methods=['POST', 'OPTIONS'])
@jwt_required(roles={'cliente', 'administrador'})
def create_ticket():
    """Crear nuevo ticket"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        required_fields = ['title']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo requerido: {field}'}), 400
        
        from funcionalidades.core.infraestructura.auth import get_current_user_id
        user_id = get_current_user_id()
        
        with current_app.app_context():
            ticket = crear_ticket_use_case.ejecutar(
                user_id=user_id,
                title=data['title'],
                description=data.get('description', ''),
                priority=data.get('priority', 'media'),
                category=data.get('category', 'soporte')
            )
        
        return jsonify({
            'id': ticket.id,
            'title': ticket.title,
            'status': ticket.status,
            'message': 'Ticket creado exitosamente'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@ticket_bp.route('/<int:ticket_id>', methods=['GET', 'OPTIONS'])
@jwt_required(roles={'cliente', 'administrador', 'atencion_cliente'})
def get_ticket(ticket_id):
    """Obtener ticket específico"""
    try:
        from funcionalidades.core.infraestructura.auth import get_current_user_id
        
        with current_app.app_context():
            ticket = obtener_ticket_use_case.ejecutar(ticket_id)
        
        # Verificar permisos
        current_user_id = get_current_user_id()
        from funcionalidades.usuarios.infrastructure.usuario_model import UsuarioModel
        current_user = UsuarioModel.query.get(current_user_id)
        
        # Permitir acceso si:
        # 1. Es el creador del ticket
        # 2. Es administrador (con header X-Admin-Request)
        # 3. Es atención al cliente y el ticket está asignado a él
        can_access = (
            ticket.user_id == current_user_id or 
            request.headers.get('X-Admin-Request') or
            (current_user.rol == 'atencion_cliente' and ticket.assigned_to == current_user_id)
        )
        
        if not can_access:
            return jsonify({'error': 'No tienes permisos para ver este ticket'}), 403
        
        # Obtener información adicional del modelo para nombres de usuario
        from funcionalidades.tickets.infrastructure.ticket_model import TicketModel
        ticket_model = TicketModel.query.get(ticket_id)
        
        ticket_data = {
            'id': ticket.id,
            'title': ticket.title,
            'description': ticket.description,
            'status': ticket.status,
            'priority': ticket.priority,
            'category': ticket.category,
            'assigned_to': ticket.assigned_to,
            'created_at': ticket.created_at.isoformat() if ticket.created_at else None,
            'updated_at': ticket.updated_at.isoformat() if ticket.updated_at else None,
            'closed_at': ticket.closed_at.isoformat() if ticket.closed_at else None,
            'resolution': ticket.resolution,
            'user_name': ticket_model.user.username if ticket_model.user else 'Usuario anónimo',
            'assignee_name': ticket_model.assignee.username if ticket_model.assignee else None
        }
        
        return jsonify(ticket_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@ticket_bp.route('/<int:ticket_id>/status', methods=['PUT', 'OPTIONS'])
@jwt_required(roles={'atencion_cliente'})
def update_ticket_status(ticket_id):
    """Actualizar estado de ticket (solo atención al cliente)"""
    try:
        data = request.get_json()
        
        if not data or 'status' not in data:
            return jsonify({'error': 'Estado requerido'}), 400
        
        from funcionalidades.core.infraestructura.auth import get_current_user_id
        user_id = get_current_user_id()
        
        with current_app.app_context():
            ticket = actualizar_estado_ticket_use_case.ejecutar(
                ticket_id=ticket_id,
                new_status=data['status'],
                user_id=user_id,
                resolution=data.get('resolution')
            )
        
        return jsonify({
            'id': ticket.id,
            'status': ticket.status,
            'message': 'Estado actualizado exitosamente'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@ticket_bp.route('/<int:ticket_id>/assign', methods=['PUT', 'OPTIONS'])
@jwt_required(roles={'administrador'})
def assign_ticket(ticket_id):
    """Asignar ticket (solo admin)"""
    try:
        data = request.get_json()
        
        if not data or 'assignee_id' not in data:
            return jsonify({'error': 'ID de asignado requerido'}), 400
        
        from funcionalidades.core.infraestructura.auth import get_current_user_id
        user_id = get_current_user_id()
        
        with current_app.app_context():
            ticket = asignar_ticket_use_case.ejecutar(
                ticket_id=ticket_id,
                assigned_to=data['assignee_id'],
                user_id=user_id
            )
        
        return jsonify({
            'id': ticket.id,
            'assigned_to': ticket.assigned_to,
            'message': 'Ticket asignado exitosamente'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@ticket_bp.route('/<int:ticket_id>/activities', methods=['GET', 'OPTIONS'])
@jwt_required(roles={'cliente', 'administrador', 'atencion_cliente'})
def get_ticket_activities(ticket_id):
    """Obtener actividades de un ticket"""
    try:
        from funcionalidades.core.infraestructura.auth import get_current_user_id
        
        ticket = obtener_ticket_use_case.ejecutar(ticket_id)
        
        # Verificar permisos
        current_user_id = get_current_user_id()
        if ticket.user_id != current_user_id and ticket.assigned_to != current_user_id and not request.headers.get('X-Admin-Request'):
            return jsonify({'error': 'No tienes permisos para ver este ticket'}), 403
        
        activities = ticket_repository.get_actividades_by_ticket_id(ticket_id)
        
        # Convertir entidades a diccionarios para JSON
        activities_data = []
        for activity in activities:
            activities_data.append({
                'id': activity.id,
                'ticket_id': activity.ticket_id,
                'user_id': activity.user_id,
                'activity_type': activity.activity_type,
                'description': activity.description,
                'old_value': activity.old_value,
                'new_value': activity.new_value,
                'created_at': activity.created_at.isoformat() if activity.created_at else None
            })
        
        return jsonify(activities_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@ticket_bp.route('/<int:ticket_id>/message', methods=['POST', 'OPTIONS'])
@jwt_required(roles={'cliente', 'atencion_cliente'})
def add_ticket_message(ticket_id):
    """Agregar mensaje al chat del ticket (cliente y atención al cliente)"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'error': 'Mensaje requerido'}), 400
        
        from funcionalidades.core.infraestructura.auth import get_current_user_id
        from funcionalidades.usuarios.infrastructure.usuario_model import UsuarioModel
        
        user_id = get_current_user_id()
        user = UsuarioModel.query.get(user_id)
        
        # Verificar que el ticket existe
        with current_app.app_context():
            ticket = obtener_ticket_use_case.ejecutar(ticket_id)
        
        # Verificar permisos: debe ser el creador del ticket o el asignado
        if user.rol == 'cliente' and ticket.user_id != user_id:
            return jsonify({'error': 'No tienes permisos para enviar mensajes en este ticket'}), 403
        
        if user.rol == 'atencion_cliente' and ticket.assigned_to != user_id:
            return jsonify({'error': 'Este ticket no está asignado a ti'}), 403
        
        # Crear actividad de mensaje usando el caso de uso
        with current_app.app_context():
            activity = agregar_actividad_ticket_use_case.ejecutar(
                ticket_id=ticket_id,
                user_id=user_id,
                activity_type='commented',
                description=data['message']
            )
        
        return jsonify({
            'id': activity.id,
            'message': 'Mensaje enviado exitosamente',
            'activity': {
                'id': activity.id,
                'ticket_id': activity.ticket_id,
                'user_id': activity.user_id,
                'user_name': user.username,
                'user_rol': user.rol,
                'activity_type': activity.activity_type,
                'description': activity.description,
                'created_at': activity.created_at.isoformat() if activity.created_at else None
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@ticket_bp.route('/from-conversation/<int:conversation_id>', methods=['POST', 'OPTIONS'])
@jwt_required(roles={'cliente', 'administrador'})
def create_ticket_from_conversation(conversation_id):
    """Crear ticket desde una conversación"""
    try:
        data = request.get_json() or {}
        
        from funcionalidades.core.infraestructura.auth import get_current_user_id
        user_id = get_current_user_id()
        
        with current_app.app_context():
            ticket = crear_ticket_desde_conversacion_use_case.ejecutar(
                conversation_id=conversation_id,
                user_id=user_id,
                title=data.get('title'),
                description=data.get('description'),
                priority=data.get('priority', 'media'),
                category=data.get('category', 'soporte')
            )
        
        return jsonify({
            'id': ticket.id,
            'title': ticket.title,
            'status': ticket.status,
            'message': 'Ticket creado desde conversación exitosamente'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
