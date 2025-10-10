import { defineNuxtPlugin } from '#app'
import { useCarritoStore } from '~/stores/carrito'

export default defineNuxtPlugin(() => {
  // Inicializar carrito limpio al cargar la aplicación
  const carrito = useCarritoStore()
  carrito.inicializar()
})


