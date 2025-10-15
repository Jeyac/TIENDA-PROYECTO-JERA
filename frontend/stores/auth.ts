import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

interface User {
  id: number
  username: string
  email: string
  rol: string
}

interface LoginCredentials {
  username_or_email: string
  password: string
}

interface RegisterData {
  username: string
  email: string
  password: string
  confirm_password: string
}

interface ResetPasswordData {
  email: string
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as User | null,
    token: null as string | null,
    refreshToken: null as string | null,
    isLoading: false,
    error: null as string | null,
    refreshInterval: null as NodeJS.Timeout | null
  }),

  getters: {
    isAuthenticated: (state) => {
      if (!state.token || !state.user) {
        console.log('isAuthenticated: No hay token o usuario')
        return false
      }
      
      try {
        // Verificar si el token está expirado
        const tokenParts = state.token.split('.')
        if (tokenParts.length !== 3 || !tokenParts[1]) {
          console.log('isAuthenticated: Token malformado')
          return false
        }
        
        const payload = JSON.parse(atob(tokenParts[1]))
        const currentTime = Math.floor(Date.now() / 1000)
        const timeUntilExpiry = payload.exp - currentTime
        
        console.log(`isAuthenticated: Token expira en ${timeUntilExpiry} segundos`)
        
        // Considerar autenticado si el token no está expirado O si tenemos refresh token
        // Esto permite que el middleware intente renovar tokens expirados
        const isTokenValid = payload.exp && payload.exp > currentTime
        const hasRefreshToken = !!state.refreshToken
        
        const isValid = isTokenValid || hasRefreshToken
        console.log(`isAuthenticated: Token válido: ${isTokenValid}, tiene refresh: ${hasRefreshToken}, resultado: ${isValid}`)
        return isValid
      } catch (error) {
        console.error('Error verificando token en isAuthenticated:', error)
        return false
      }
    },
    hasTokens: (state) => !!state.token && !!state.refreshToken && !!state.user,
    isAdmin: (state) => state.user?.rol === 'administrador',
    userName: (state) => state.user?.username || '',
    userEmail: (state) => state.user?.email || ''
  },

  actions: {
    async login(credentials: LoginCredentials) {
      this.isLoading = true
      this.error = null

      try {
        const config = useRuntimeConfig()
        const response = await fetch(`${config.public.apiBase}/api/auth/login`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(credentials)
        })

        const data = await response.json()

        if (!response.ok) {
          throw new Error(data.error || data.message || 'Error de autenticación')
        }

        // Guardar tokens y usuario
        this.token = data.access_token
        this.refreshToken = data.refresh_token
        this.user = data.user

        // Persistir en localStorage
        if (typeof window !== 'undefined') {
          localStorage.setItem('access_token', data.access_token)
          localStorage.setItem('refresh_token', data.refresh_token)
          localStorage.setItem('user', JSON.stringify(data.user))
        }

        // Iniciar refresh automático
        this.startTokenRefresh()

        // Redirigir según el rol
        if (typeof window !== 'undefined') {
          if (data.user.rol === 'administrador') {
            await navigateTo('/admin/analytics')
          } else if (data.user.rol === 'atencion_cliente') {
            await navigateTo('/atencion/tickets')
          } else {
            // Usuario normal - redirigir a su dashboard
            await navigateTo('/profile')
          }
        }

        return { success: true, user: data.user }
      } catch (error: any) {
        this.error = error.message
        return { success: false, error: error.message }
      } finally {
        this.isLoading = false
      }
    },

    // Función helper para manejar sesión expirada
    handleSessionExpired(forceRedirect: boolean = false) {
      console.log('Sesión expirada, limpiando datos...')
      
      // Limpiar intervalo de refresh
      if (this.refreshInterval) {
        clearInterval(this.refreshInterval)
        this.refreshInterval = null
      }
      
      // Limpiar estado
      this.user = null
      this.token = null
      this.refreshToken = null
      this.error = null

      // Limpiar localStorage
      if (typeof window !== 'undefined') {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('user')
      }

      // Solo redirigir si se fuerza o si estamos en una página protegida
      if (forceRedirect || process.client) {
        const currentPath = window.location.pathname
        const protectedPaths = ['/admin', '/atencion', '/profile', '/orders', '/tickets']
        const isProtectedPath = protectedPaths.some(path => currentPath.startsWith(path))
        
        if (isProtectedPath) {
          console.log('Redirigiendo al login desde página protegida...')
          window.location.href = '/login'
        } else {
          console.log('Manteniendo usuario en página pública...')
        }
      }
    },

    async refreshAccessToken() {
      if (!this.refreshToken) {
        console.log('No hay refresh token disponible')
        throw new Error('No hay refresh token disponible')
      }

      try {
        console.log('Intentando renovar token...')
        const config = useRuntimeConfig()
        const response = await fetch(`${config.public.apiBase}/api/auth/refresh`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ refresh_token: this.refreshToken })
        })

        console.log('Response status:', response.status)
        const data = await response.json()
        console.log('Response data:', data)

        if (!response.ok) {
          console.log('Error renovando token:', data.error)
          throw new Error(data.error || 'Error al renovar token')
        }

        this.token = data.access_token
        if (typeof window !== 'undefined') {
          localStorage.setItem('access_token', data.access_token)
        }

        // Emitir evento para que otros componentes sepan que el token se renovó
        if (typeof window !== 'undefined') {
          window.dispatchEvent(new CustomEvent('tokenRefreshed', { 
            detail: { newToken: data.access_token } 
          }))
        }

        console.log('Token renovado exitosamente')
        return data.access_token
      } catch (error: any) {
        console.log('Error en refresh token:', error.message)
        // Si el refresh falla, manejar sesión expirada
        this.handleSessionExpired()
        throw error
      }
    },

    startTokenRefresh() {
      // Limpiar intervalo anterior si existe
      if (this.refreshInterval) {
        clearInterval(this.refreshInterval)
      }

      // Obtener configuración del runtime config
      const config = useRuntimeConfig()
      const refreshInterval = config.public.jwtRefreshInterval * 1000 // convertir a milisegundos

      // Verificar si el token está cerca de expirar según configuración
      this.refreshInterval = setInterval(async () => {
        if (this.token && this.refreshToken) {
          try {
            console.log('Renovando token automáticamente...')
            await this.refreshAccessToken()
            console.log('Token renovado automáticamente')
          } catch (error) {
            console.log('Error renovando token automáticamente:', error)
            // Si no se puede renovar automáticamente, manejar sesión expirada
            this.handleSessionExpired()
          }
        }
      }, refreshInterval)
    },

    async makeAuthenticatedRequest(url: string, options: RequestInit = {}) {
      const config = useRuntimeConfig()
      const fullUrl = url.startsWith('http') ? url : `${config.public.apiBase}${url}`
      
      // Don't set Content-Type for FormData, let the browser set it with boundary
      const isFormData = options.body instanceof FormData
      const headers: Record<string, string> = {
        'Authorization': `Bearer ${this.token}`,
        ...(options.headers as Record<string, string> || {})
      }
      
      if (!isFormData) {
        headers['Content-Type'] = 'application/json'
      }
      
      let response = await fetch(fullUrl, {
        ...options,
        headers
      })

      // Si el token expiró, intentar renovarlo
      if (response.status === 401 && this.refreshToken) {
        try {
          await this.refreshAccessToken()
          // Reintentar la petición con el nuevo token
          const retryHeaders: Record<string, string> = {
            'Authorization': `Bearer ${this.token}`,
            ...(options.headers as Record<string, string> || {})
          }
          
          if (!isFormData) {
            retryHeaders['Content-Type'] = 'application/json'
          }
          
          response = await fetch(fullUrl, {
            ...options,
            headers: retryHeaders
          })
        } catch (error) {
          // Si no se puede renovar, manejar sesión expirada
          console.log('No se pudo renovar el token, cerrando sesión...')
          this.handleSessionExpired()
          throw new Error('Sesión expirada. Por favor, inicia sesión nuevamente.')
        }
      }

      return response
    },

    async register(userData: RegisterData) {
      this.isLoading = true
      this.error = null

      try {
        const config = useRuntimeConfig()
        const url = `${config.public.apiBase}/api/auth/register`
        const body = JSON.stringify(userData)
        
        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: body
        })

        const data = await response.json()

        if (!response.ok) {
          throw new Error(data.error || data.message || 'Error al registrar usuario')
        }

        return { success: true, message: data.message || 'Usuario registrado exitosamente' }
      } catch (error: any) {
        this.error = error.message
        return { success: false, error: error.message }
      } finally {
        this.isLoading = false
      }
    },

    async resetPassword(email: string) {
      this.isLoading = true
      this.error = null

      try {
        const config = useRuntimeConfig()
        const response = await fetch(`${config.public.apiBase}/api/auth/reset-password`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ email })
        })

        const data = await response.json()

        if (!response.ok) {
          throw new Error(data.error || data.message || 'Error al enviar correo de recuperación')
        }

        return { success: true, message: data.message || 'Correo de recuperación enviado' }
      } catch (error: any) {
        this.error = error.message
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async validateResetToken(token: string) {
      this.isLoading = true
      this.error = null

      try {
        const config = useRuntimeConfig()
        const response = await fetch(`${config.public.apiBase}/api/auth/reset-password/validate`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ token })
        })

        const data = await response.json()

        if (!response.ok) {
          throw new Error(data.error || data.message || 'Token inválido')
        }

        return { success: true, valid: data.valid, user_id: data.user_id, username: data.username }
      } catch (error: any) {
        this.error = error.message
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async confirmPasswordReset(token: string, newPassword: string) {
      this.isLoading = true
      this.error = null

      try {
        const config = useRuntimeConfig()
        const response = await fetch(`${config.public.apiBase}/api/auth/reset-password/confirm`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ token, new_password: newPassword })
        })

        const data = await response.json()

        if (!response.ok) {
          throw new Error(data.error || data.message || 'Error al cambiar contraseña')
        }

        return { success: true, message: data.message || 'Contraseña actualizada exitosamente' }
      } catch (error: any) {
        this.error = error.message
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async logout(redirectToLogin: boolean = true) {
      // Limpiar intervalo de refresh
      if (this.refreshInterval) {
        clearInterval(this.refreshInterval)
        this.refreshInterval = null
      }
      
      this.user = null
      this.token = null
      this.refreshToken = null
      this.error = null

      // Limpiar carrito
      const { useCarritoStore } = await import('./carrito')
      const carrito = useCarritoStore()
      carrito.vaciar()

      // Limpiar localStorage
      if (typeof window !== 'undefined') {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('user')
      }

      // Solo redirigir al login si se solicita explícitamente
      if (redirectToLogin) {
        await navigateTo('/login')
      }
    },

    initializeAuth() {
      // Cargar datos del localStorage al inicializar
      if (typeof window !== 'undefined') {
        // Si ya tenemos tokens, no hacer nada
        if (this.hasTokens) {
          console.log('Auth ya inicializada, saltando...')
          return
        }
        
        console.log('=== INICIALIZANDO AUTH ===')
        
        const token = localStorage.getItem('access_token')
        const refreshToken = localStorage.getItem('refresh_token')
        const userStr = localStorage.getItem('user')

        if (token && refreshToken && userStr) {
          try {
            // Verificar si el token está expirado al inicializar
            try {
              if (!token || typeof token !== 'string') {
                this.handleSessionExpired()
                return
              }
              
              const tokenParts = token.split('.')
              if (tokenParts.length !== 3) {
                this.handleSessionExpired()
                return
              }
              const payload = JSON.parse(atob(tokenParts[1] as string))
              const currentTime = Math.floor(Date.now() / 1000)
              const config = useRuntimeConfig()
              const refreshThreshold = config.public.jwtRefreshThreshold
              
              // Verificar si el token expira en menos del threshold configurado
              const timeUntilExpiry = payload.exp - currentTime
              
              if (payload.exp && payload.exp < currentTime) {
                console.log('Token expirado al inicializar, intentando renovar...')
                // Asignar tokens temporalmente para poder renovar
                this.token = token
                this.refreshToken = refreshToken
                this.user = JSON.parse(userStr)
                // Intentar renovar el token
                this.refreshAccessToken().catch(() => {
                  // Si no se puede renovar, limpiar sesión
                  this.handleSessionExpired()
                })
              } else if (timeUntilExpiry < refreshThreshold) {
                console.log(`Token expira pronto (en ${timeUntilExpiry}s), renovando inmediatamente...`)
                // Asignar tokens temporalmente para poder renovar
                this.token = token
                this.refreshToken = refreshToken
                this.user = JSON.parse(userStr)
                // Renovar inmediatamente si expira en menos del threshold configurado
                this.refreshAccessToken().catch(() => {
                  this.handleSessionExpired()
                })
              } else {
                // Asignar tokens solo si están válidos
                this.token = token
                this.refreshToken = refreshToken
                this.user = JSON.parse(userStr)
                
                // Iniciar refresh automático solo si no está ya iniciado
                if (!this.refreshInterval) {
                  this.startTokenRefresh()
                }
              }
            } catch (tokenError) {
              console.error('Error al verificar token:', tokenError)
              // Si no se puede verificar el token, limpiar sesión
              this.handleSessionExpired()
            }
          } catch (error) {
            console.error('Error al inicializar autenticación:', error)
            // Si hay error al parsear, limpiar todo
            this.handleSessionExpired()
          }
        }
      }
    }
  }
})




