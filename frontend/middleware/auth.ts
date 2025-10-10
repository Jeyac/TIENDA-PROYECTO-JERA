export default defineNuxtRouteMiddleware((to) => {
  const auth = useAuthStore()
  
  // Inicializar autenticación si no está inicializada
  if (typeof window !== 'undefined' && !auth.token) {
    const token = localStorage.getItem('access_token')
    const refreshToken = localStorage.getItem('refresh_token')
    const userStr = localStorage.getItem('user')

    if (token && refreshToken && userStr) {
      try {
        auth.token = token
        auth.refreshToken = refreshToken
        auth.user = JSON.parse(userStr)
        
        // Iniciar refresh automático si no está ya iniciado
        if (!auth.refreshInterval) {
          auth.startTokenRefresh()
        }
      } catch (error) {
        console.error('Error al parsear datos de usuario:', error)
        // Limpiar datos corruptos
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('user')
        return navigateTo(`/login?next=${to.fullPath}`)
      }
    }
  }
  
  // Solo redirigir al login si realmente no hay sesión válida
  if (!auth.isAuthenticated) {
    return navigateTo(`/login?next=${to.fullPath}`)
  }
})

