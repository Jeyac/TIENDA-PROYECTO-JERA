from flask import Blueprint, jsonify, request

from funcionalidades.core.infraestructura.auth import jwt_required
from funcionalidades.chatlog.infrastructure.chat_message_model import ChatMessageModel


chatlog_bp = Blueprint('chatlog', __name__)


@chatlog_bp.get('/')
@jwt_required(roles={'administrador'})
def listar_chats():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    q = ChatMessageModel.query.order_by(ChatMessageModel.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        'items': [
            {
                'id': m.id,
                'user_id': m.user_id,
                'role': m.role,
                'content': m.content[:200],
                'created_at': m.created_at.isoformat()
            } for m in q.items
        ],
        'page': q.page,
        'pages': q.pages,
        'total': q.total
    })



