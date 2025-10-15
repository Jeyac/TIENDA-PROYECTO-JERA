export default defineNuxtRouteMiddleware(async (to, from) => {
  const auth = useAuthStore()
  
  // Solo ejecutar en el cliente (no en el servidor)
  if (typeof window === 'undefined') {
    return
  }
  
  if (!auth.hasTokens) {
    const token = localStorage.getItem('access_token')
    const refreshToken = localStorage.getItem('refresh_token')
    const userStr = localStorage.getItem('user')

    if (token && refreshToken && userStr) {
      try {
        // Verificar si el token está expirado
        const tokenParts = token.split('.')
        if (tokenParts.length === 3 && tokenParts[1]) {
          const payload = JSON.parse(atob(tokenParts[1]))
          const currentTime = Math.floor(Date.now() / 1000)
          
          if (payload.exp && payload.exp > currentTime) {
            // Token válido, restaurar sesión
            auth.token = token
            auth.refreshToken = refreshToken
            auth.user = JSON.parse(userStr)
            
            // Iniciar refresh automático si no está ya iniciado
            if (!auth.refreshInterval) {
              auth.startTokenRefresh()
            }
          } else {
            // Token expirado, intentar renovar
            auth.token = token
            auth.refreshToken = refreshToken
            auth.user = JSON.parse(userStr)
            
            // Intentar renovar el token
            try {
              await auth.refreshAccessToken()
            } catch (error) {
              // Si no se puede renovar, limpiar sesión
              auth.handleSessionExpired()
            }
          }
        } else {
          // Token malformado, limpiar
          auth.handleSessionExpired()
        }
      } catch (error) {
        // Limpiar datos corruptos
        auth.handleSessionExpired()
      }
    }
  }
  
  // Verificar que esté autenticado
  if (!auth.isAuthenticated) {
    return navigateTo('/login')
  }
  
  // Si estamos autenticados pero el token podría estar expirado, intentar renovar
  if (auth.hasTokens) {
    try {
      const tokenParts = auth.token?.split('.')
      if (tokenParts && tokenParts.length === 3 && tokenParts[1]) {
        const payload = JSON.parse(atob(tokenParts[1]))
        const currentTime = Math.floor(Date.now() / 1000)
        const timeUntilExpiry = payload.exp - currentTime
        
        // Si el token expira en menos de 5 minutos, renovarlo
        if (timeUntilExpiry < 300) {
          await auth.refreshAccessToken()
        }
      }
    } catch (error) {
      // No redirigir aquí, solo loggear el error
    }
  }
  
  // Verificar que NO sea administrador ni atención al cliente
  const rol = auth.user?.rol
  if (rol === 'administrador') {
    return navigateTo('/admin/analytics')
  }
  
  if (rol === 'atencion_cliente') {
    return navigateTo('/atencion/tickets')
  }
})
