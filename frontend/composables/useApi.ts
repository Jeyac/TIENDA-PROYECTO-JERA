export const useApi = () => {
  const auth = useAuthStore()
  const config = useRuntimeConfig()

  const apiRequest = async (url: string, options: RequestInit = {}) => {
    // Agregar token si está disponible
    if (auth.token) {
      options.headers = {
        ...options.headers,
        'Authorization': `Bearer ${auth.token}`
      }
    }

    try {
      const response = await fetch(`${config.public.apiBase}${url}`, options)
      
      // Si es 401, intentar renovar token
      if (response.status === 401 && auth.refreshToken) {
        console.log('Token expirado, renovando...')
        try {
          await auth.refreshAccessToken()
          console.log('Token renovado, reintentando petición...')
          // Reintentar con nuevo token
          options.headers = {
            ...options.headers,
            'Authorization': `Bearer ${auth.token}`
          }
          return await fetch(`${config.public.apiBase}${url}`, options)
        } catch (error) {
          console.log('No se pudo renovar token, redirigiendo...')
          await auth.logout()
          throw new Error('Sesión expirada')
        }
      }
      
      return response
    } catch (error) {
      console.error('Error en petición API:', error)
      throw error
    }
  }

  return {
    apiRequest
  }
}

