from typing import List, Dict
from funcionalidades.core.infraestructura.database import db
from funcionalidades.productos.infrastructure.producto_model import ProductoModel
from funcionalidades.pedidos.infrastructure.pedido_model import PedidoModel, PedidoItemModel


class StockService:
    """Servicio para manejar el stock de productos"""
    
    @staticmethod
    def verificar_stock_disponible(items: List[Dict]) -> bool:
        """
        Verificar si hay stock suficiente para todos los items del pedido
        
        Args:
            items: Lista de items con producto_id y cantidad
            
        Returns:
            bool: True si hay stock suficiente, False en caso contrario
        """
        for item in items:
            producto_id = item['producto_id']
            cantidad_solicitada = item['cantidad']
            
            producto = ProductoModel.query.get(producto_id)
            if not producto:
                return False
                
            if producto.stock < cantidad_solicitada:
                return False
                
        return True
    
    @staticmethod
    def reducir_stock(items: List[Dict]) -> None:
        """
        Reducir el stock de productos cuando se crea un pedido
        
        Args:
            items: Lista de items con producto_id y cantidad
        """
        for item in items:
            producto_id = item['producto_id']
            cantidad = item['cantidad']
            
            producto = ProductoModel.query.get(producto_id)
            if producto:
                producto.stock -= cantidad
                if producto.stock < 0:
                    producto.stock = 0
        
        db.session.commit()
    
    @staticmethod
    def restaurar_stock(pedido_id: int) -> None:
        """
        Restaurar el stock de productos cuando se cancela un pedido
        
        Args:
            pedido_id: ID del pedido a cancelar
        """
        pedido = PedidoModel.query.get(pedido_id)
        if not pedido:
            print(f"Warning: Pedido {pedido_id} no encontrado para restaurar stock")
            return
        
        print(f"Restaurando stock para pedido {pedido_id} con {len(pedido.items)} items")
        
        for item in pedido.items:
            producto = ProductoModel.query.get(item.producto_id)
            if producto:
                stock_anterior = producto.stock
                producto.stock += item.cantidad
                print(f"Producto {producto.id} ({producto.titulo}): {stock_anterior} + {item.cantidad} = {producto.stock}")
            else:
                print(f"Warning: Producto {item.producto_id} no encontrado")
        
        db.session.commit()
        print(f"Stock restaurado exitosamente para pedido {pedido_id}")
    
    @staticmethod
    def restaurar_stock_por_items(items: List[Dict]) -> None:
        """
        Restaurar stock específico por items (para casos donde no se tiene el pedido completo)
        
        Args:
            items: Lista de items con producto_id y cantidad
        """
        for item in items:
            producto_id = item['producto_id']
            cantidad = item['cantidad']
            
            producto = ProductoModel.query.get(producto_id)
            if producto:
                producto.stock += cantidad
        
        db.session.commit()
