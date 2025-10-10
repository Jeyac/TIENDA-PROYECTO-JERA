import { defineStore } from 'pinia'

type CarritoItem = {
  producto_id: number
  titulo: string
  precio_unitario: number
  cantidad: number
}

export const useCarritoStore = defineStore('carrito', {
  state: () => ({ 
    items: [] as CarritoItem[] 
  }),
  getters: {
    total(state) {
      return state.items.reduce((acc, it) => acc + it.cantidad * it.precio_unitario, 0)
    },
    count(state) {
      return state.items.reduce((acc, it) => acc + it.cantidad, 0)
    }
  },
  actions: {
    agregarItem(p: any, cantidad: number = 1) {
      const found = this.items.find(i => i.producto_id === p.id)
      if (found) {
        // Si el producto ya existe, establecer la cantidad exacta (no sumar)
        found.cantidad = cantidad
      } else {
        // Si es un producto nuevo, agregarlo con la cantidad especificada
        this.items.push({ producto_id: p.id, titulo: p.titulo, precio_unitario: p.precio, cantidad })
      }
    },
    quitarItem(producto_id: number) {
      this.items = this.items.filter(i => i.producto_id !== producto_id)
    },
    vaciar() { 
      this.items = [] 
    },
    // Inicializar carrito limpio
    inicializar() {
      this.items = []
    }
  }
})


