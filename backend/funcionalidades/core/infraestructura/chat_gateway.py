import re
import numpy as np
from typing import List, Tuple, Optional

from funcionalidades.core.infraestructura.openai_service import OpenAIService
"""
ChatGateway híbrido:
- Productos/categorías: exclusivamente BD (no LLM)
- Soporte general: RAG + OpenAI (con instrucciones estrictas de no inventar datos de catálogo)
"""
from funcionalidades.rag.application.use_cases.recuperar_contexto_use_case import RecuperarContextoUseCase
from funcionalidades.rag.infrastructure.documento_repository_impl import DocumentoRepositoryImpl
from funcionalidades.rag.infrastructure.embedder_openai import OpenAIEmbedder
from funcionalidades.productos.infrastructure.producto_model import ProductoModel
from funcionalidades.core.infraestructura.database import db
from funcionalidades.categorias.infrastructure.categoria_model import CategoriaModel

# Configuración de soporte
SUPPORT_EMAIL = "rox17jacome@gmail.com"


class ChatGateway:
    def __init__(self, similarity_threshold: float = 0.65):
        self.openai = OpenAIService()
        self.rag_repo = DocumentoRepositoryImpl()
        self.embedder = OpenAIEmbedder()

        self.similarity_threshold = similarity_threshold
        self.products: List[ProductoModel] = []
        self.product_embeddings: Optional[np.ndarray] = None
        self.product_norms: Optional[np.ndarray] = None

        self._load_products_embeddings()

    def _load_products_embeddings(self):
        try:
            productos = (
                db.session.query(ProductoModel)
                .filter(ProductoModel.activo.is_(True))
                .all()
            ) or []
            self.products = productos

            texts = [f"{p.titulo}. {p.descripcion or ''}" for p in self.products]
            embeddings = (
                self.embedder.embed_many(texts)
                if hasattr(self.embedder, "embed_many")
                else [self.embedder.embed(t) for t in texts]
            )

            if embeddings and len(embeddings) == len(self.products):
                self.product_embeddings = np.array(embeddings, dtype="float32")
                self.product_norms = np.linalg.norm(self.product_embeddings, axis=1)
            else:
                self.product_embeddings = None
                self.product_norms = None

        except Exception as e:
            print("warning: no se pudieron cargar embeddings de productos:", str(e))
            self.products = []
            self.product_embeddings = None
            self.product_norms = None

    def _semantic_search_products(self, query: str, top_k: int = 5) -> List[Tuple[ProductoModel, float]]:
        if self.product_embeddings is not None and len(self.products) > 0:
            try:
                q_emb = (
                    np.array(self.embedder.embed(query), dtype="float32")
                    if hasattr(self.embedder, "embed")
                    else np.array(self.embedder.embed_text(query), dtype="float32")
                )
                q_norm = np.linalg.norm(q_emb)
                if q_norm == 0:
                    return []
                sims = (self.product_embeddings @ q_emb) / (self.product_norms * q_norm + 1e-10)
                idx = np.argsort(-sims)[:top_k]
                return [(self.products[i], float(sims[i])) for i in idx]
            except Exception as e:
                print("warning: error en búsqueda semántica:", str(e))
                return []
        return []

    def _format_product_short(self, p: ProductoModel) -> str:
        precio = f"Q{(getattr(p, 'precio', 0) or 0):.2f}"
        return f"- {p.titulo} — {precio}"

    def _format_product_detail(self, p: ProductoModel) -> str:
        precio = f"Q{(getattr(p, 'precio', 0) or 0):.2f}"
        stock = getattr(p, "stock", None)
        estado = f"Disponible ({stock} unidades)" if stock else ("Disponible" if getattr(p, 'activo', True) else "No disponible")
        descripcion = getattr(p, "descripcion", "") or "No disponible"
        imagen = getattr(p, "imagen_url", None) or getattr(p, "imagen", None)
        categoria_nombre = getattr(p, 'categoria_nombre', '')
        if not categoria_nombre:
            try:
                if getattr(p, 'categoria_id', None) is not None:
                    cat = db.session.query(CategoriaModel).get(getattr(p, 'categoria_id'))
                    if cat:
                        categoria_nombre = getattr(cat, 'nombre', '') or ''
            except Exception:
                categoria_nombre = ''
        lines = [
            f"Producto: {p.titulo}",
            f"Precio: {precio}",
            f"Estado: {estado}",
            f"Categoría: {categoria_nombre}",
            "",
            f"Descripción: {descripcion}"
        ]
        if imagen:
            lines.append(f"Imagen: {imagen}")
        return "\n".join(lines)

    def _db_text_search(self, user_message: str, limit: int = 5) -> List[ProductoModel]:
        try:
            like = f"%{user_message}%"
            query = (
                db.session.query(ProductoModel)
                .filter(ProductoModel.activo.is_(True))
                .filter((ProductoModel.titulo.ilike(like)) | (ProductoModel.descripcion.ilike(like)))
                .limit(limit)
            )
            return list(query)
        except Exception as e:
            print("warning: error en búsqueda por texto:", str(e))
            return []

    def _extract_product_by_name(self, text: str) -> Optional[ProductoModel]:
        """Busca un producto por nombre aproximado en BD (ilike)."""
        if not text:
            return None
        try:
            like = f"%{text}%"
            return (
                db.session.query(ProductoModel)
                .filter(ProductoModel.activo.is_(True))
                .filter(ProductoModel.titulo.ilike(like))
                .order_by(ProductoModel.id.desc())
                .first()
            )
        except Exception:
            return None

    def _resolve_product_from_history(self, history: Optional[List[dict]], fallback_first: bool = True) -> Optional[ProductoModel]:
        """Intenta deducir el último producto mencionado/listado en la conversación."""
        if not history:
            return None
        # buscar en los últimos mensajes del asistente líneas tipo "- Nombre — Q..."
        for msg in reversed(history[-8:]):
            if msg.get('role') != 'assistant':
                continue
            content = msg.get('content') or ''
            for line in content.splitlines():
                line = line.strip()
                if not line.startswith('- '):
                    continue
                # extraer nombre entre el "- " y el separador " — " si existe
                name = line[2:]
                if ' — ' in name:
                    name = name.split(' — ', 1)[0].strip()
                if name:
                    p = self._extract_product_by_name(name)
                    if p:
                        return p
        if fallback_first and self.products:
            return self.products[-1]
        return None

    def answer(self, user_message: str, history: Optional[List[dict]] = None) -> str:
        context_chunks = RecuperarContextoUseCase(self.rag_repo, self.embedder).ejecutar(user_message, top_k=3)
        context = '\n'.join(context_chunks or [])

        # 🔍 categorías: detección simple y listados
        lower = (user_message or '').lower()
        is_catalog_intent = False

        # 🛒 intención de compra (mensaje guiado, sin tocar carrito/pedidos)
        buy_keywords = (
            'comprar', 'adquirir', 'quiero comprar', 'añadir al carrito', 'agregar al carrito',
            'lo quiero', 'me lo llevo', 'quiero ese', 'comprarlo', 'comprarla'
        )
        if any(k in lower for k in buy_keywords):
            # si podemos resolver un producto del historial, guiar con ese nombre
            prod_for_buy = self._resolve_product_from_history(history) if history else None
            if prod_for_buy:
                return (
                    f"Para comprar {prod_for_buy.titulo}:\n"
                    "1) Ve al catálogo y abre el producto.\n"
                    "2) Inicia sesión o regístrate si aún no lo has hecho.\n"
                    "3) Añade el producto al carrito y procede al pago.\n"
                    "Si necesitas, puedo darte más detalles del producto antes de continuar."
                )
            return (
                "Para comprar:\n"
                "1) Ve al catálogo y elige el producto.\n"
                "2) Inicia sesión o regístrate si aún no lo has hecho.\n"
                "3) Añade el producto al carrito y procede al pago.\n"
                "Si me dices el nombre del producto, te doy sus detalles."
            )
        if any(k in lower for k in ["categoría", "categoria", "categorías", "categorias"]):
            # Buscar primero si preguntan por productos de una categoría específica
            # heurística: tomar última palabra o frase entre comillas después de 'categor'
            cat_name = None
            m = re.search(r"categor[ií]a[s]?\s*(?:de|:)?\s*['\"]?([\w\sáéíóúñ]+)['\"]?", lower)
            if m:
                cat_name = m.group(1).strip()
            if cat_name:
                try:
                    cat = db.session.query(CategoriaModel).filter(CategoriaModel.nombre.ilike(f"%{cat_name}%"), CategoriaModel.activa.is_(True)).first()
                    if cat:
                        prods = (
                            db.session.query(ProductoModel)
                            .filter(ProductoModel.activo.is_(True), ProductoModel.categoria_id == cat.id)
                            .order_by(ProductoModel.id.desc())
                            .limit(10)
                            .all()
                        )
                        if prods:
                            lines = [f"Productos en la categoría '{cat.nombre}':"]
                            for p in prods:
                                lines.append(self._format_product_short(p))
                            lines.append("¿Quieres detalles de alguno? dime el nombre.")
                            return "\n".join(lines)
                        else:
                            return f"No encontré productos activos en la categoría '{cat.nombre}'."
                except Exception:
                    pass
            # Si no mencionan específica, devolver listado general
            try:
                cats = (
                    db.session.query(CategoriaModel)
                    .filter(CategoriaModel.activa.is_(True))
                    .order_by(CategoriaModel.nombre.asc())
                    .all()
                )
                if cats:
                    names = [f"- {c.nombre}" for c in cats]
                    return "Estas son nuestras categorías disponibles:\n" + "\n".join(names)
            except Exception:
                pass
            # marcar que es intención de catálogo/categorías, para no recurrir a RAG
            is_catalog_intent = True

        # 📌 referencias anafóricas simples ("la laptop", "esa", "sí") usando historial
        if history:
            # si el usuario dice solo "sí" o confirma, ofrecer detalle del último producto mencionado
            if lower.strip() in ("si", "sí", "dale", "ok", "esta bien", "está bien"):
                p_hist = self._resolve_product_from_history(history)
                if p_hist:
                    return self._format_product_detail(p_hist)
            # si dice "la X" / "el X" / "sobre X"
            m_ref = re.search(r"\b(?:la|el|sobre|de)\s+([\w\sáéíóúñ\-]+)$", lower)
            if m_ref:
                name_ref = m_ref.group(1).strip()
                p_name = self._extract_product_by_name(name_ref)
                if p_name:
                    return self._format_product_detail(p_name)

        # 🧩 consultas de información/especificaciones de un producto
        info_keywords = ("información", "informacion", "detalles", "especificaciones", "caracteristicas", "características", "procesador", "ram", "memoria", "almacenamiento")
        if any(k in lower for k in info_keywords):
            # intentar resolver producto por historial o por nombre dentro del mensaje
            p_target = self._resolve_product_from_history(history)
            if not p_target:
                # buscar por nombre aproximado a partir del mensaje completo
                # tomar la última palabra relevante si existe
                tokens = [t for t in re.split(r"[^\wáéíóúñ]+", lower) if t]
                if tokens:
                    p_target = self._extract_product_by_name(tokens[-1])
            if p_target:
                # si no hay descripción, decirlo explícitamente
                desc = getattr(p_target, 'descripcion', None)
                if not desc:
                    return f"Descripción: No disponible"
                return self._format_product_detail(p_target)
            # si no resolvemos producto, guiar al usuario
            return "Dime el nombre del producto para darte su información desde nuestra base de datos."

        # 🔍 buscar productos similares
        semantic_matches = self._semantic_search_products(user_message, top_k=5)
        semantic_matches_filtered = [(p, s) for p, s in semantic_matches if s >= self.similarity_threshold]

        if len(semantic_matches_filtered) > 0:
            top_product, top_score = semantic_matches_filtered[0]
            if top_score >= 0.85:
                return self._format_product_detail(top_product)
            else:
                lines = ["Encontré algunos productos que podrían interesarte:"]
                for p, s in semantic_matches_filtered[:5]:
                    lines.append(self._format_product_short(p))
                lines.append("¿Quieres que te muestre más detalles de alguno? solo dime su nombre.")
                return "\n".join(lines)

        # 🔎 fallback por texto (sin embeddings)
        db_matches = self._db_text_search(user_message, limit=5)
        if len(db_matches) > 0:
            lines = ["Estos son algunos productos relacionados con tu búsqueda:"]
            for p in db_matches:
                lines.append(self._format_product_short(p))
            lines.append("¿Quieres saber más sobre alguno? solo dime el nombre del producto.")
            return "\n".join(lines)

        # 🛒 intención genérica sobre productos: devolver catálogo breve desde BD
        product_intent_keywords = [
            "productos", "producto", "catalogo", "catálogo", "ver productos", "qué tienen", "que tienen",
            "mostrar productos", "lista de productos", "ofrecen", "disponibles"
        ]
        lower_intent = lower
        if any(k in lower_intent for k in product_intent_keywords):
            try:
                fallback = (
                    db.session.query(ProductoModel)
                    .filter(ProductoModel.activo.is_(True))
                    .order_by(ProductoModel.id.desc())
                    .limit(5)
                    .all()
                )
                if fallback:
                    lines = ["Estos son algunos de nuestros productos disponibles:"]
                    for p in fallback:
                        lines.append(self._format_product_short(p))
                    lines.append("¿Quieres más detalles de alguno? dime el nombre.")
                    return "\n".join(lines)
            except Exception:
                pass
            # marcar intención de catálogo para no caer a RAG
            is_catalog_intent = True

        # 🧠 si no hay productos pero hay contexto RAG (información general de tienda)
        # Evitar RAG si la intención es de productos/categorías: en esos casos solo BD
        if context.strip() and not is_catalog_intent:
            # Usar LLM, con prompt que prohíbe inventar datos de catálogo
            messages = [
                {
                    "role": "system",
                    "content": (
                        "Eres un asistente de soporte de una tienda online. Responde de forma breve, amable y precisa. "
                        "Cuando el usuario pregunte por productos o categorías, NO inventes: di que solo puedes usar la base de datos. "
                        f"Para contacto de soporte usa exclusivamente el correo {SUPPORT_EMAIL}."
                    ),
                },
                {"role": "system", "content": f"Contexto RAG (solo referencia, no inventes):\n{context}"},
            ]
            # incluir breve historial reciente si se proporciona
            if history:
                for h in history[-6:]:
                    role = h.get("role")
                    content = h.get("content", "")
                    if role in ("user", "assistant") and content:
                        messages.append({"role": role, "content": content})
            messages.append({"role": "user", "content": user_message})
            return self.openai.chat(messages)

        # ⚠️ fuera de dominio
        return (
            "Lo siento, no encontré información sobre eso. Puedo ayudarte con productos, precios o categorías de la tienda. "
            "¿Qué te gustaría ver?"
        )

    def refresh_products_embeddings(self):
        self._load_products_embeddings()

    def summarize(self, history: List[dict]) -> str:
        """Resumen breve con LLM, limitado y seguro."""
        last_msgs = [m for m in history[-12:] if m.get("role") in ("user", "assistant")]
        messages = [
            {
                "role": "system",
                "content": (
                    "Eres un asistente que resume conversaciones de soporte. Devuelve un resumen breve (máx 4 oraciones) "
                    "con puntos clave, productos mencionados y próximas acciones. No inventes datos de catálogo."
                ),
            }
        ]
        for m in last_msgs:
            messages.append({"role": m.get("role"), "content": m.get("content", "")})
        try:
            return self.openai.chat(messages)
        except Exception:
            return "Resumen no disponible."
