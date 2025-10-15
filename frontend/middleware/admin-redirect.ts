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
                // Si no se puede renovar, no redirigir aquí, dejar que otros middlewares manejen
                return
              }
            }
          } else {
            // Token malformado, no redirigir aquí
            return
          }
        } catch (error) {
          // No redirigir aquí, dejar que otros middlewares manejen
          return
        }
      }
    }
    
    // Solo redirigir si realmente está autenticado
    if (auth.isAuthenticated && auth.user?.rol) {
      // Si el usuario está autenticado y es administrador
      if (auth.user.rol === 'administrador') {
        // Si no está en una página de admin, redirigir
        if (!to.path.startsWith('/admin')) {
          return navigateTo('/admin/analytics')
        }
      }
      
      // Si el usuario está autenticado y es atención al cliente
      else if (auth.user.rol === 'atencion_cliente') {
        // Si no está en una página de atención, redirigir
        if (!to.path.startsWith('/atencion')) {
          return navigateTo('/atencion/tickets')
        }
      }
      
      // Si el usuario está autenticado y es usuario normal
      else if (auth.user.rol === 'usuario') {
        // Si está en páginas de admin o atención, redirigir
        if (to.path.startsWith('/admin') || to.path.startsWith('/atencion')) {
          return navigateTo('/profile')
        }
      }
    }
})



