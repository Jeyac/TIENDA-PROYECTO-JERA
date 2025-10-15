export default defineNuxtRouteMiddleware((to, from) => {
  const auth = useAuthStore()
  
  // Solo inicializar autenticación básica si no está inicializada
  if (typeof window !== 'undefined' && !auth.hasTokens) {
    const token = localStorage.getItem('access_token')
    const refreshToken = localStorage.getItem('refresh_token')
    const userStr = localStorage.getItem('user')
    
    if (token && refreshToken && userStr) {
      try {
        // Solo restaurar tokens básicamente, sin verificar expiración
        // La verificación de expiración se hará en los middlewares específicos
        auth.token = token
        auth.refreshToken = refreshToken
        auth.user = JSON.parse(userStr)
      } catch (error) {
        // Limpiar datos corruptos silenciosamente
        auth.token = null
        auth.refreshToken = null
        auth.user = null
        if (typeof window !== 'undefined') {
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          localStorage.removeItem('user')
        }
      }
    }
  }
})








