from flask import Blueprint, jsonify, request

from funcionalidades.core.infraestructura.auth import jwt_required
from funcionalidades.rag.application.use_cases.ingestar_documento_use_case import IngestarDocumentoUseCase
from funcionalidades.rag.application.use_cases.recuperar_contexto_use_case import RecuperarContextoUseCase
from funcionalidades.rag.application.use_cases.eliminar_documento_use_case import EliminarDocumentoUseCase
from funcionalidades.rag.infrastructure.documento_repository_impl import DocumentoRepositoryImpl
from funcionalidades.rag.infrastructure.documento_model import DocumentoModel, DocumentoChunkModel
from funcionalidades.rag.infrastructure.embedder_openai import OpenAIEmbedder
from funcionalidades.rag.infrastructure.text_extractor import TextExtractor


rag_bp = Blueprint('rag', __name__)
repo = DocumentoRepositoryImpl()
embedder = OpenAIEmbedder()


@rag_bp.post('/documentos')
@jwt_required(roles={'administrador'})
def ingestar_documento():
    data = request.get_json(silent=True) or {}
    titulo = data.get('titulo')
    contenido = data.get('contenido')
    if not titulo or not contenido:
        return jsonify({'message': 'Datos incompletos'}), 400
    doc = IngestarDocumentoUseCase(repo, embedder).ejecutar(titulo, contenido)
    return jsonify({'id': doc.id, 'titulo': doc.titulo}), 201


@rag_bp.delete('/documentos/<int:documento_id>')
@jwt_required(roles={'administrador'})
def eliminar_documento(documento_id: int):
    EliminarDocumentoUseCase(repo).ejecutar(documento_id)
    return jsonify({'message': 'Eliminado'})


@rag_bp.post('/retrieve')
@jwt_required
def retrieve():
    data = request.get_json(silent=True) or {}
    query = data.get('query')
    if not query:
        return jsonify({'message': 'query requerido'}), 400
    chunks = RecuperarContextoUseCase(repo, embedder).ejecutar(query, top_k=3)
    return jsonify({'chunks': chunks})


@rag_bp.post('/upload')
@jwt_required(roles={'administrador'})
def upload():
    if 'file' not in request.files:
        return jsonify({'message': 'file requerido'}), 400
    storage = request.files['file']
    titulo, contenido = TextExtractor.from_file(storage)
    if not contenido.strip():
        return jsonify({'message': 'No se pudo extraer texto'}), 400
    doc = IngestarDocumentoUseCase(repo, embedder).ejecutar(titulo, contenido)
    return jsonify({'id': doc.id, 'titulo': doc.titulo}), 201


@rag_bp.get('/documentos')
@jwt_required(roles={'administrador'})
def listar_documentos():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    q = DocumentoModel.query.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        'items': [{'id': d.id, 'titulo': d.titulo} for d in q.items],
        'page': q.page,
        'pages': q.pages,
        'total': q.total
    })


@rag_bp.get('/documentos/<int:documento_id>/chunks')
@jwt_required(roles={'administrador'})
def listar_chunks(documento_id: int):
    chunks = DocumentoChunkModel.query.filter_by(documento_id=documento_id).all()
    return jsonify([
        {'id': c.id, 'texto': c.texto[:200], 'len': len(c.texto)} for c in chunks
    ])


