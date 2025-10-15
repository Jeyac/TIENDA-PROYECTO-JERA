"""
ChatGateway híbrido:
- Productos/categorías: exclusivamente BD (no LLM)
- Soporte general: RAG + OpenAI (con instrucciones estrictas de no inventar datos de catálogo)
"""
from funcionalidades.rag.application.use_cases.recuperar_contexto_use_case import RecuperarContextoUseCase
from funcionalidades.rag.infrastructure.documento_repository_impl import DocumentoRepositoryImpl
from funcionalidades.rag.infrastructure.embedder_openai import OpenAIEmbedder
from funcionalidades.productos.infrastructure.producto_model import ProductoModel
from funcionalidades.categorias.infrastructure.categoria_model import CategoriaModel
from funcionalidades.core.infraestructura.database import db

# Configuración de soporte
SUPPORT_EMAIL = "rox17jacome@gmail.com"

from typing import List, Optional, Tuple
import numpy as np
import re
from funcionalidades.core.infraestructura.openai_service import OpenAIService


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
            )
            self.products = productos
            if productos:
                # Generar embeddings para búsqueda semántica
                textos = [f"{p.titulo} {p.descripcion}" for p in productos]
                self.product_embeddings = self.embedder.embed_batch(textos)
                self.product_norms = np.linalg.norm(self.product_embeddings, axis=1, keepdims=True)
        except Exception as e:
            print(f"Error cargando embeddings de productos: {e}")
            self.products = []
            self.product_embeddings = None
            self.product_norms = None

    def _semantic_search_products(self, query: str, top_k: int = 5) -> List[Tuple[ProductoModel, float]]:
        if self.product_embeddings is not None and len(self.products) > 0:
            try:
                query_embedding = self.embedder.embed(query)
                query_norm = np.linalg.norm(query_embedding)
                
                if query_norm > 0:
                    # Calcular similitud coseno
                    similarities = np.dot(self.product_embeddings, query_embedding) / (
                        self.product_norms.flatten() * query_norm
                    )
                    
                    # Obtener top_k productos más similares
                    top_indices = np.argsort(similarities)[::-1][:top_k]
                    results = []
                    for idx in top_indices:
                        if similarities[idx] >= self.similarity_threshold:
                            results.append((self.products[idx], float(similarities[idx])))
                    return results
            except Exception as e:
                print(f"Error en búsqueda semántica: {e}")
        return []

    def _format_product_short(self, p: ProductoModel) -> str:
        precio = f"Q{(getattr(p, 'precio', 0) or 0):.2f}"
        return f"- {p.titulo} — {precio}"

    def _format_product_detail(self, p: ProductoModel) -> str:
        precio = f"Q{(getattr(p, 'precio', 0) or 0):.2f}"
        stock = getattr(p, "stock", None)
        stock_str = f" (Stock: {stock})" if stock is not None else ""
        
        # Obtener categoría
        categoria = None
        if hasattr(p, 'categoria_id'):
            categoria = db.session.query(CategoriaModel).filter(CategoriaModel.id == p.categoria_id).first()
        
        categoria_str = f"\nCategoría: {categoria.nombre}" if categoria else ""
        
        return (
            f"**{p.titulo}**\n"
            f"Precio: {precio}{stock_str}{categoria_str}\n"
            f"Descripción: {p.descripcion}"
        )

    def _db_text_search(self, user_message: str, limit: int = 5) -> List[ProductoModel]:
        try:
            like = f"%{user_message}%"
            return (
                db.session.query(ProductoModel)
                .filter(
                    ProductoModel.activo.is_(True),
                    db.or_(
                        ProductoModel.titulo.ilike(like),
                        ProductoModel.descripcion.ilike(like)
                    )
                )
                .limit(limit)
                .all()
            )
        except Exception:
            return []

    def _extract_product_by_name(self, text: str) -> Optional[ProductoModel]:
        """Busca un producto por nombre aproximado en BD (ilike)."""
        if not text:
            return None
        try:
            return (
                db.session.query(ProductoModel)
                .filter(ProductoModel.activo.is_(True), ProductoModel.titulo.ilike(f"%{text}%"))
                .first()
            )
        except Exception:
            return None

    def _resolve_product_from_history(self, history: Optional[List[dict]], fallback_first: bool = True) -> Optional[ProductoModel]:
        """Intenta deducir el último producto mencionado/listado en la conversación."""
        if not history:
            return None
        # Buscar en los últimos mensajes del asistente por nombres de productos
        for msg in reversed(history[-10:]):
            if msg.get("role") == "assistant":
                content = msg.get("content", "")
                # Buscar líneas que empiecen con "- " (formato de lista)
                lines = content.split("\n")
                for line in lines:
                    if line.strip().startswith("- "):
                        # Extraer nombre del producto (antes de " — ")
                        name = line.strip()[2:]  # quitar "- "
                        if " — " in name:
                            name = name.split(" — ", 1)[0].strip()
                        if name:
                            p = self._extract_product_by_name(name)
                            if p:
                                return p
        if fallback_first and self.products:
            return self.products[-1]
        return None

    def answer(self, user_message: str, history: Optional[List[dict]] = None) -> str:
        # Obtener contexto RAG
        context_chunks = RecuperarContextoUseCase(self.rag_repo, self.embedder).ejecutar(user_message, top_k=3)
        context = '\n'.join(context_chunks or [])

        # Definir las funciones disponibles para function calling
        functions = [
            {
                "name": "buscar_productos_por_nombre",
                "description": "Buscar productos por nombre o descripción",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "nombre": {
                            "type": "string",
                            "description": "Nombre o descripción del producto a buscar"
                        }
                    },
                    "required": ["nombre"]
                }
            },
            {
                "name": "buscar_productos_por_categoria",
                "description": "Buscar productos por categoría",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "categoria_nombre": {
                            "type": "string",
                            "description": "Nombre de la categoría"
                        }
                    },
                    "required": ["categoria_nombre"]
                }
            },
            {
                "name": "listar_categorias",
                "description": "Listar todas las categorías disponibles",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "obtener_detalles_producto",
                "description": "Obtener detalles completos de un producto específico",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "nombre_producto": {
                            "type": "string",
                            "description": "Nombre del producto"
                        }
                    },
                    "required": ["nombre_producto"]
                }
            },
            {
                "name": "buscar_productos_por_precio",
                "description": "Buscar productos por rango de precios",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "precio_min": {
                            "type": "number",
                            "description": "Precio mínimo"
                        },
                        "precio_max": {
                            "type": "number",
                            "description": "Precio máximo"
                        }
                    },
                    "required": []
                }
            }
        ]

        # Mapeo de funciones
        function_map = {
            "buscar_productos_por_nombre": buscar_productos_por_nombre,
            "buscar_productos_por_categoria": buscar_productos_por_categoria,
            "listar_categorias": listar_categorias,
            "obtener_detalles_producto": obtener_detalles_producto,
            "buscar_productos_por_precio": buscar_productos_por_precio
        }

        # Preparar mensajes para OpenAI con function calling
        messages = [
            {
                "role": "system",
                "content": (
                    "Eres un asistente de soporte de una tienda online. "
                    "Puedes buscar productos, categorías y proporcionar información detallada usando las funciones disponibles. "
                    "Responde de forma amable y útil. "
                    f"Para contacto de soporte usa exclusivamente el correo {SUPPORT_EMAIL}."
                )
            }
        ]

        # Agregar contexto RAG si existe
        if context.strip():
            messages.append({
                "role": "system", 
                "content": f"Contexto adicional de la tienda:\n{context}"
            })

        # Agregar historial si existe
        if history:
            for h in history[-6:]:  # Últimos 6 mensajes
                role = h.get("role")
                content = h.get("content", "")
                if role in ("user", "assistant") and content:
                    messages.append({"role": role, "content": content})

        # Agregar mensaje actual del usuario
        messages.append({"role": "user", "content": user_message})

        try:
            # Llamar a OpenAI con function calling
            response = self.openai.chat_with_functions(messages, functions)
            
            # Verificar si hay function calls
            if response.get("function_call"):
                function_name = response["function_call"]["name"]
                function_args = response["function_call"]["arguments"]
                
                # Ejecutar la función
                if function_name in function_map:
                    function_result = function_map[function_name](**function_args)
                    
                    # Agregar resultado de la función al contexto
                    messages.append({
                        "role": "function",
                        "name": function_name,
                        "content": function_result
                    })
                    
                    # Obtener respuesta final
                    final_response = self.openai.chat(messages)
                    return final_response
                else:
                    return "Función no disponible."
            else:
                # Respuesta directa sin function calling
                return response.get("content", "No pude procesar tu consulta.")
                
        except Exception as e:
            print(f"Error en function calling: {e}")
            # Fallback a respuesta simple
            return (
                "Lo siento, tuve un problema procesando tu consulta. "
                "Puedes preguntarme sobre productos, categorías o información general de la tienda. "
                f"Para soporte directo, contacta a {SUPPORT_EMAIL}."
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


# Funciones para function calling
def buscar_productos_por_nombre(nombre: str) -> str:
    """Buscar productos por nombre o descripción"""
    try:
        productos = db.session.query(ProductoModel).filter(
            ProductoModel.activo == True,
            db.or_(
                ProductoModel.titulo.ilike(f'%{nombre}%'),
                ProductoModel.descripcion.ilike(f'%{nombre}%')
            )
        ).limit(10).all()
        
        if not productos:
            return f"No se encontraron productos que coincidan con '{nombre}'"
        
        resultado = f"Productos encontrados para '{nombre}':\n\n"
        for producto in productos:
            categoria = db.session.query(CategoriaModel).filter(CategoriaModel.id == producto.categoria_id).first()
            resultado += f"• {producto.titulo}\n"
            resultado += f"  Precio: Q{producto.precio}\n"
            resultado += f"  Stock: {producto.stock} unidades\n"
            resultado += f"  Categoría: {categoria.nombre if categoria else 'N/A'}\n"
            resultado += f"  Descripción: {producto.descripcion[:100]}...\n\n"
        
        return resultado
    except Exception as e:
        return f"Error buscando productos: {str(e)}"


def buscar_productos_por_categoria(categoria_nombre: str) -> str:
    """Buscar productos por categoría"""
    try:
        categoria = db.session.query(CategoriaModel).filter(
            CategoriaModel.activa == True,
            CategoriaModel.nombre.ilike(f'%{categoria_nombre}%')
        ).first()
        
        if not categoria:
            return f"No se encontró la categoría '{categoria_nombre}'"
        
        productos = db.session.query(ProductoModel).filter(
            ProductoModel.activo == True,
            ProductoModel.categoria_id == categoria.id
        ).limit(20).all()
        
        if not productos:
            return f"No hay productos disponibles en la categoría '{categoria.nombre}'"
        
        resultado = f"Productos en la categoría '{categoria.nombre}':\n\n"
        for producto in productos:
            resultado += f"• {producto.titulo}\n"
            resultado += f"  Precio: Q{producto.precio}\n"
            resultado += f"  Stock: {producto.stock} unidades\n"
            resultado += f"  Descripción: {producto.descripcion[:100]}...\n\n"
        
        return resultado
    except Exception as e:
        return f"Error buscando productos por categoría: {str(e)}"


def listar_categorias() -> str:
    """Listar todas las categorías disponibles"""
    try:
        categorias = db.session.query(CategoriaModel).filter(CategoriaModel.activa == True).all()
        
        if not categorias:
            return "No hay categorías disponibles"
        
        resultado = "Categorías disponibles:\n\n"
        for categoria in categorias:
            # Contar productos en cada categoría
            count = db.session.query(ProductoModel).filter(
                ProductoModel.activo == True,
                ProductoModel.categoria_id == categoria.id
            ).count()
            
            resultado += f"• {categoria.nombre}\n"
            resultado += f"  Descripción: {categoria.descripcion}\n"
            resultado += f"  Productos disponibles: {count}\n\n"
        
        return resultado
    except Exception as e:
        return f"Error listando categorías: {str(e)}"


def obtener_detalles_producto(nombre_producto: str) -> str:
    """Obtener detalles completos de un producto específico"""
    try:
        producto = db.session.query(ProductoModel).filter(
            ProductoModel.activo == True,
            ProductoModel.titulo.ilike(f'%{nombre_producto}%')
        ).first()
        
        if not producto:
            return f"No se encontró el producto '{nombre_producto}'"
        
        categoria = db.session.query(CategoriaModel).filter(CategoriaModel.id == producto.categoria_id).first()
        
        resultado = f"Detalles del producto '{producto.titulo}':\n\n"
        resultado += f"• Precio: Q{producto.precio}\n"
        resultado += f"• Stock disponible: {producto.stock} unidades\n"
        resultado += f"• Categoría: {categoria.nombre if categoria else 'N/A'}\n"
        resultado += f"• Descripción completa: {producto.descripcion}\n"
        
        if producto.imagenes and len(producto.imagenes) > 0:
            resultado += f"• Imágenes disponibles: {len(producto.imagenes)}\n"
        
        return resultado
    except Exception as e:
        return f"Error obteniendo detalles del producto: {str(e)}"


def buscar_productos_por_precio(precio_min: float = None, precio_max: float = None) -> str:
    """Buscar productos por rango de precios"""
    try:
        query = db.session.query(ProductoModel).filter(ProductoModel.activo == True)
        
        if precio_min is not None:
            query = query.filter(ProductoModel.precio >= precio_min)
        if precio_max is not None:
            query = query.filter(ProductoModel.precio <= precio_max)
        
        productos = query.limit(20).all()
        
        if not productos:
            rango = ""
            if precio_min and precio_max:
                rango = f"entre Q{precio_min} y Q{precio_max}"
            elif precio_min:
                rango = f"desde Q{precio_min}"
            elif precio_max:
                rango = f"hasta Q{precio_max}"
            return f"No se encontraron productos {rango}"
        
        resultado = f"Productos encontrados "
        if precio_min and precio_max:
            resultado += f"entre Q{precio_min} y Q{precio_max}"
        elif precio_min:
            resultado += f"desde Q{precio_min}"
        elif precio_max:
            resultado += f"hasta Q{precio_max}"
        resultado += ":\n\n"
        
        for producto in productos:
            categoria = db.session.query(CategoriaModel).filter(CategoriaModel.id == producto.categoria_id).first()
            resultado += f"• {producto.titulo}\n"
            resultado += f"  Precio: Q{producto.precio}\n"
            resultado += f"  Stock: {producto.stock} unidades\n"
            resultado += f"  Categoría: {categoria.nombre if categoria else 'N/A'}\n\n"
        
        return resultado
    except Exception as e:
        return f"Error buscando productos por precio: {str(e)}"
