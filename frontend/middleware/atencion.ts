export default defineNuxtRouteMiddleware((to, from) => {
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
      } catch (error) {
        console.error('Error al parsear datos de usuario:', error)
        // Limpiar datos corruptos
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('user')
        return navigateTo('/login')
      }
    }
  }
  
  // Verificar que esté autenticado
  if (!auth.isAuthenticated) {
    return navigateTo('/login')
  }
  
  // Verificar que sea atención al cliente
  const rol = auth.user?.rol
  if (rol !== 'atencion_cliente') {
    // Si es administrador, redirigir a admin
    if (rol === 'administrador') {
      return navigateTo('/admin/analytics')
    }
    
    throw createError({
      statusCode: 403,
      statusMessage: 'Acceso denegado. Solo personal de atención al cliente puede acceder a esta página.'
    })
  }
})