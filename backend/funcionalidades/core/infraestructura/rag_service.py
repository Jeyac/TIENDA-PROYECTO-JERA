from typing import List
from openai import OpenAI
import numpy as np
import faiss


class RAGService:
    def __init__(self):
        # Inicializar cliente OpenAI
        self.client = OpenAI()

        # Documentos base del sistema (pueden venir de archivos o BD)
        self.docs = [
            'Políticas de envío: los pedidos se entregan en 24-48 horas hábiles.',
            'Devoluciones: puedes devolver un producto dentro de 30 días presentando el ticket.',
            'Soporte técnico: disponible de lunes a viernes de 9:00 a 18:00 horas.',
        ]

        # Generar embeddings de los documentos
        print("Generando embeddings...")
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=self.docs
        )
        self.embeddings = np.array([item.embedding for item in response.data], dtype="float32")

        # Crear índice FAISS para búsqueda por similitud
        dim = len(self.embeddings[0])
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(self.embeddings)
        print(f"Índice FAISS creado con {len(self.docs)} documentos.")

    def retrieve(self, query: str, k: int = 3) -> List[str]:
        """Devuelve los k documentos más relevantes según la consulta"""
        # Generar embedding de la consulta
        query_emb = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=query
        ).data[0].embedding

        query_emb = np.array([query_emb], dtype="float32")

        # Buscar los k más cercanos
        distances, indices = self.index.search(query_emb, k)
        results = [self.docs[i] for i in indices[0]]

        return results

