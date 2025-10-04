import { defineStore } from 'pinia'

type CarritoItem = {
  producto_id: number
  titulo: string
  precio_unitario: number
  cantidad: number
}

export const useCarritoStore = defineStore('carrito', {
  state: () => ({ items: [] as CarritoItem[] }),
  getters: {
    total(state) {
      return state.items.reduce((acc, it) => acc + it.cantidad * it.precio_unitario, 0)
    },
    count(state) {
      return state.items.reduce((acc, it) => acc + it.cantidad, 0)
    }
  },
  actions: {
    agregarItem(p: any) {
      const found = this.items.find(i => i.producto_id === p.id)
      if (found) found.cantidad += 1
      else this.items.push({ producto_id: p.id, titulo: p.titulo, precio_unitario: p.precio, cantidad: 1 })
    },
    quitarItem(producto_id: number) {
      this.items = this.items.filter(i => i.producto_id !== producto_id)
    },
    vaciar() { this.items = [] }
  }
})


