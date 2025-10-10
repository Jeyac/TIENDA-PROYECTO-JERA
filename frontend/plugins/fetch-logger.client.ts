export default defineNuxtPlugin(() => {
  const auth = useAuthStore()
  
  // Verificar si ya se ejecutó este plugin
  if ((window as any).__fetchLoggerInstalled) {
    console.log('⚠️ fetch-logger plugin ya está instalado, ignorando...')
    return
  }
  (window as any).__fetchLoggerInstalled = true
  console.log('🔧 Instalando fetch-logger plugin...')
  
  // Interceptor para fetch
  const originalFetch = window.fetch
  let requestCounter = 0
  
  window.fetch = async (input: RequestInfo | URL, init?: RequestInit) => {
    const url = typeof input === 'string' ? input : input instanceof URL ? input.toString() : input.url
    const config = useRuntimeConfig()
    const requestId = ++requestCounter
    
    // Log de petición (solo para debugging si es necesario)
    // if (url.startsWith(config.public.apiBase)) {
    //   console.log(`[fetch][start][${requestId}] ${init?.method || 'GET'} ${url}`)
    // }
    
    // Agregar token si es una petición a nuestra API
    if (url.startsWith(config.public.apiBase) && auth.token) {
      if (init) {
        init.headers = {
          ...init.headers,
          'Authorization': `Bearer ${auth.token}`
        }
      } else {
        init = {
          headers: {
            'Authorization': `Bearer ${auth.token}`
          }
        }
      }
    }
    
    try {
      const response = await originalFetch(input, init)
      
      // Log de respuesta (solo para debugging si es necesario)
      // if (url.startsWith(config.public.apiBase)) {
      //   console.log(`[fetch][end][${requestId}] ${init?.method || 'GET'} ${url} ${response.status} ${response.statusText}`)
      //   
      //   if (!response.ok) {
      //     console.log(`[fetch][error-status][${requestId}] ${init?.method || 'GET'} ${url} ${response.status} ${response.statusText}`)
      //   }
      // }
      
      // Manejar token expirado
      if (response.status === 401 && auth.refreshToken && url.startsWith(config.public.apiBase)) {
        console.log(`[fetch][401][${requestId}] Token expirado, intentando renovar...`)
        
        try {
          await auth.refreshAccessToken()
          console.log(`[fetch][retry][${requestId}] Token renovado, reintentando petición...`)
          
          // Reintentar con nuevo token
          if (init) {
            init.headers = {
              ...init.headers,
              'Authorization': `Bearer ${auth.token}`
            }
          } else {
            init = {
              headers: {
                'Authorization': `Bearer ${auth.token}`
              }
            }
          }
          
          const retryResponse = await originalFetch(input, init)
          console.log(`[fetch][retry-end][${requestId}] Respuesta del reintento: ${retryResponse.status}`)
          return retryResponse
        } catch (error) {
          console.log(`[fetch][retry-error][${requestId}] No se pudo renovar token, redirigiendo...`)
          await auth.logout()
        }
      }
      
      return response
    } catch (error) {
      if (url.startsWith(config.public.apiBase)) {
        console.error(`[fetch][error][${requestId}] ${init?.method || 'GET'} ${url}`, error)
      }
      throw error
    }
  }
})

