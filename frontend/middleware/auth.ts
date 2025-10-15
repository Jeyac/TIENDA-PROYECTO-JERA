export default defineNuxtRouteMiddleware(async (to) => {
  const auth = useAuthStore()
  
  // Solo ejecutar en el cliente (no en el servidor)
  if (typeof window === 'undefined') {
    return
  }
  
  // Inicializar autenticación si no está inicializada
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
              // Si no se puede renovar, limpiar sesión pero no redirigir aquí
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
  
  // Solo redirigir al login si realmente no hay sesión válida
  if (!auth.isAuthenticated) {
    // Si tenemos tokens pero no estamos autenticados, el token podría estar expirado
    if (auth.hasTokens) {
      try {
        // Intentar renovar el token
        await auth.refreshAccessToken()
        // Si la renovación fue exitosa, continuar
        if (auth.isAuthenticated) {
          // Continuar normalmente
        } else {
          return navigateTo(`/login?next=${to.fullPath}`)
        }
      } catch (error) {
        return navigateTo(`/login?next=${to.fullPath}`)
      }
    } else {
      // No hay tokens, redirigir al login
      return navigateTo(`/login?next=${to.fullPath}`)
    }
  }
})

