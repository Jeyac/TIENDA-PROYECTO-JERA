from funcionalidades.core.infraestructura.database import db


class DocumentoModel(db.Model):
    __tablename__ = 'documentos'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    chunks = db.relationship('DocumentoChunkModel', backref='documento', cascade='all, delete-orphan', lazy=True)


class DocumentoChunkModel(db.Model):
    __tablename__ = 'documento_chunks'

    id = db.Column(db.Integer, primary_key=True)
    documento_id = db.Column(db.Integer, db.ForeignKey('documentos.id'), nullable=False)
    texto = db.Column(db.Text, nullable=False)
    # Guardamos embedding como JSON (lista de floats)
    embedding = db.Column(db.JSON, nullable=False)


