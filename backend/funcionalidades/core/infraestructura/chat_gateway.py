from funcionalidades.core.infraestructura.openai_service import OpenAIService
from funcionalidades.rag.application.use_cases.recuperar_contexto_use_case import RecuperarContextoUseCase
from funcionalidades.rag.infrastructure.documento_repository_impl import DocumentoRepositoryImpl
from funcionalidades.rag.infrastructure.embedder_openai import OpenAIEmbedder


class ChatGateway:
    def __init__(self):
        self.openai = OpenAIService()
        self.rag_repo = DocumentoRepositoryImpl()
        self.embedder = OpenAIEmbedder()

    def answer(self, user_message: str) -> str:
        context_chunks = RecuperarContextoUseCase(self.rag_repo, self.embedder).ejecutar(user_message, top_k=3)
        context = '\n'.join(context_chunks)
        messages = [
            {"role": "system", "content": "Eres un asistente de soporte de tienda online. Usa el contexto cuando sea útil."},
            {"role": "system", "content": f"Contexto:\n{context}"},
            {"role": "user", "content": user_message}
        ]
        return self.openai.chat(messages)


