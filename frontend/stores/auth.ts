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
    error: null as string | null
  }),

  getters: {
    isAuthenticated: (state) => !!state.token && !!state.user,
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

        return { success: true, user: data.user }
      } catch (error: any) {
        this.error = error.message
        return { success: false, error: error.message }
      } finally {
        this.isLoading = false
      }
    },

    async register(userData: RegisterData) {
      this.isLoading = true
      this.error = null

      try {
        const config = useRuntimeConfig()
        const response = await fetch(`${config.public.apiBase}/api/auth/register`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(userData)
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

    async resetPassword(resetData: ResetPasswordData) {
      this.isLoading = true
      this.error = null

      try {
        const config = useRuntimeConfig()
        const response = await fetch(`${config.public.apiBase}/api/auth/reset-password`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(resetData)
        })

        const data = await response.json()

        if (!response.ok) {
          throw new Error(data.error || data.message || 'Error al enviar correo de recuperación')
        }

        return { success: true, message: data.message || 'Correo de recuperación enviado' }
      } catch (error: any) {
        this.error = error.message
        return { success: false, error: error.message }
      } finally {
        this.isLoading = false
      }
    },

    async logout() {
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

      // Redirigir al login
      await navigateTo('/login')
    },

    async initializeAuth() {
      if (typeof window !== 'undefined') {
        const token = localStorage.getItem('access_token')
        const refreshToken = localStorage.getItem('refresh_token')
        const userStr = localStorage.getItem('user')

        if (token && refreshToken && userStr) {
          try {
            this.token = token
            this.refreshToken = refreshToken
            this.user = JSON.parse(userStr)
          } catch (error) {
            // Si hay error al parsear, limpiar todo
            this.logout()
          }
        }
      }
    },

    async refreshAccessToken() {
      if (!this.refreshToken) return false

      try {
        const config = useRuntimeConfig()
        const response = await fetch(`${config.public.apiBase}/api/auth/refresh`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.refreshToken}`
          }
        })

        const data = await response.json()

        if (response.ok) {
          this.token = data.access_token
          if (typeof window !== 'undefined') {
            localStorage.setItem('access_token', data.access_token)
          }
          return true
        } else {
          this.logout()
          return false
        }
      } catch (error) {
        this.logout()
        return false
      }
    }
  }
})
