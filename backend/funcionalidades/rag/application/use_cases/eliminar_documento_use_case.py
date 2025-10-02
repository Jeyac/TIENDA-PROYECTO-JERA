from funcionalidades.rag.domain.repositories.documento_repository import DocumentoRepository


class EliminarDocumentoUseCase:
    def __init__(self, repo: DocumentoRepository):
        self.repo = repo

    def ejecutar(self, documento_id: int) -> None:
        self.repo.eliminar(documento_id)


