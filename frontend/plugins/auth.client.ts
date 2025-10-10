import { defineNuxtPlugin } from '#app'
import { useAuthStore } from '~/stores/auth'

export default defineNuxtPlugin(() => {
  // Inicializar autenticación al cargar la aplicación
  const auth = useAuthStore()
  auth.initializeAuth()
})


