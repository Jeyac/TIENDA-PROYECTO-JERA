<template>
  <div class="auth-page">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-6 col-lg-5">
          <div class="auth-card">
            <div class="auth-header text-center mb-4">
              <i class="bi bi-person-plus display-4 text-primary mb-3"></i>
              <h2 class="fw-bold">Crear Cuenta</h2>
              <p class="text-muted">Regístrate para acceder a todos nuestros servicios</p>
            </div>

            <form @submit.prevent="handleRegister" class="auth-form">
              <div class="mb-3">
                <label for="username" class="form-label fw-semibold">
                  <i class="bi bi-person me-1"></i>Nombre de Usuario
                </label>
                <input
                  v-model="form.username"
                  type="text"
                  class="form-control"
                  :class="{ 'is-invalid': usernameError, 'is-valid': form.username && !usernameError && form.username.length >= 3 }"
                  id="username"
                  placeholder="Ingresa tu nombre de usuario"
                  required
                  minlength="3"
                  maxlength="50"
                  :disabled="auth.isLoading"
                  @blur="validateUsername"
                >
                <div v-if="usernameError" class="invalid-feedback">
                  <i class="bi bi-exclamation-triangle me-1"></i>{{ usernameError }}
                </div>
                <div v-else class="form-text">
                  <i class="bi bi-info-circle me-1"></i>Mínimo 3 caracteres, máximo 50
                </div>
              </div>

              <div class="mb-3">
                <label for="email" class="form-label fw-semibold">
                  <i class="bi bi-envelope me-1"></i>Correo Electrónico
                </label>
                <input
                  v-model="form.email"
                  type="email"
                  class="form-control"
                  :class="{ 'is-invalid': emailError, 'is-valid': form.email && !emailError && isValidEmail }"
                  id="email"
                  placeholder="tu@correo.com"
                  required
                  :disabled="auth.isLoading"
                  @blur="validateEmail"
                >
                <div v-if="emailError" class="invalid-feedback">
                  <i class="bi bi-exclamation-triangle me-1"></i>{{ emailError }}
                </div>
              </div>

              <div class="mb-3">
                <label for="password" class="form-label fw-semibold">
                  <i class="bi bi-lock me-1"></i>Contraseña
                </label>
                <div class="input-group">
                  <input
                    v-model="form.password"
                    :type="showPassword ? 'text' : 'password'"
                    class="form-control"
                    id="password"
                    placeholder="Crea una contraseña segura"
                    required
                    minlength="8"
                    :disabled="auth.isLoading"
                  >
                  <button
                    type="button"
                    class="btn btn-outline-secondary"
                    @click="showPassword = !showPassword"
                    :disabled="auth.isLoading"
                  >
                    <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
                  </button>
                </div>
                <div class="form-text">
                  <i class="bi bi-shield-check me-1"></i>Mínimo 8 caracteres
                </div>
              </div>

              <div class="mb-3">
                <label for="confirm_password" class="form-label fw-semibold">
                  <i class="bi bi-lock-fill me-1"></i>Confirmar Contraseña
                </label>
                <div class="input-group">
                  <input
                    v-model="form.confirm_password"
                    :type="showConfirmPassword ? 'text' : 'password'"
                    class="form-control"
                    id="confirm_password"
                    placeholder="Repite tu contraseña"
                    required
                    :disabled="auth.isLoading"
                  >
                  <button
                    type="button"
                    class="btn btn-outline-secondary"
                    @click="showConfirmPassword = !showConfirmPassword"
                    :disabled="auth.isLoading"
                  >
                    <i :class="showConfirmPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
                  </button>
                </div>
              </div>

              <!-- Password validation -->
              <div v-if="form.password" class="mb-3">
                <div class="password-strength">
                  <small class="text-muted d-block mb-2">Requisitos de contraseña:</small>
                  <div class="d-flex flex-wrap gap-2">
                    <span class="badge" :class="form.password.length >= 8 ? 'bg-success' : 'bg-secondary'">
                      <i class="bi bi-check-circle me-1"></i>8+ caracteres
                    </span>
                    <span class="badge" :class="hasUppercase ? 'bg-success' : 'bg-secondary'">
                      <i class="bi bi-check-circle me-1"></i>Mayúscula
                    </span>
                    <span class="badge" :class="hasLowercase ? 'bg-success' : 'bg-secondary'">
                      <i class="bi bi-check-circle me-1"></i>Minúscula
                    </span>
                    <span class="badge" :class="hasNumber ? 'bg-success' : 'bg-secondary'">
                      <i class="bi bi-check-circle me-1"></i>Número
                    </span>
                  </div>
                </div>
              </div>

              <!-- Password match validation -->
              <div v-if="form.confirm_password && form.password !== form.confirm_password" class="mb-3">
                <div class="alert alert-warning" role="alert">
                  <i class="bi bi-exclamation-triangle me-2"></i>Las contraseñas no coinciden
                </div>
              </div>

              <div v-if="auth.error" class="alert alert-danger" role="alert">
                <i class="bi bi-exclamation-triangle me-2"></i>{{ auth.error }}
              </div>

              <div v-if="successMessage" class="alert alert-success" role="alert">
                <i class="bi bi-check-circle me-2"></i>{{ successMessage }}
              </div>

              <BaseButton
                type="submit"
                class="w-100 py-2 fw-semibold"
                variant="primary"
                :loading="auth.isLoading"
                :disabled="auth.isLoading || !isFormValid"
              >
                <i v-if="!auth.isLoading" class="bi bi-person-plus me-2"></i>
                {{ auth.isLoading ? 'Creando cuenta...' : 'Crear Cuenta' }}
              </BaseButton>
            </form>

            <div class="auth-footer text-center mt-4">
              <p class="text-muted mb-0">
                ¿Ya tienes una cuenta?
                <NuxtLink to="/login" class="text-decoration-none fw-semibold">
                  Inicia sesión aquí
                </NuxtLink>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { navigateTo } from 'nuxt/app'
import { useAuthStore } from '../../stores/auth'

const auth = useAuthStore()

// Form data
const form = reactive({
  username: '',
  email: '',
  password: '',
  confirm_password: ''
})

// UI state
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const successMessage = ref('')

// Validation errors
const usernameError = ref('')
const emailError = ref('')

// Password validation computed properties
const hasUppercase = computed(() => /[A-Z]/.test(form.password))
const hasLowercase = computed(() => /[a-z]/.test(form.password))
const hasNumber = computed(() => /\d/.test(form.password))

// Email validation
const isValidEmail = computed(() => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(form.email)
})

// Form validation
const isFormValid = computed(() => {
  return form.username.length >= 3 &&
         form.username.length <= 50 &&
         !usernameError.value &&
         isValidEmail.value &&
         !emailError.value &&
         form.password.length >= 8 &&
         form.password === form.confirm_password &&
         hasUppercase.value &&
         hasLowercase.value &&
         hasNumber.value
})

// Validation functions
const validateUsername = async () => {
  usernameError.value = ''
  
  if (!form.username) {
    usernameError.value = 'El nombre de usuario es requerido'
    return
  }
  
  if (form.username.length < 3) {
    usernameError.value = 'El nombre de usuario debe tener al menos 3 caracteres'
    return
  }
  
  if (form.username.length > 50) {
    usernameError.value = 'El nombre de usuario no puede tener más de 50 caracteres'
    return
  }
  
  // Verificar disponibilidad en tiempo real (opcional)
  try {
    const response = await $fetch('/api/auth/check-username', {
      method: 'POST',
      body: { username: form.username }
    })
    if (!response.available) {
      usernameError.value = 'Este nombre de usuario ya está en uso'
    }
  } catch (error) {
    // Si el endpoint no existe, no mostrar error
    console.log('Username check endpoint not available')
  }
}

const validateEmail = async () => {
  emailError.value = ''
  
  if (!form.email) {
    emailError.value = 'El correo electrónico es requerido'
    return
  }
  
  if (!isValidEmail.value) {
    emailError.value = 'Formato de correo electrónico inválido'
    return
  }
  
  // Verificar disponibilidad en tiempo real (opcional)
  try {
    const response = await $fetch('/api/auth/check-email', {
      method: 'POST',
      body: { email: form.email }
    })
    if (!response.available) {
      emailError.value = 'Este correo electrónico ya está registrado'
    }
  } catch (error) {
    // Si el endpoint no existe, no mostrar error
    console.log('Email check endpoint not available')
  }
}

// Handle registration
const handleRegister = async () => {
  if (!isFormValid.value) return

  // Limpiar errores previos
  usernameError.value = ''
  emailError.value = ''

  // Preparar datos para el backend (sin confirm_password)
  const userData = {
    username: form.username.trim(),
    email: form.email.trim().toLowerCase(),
    password: form.password
  }

  try {
    const result = await auth.register(userData)
    
    if (result.success) {
      successMessage.value = result.message || 'Cuenta creada exitosamente'
      setTimeout(async () => {
        await navigateTo('/login')
      }, 2000)
    } else {
      // Manejar errores específicos del backend
      if (result.error) {
        if (result.error.includes('username') && result.error.includes('uso')) {
          usernameError.value = 'Este nombre de usuario ya está en uso'
        } else if (result.error.includes('email') && result.error.includes('registrado')) {
          emailError.value = 'Este correo electrónico ya está registrado'
        } else if (result.error.includes('caracteres')) {
          if (result.error.includes('username')) {
            usernameError.value = result.error
          } else if (result.error.includes('contraseña')) {
            // Mostrar error general de contraseña
            auth.error = result.error
          }
        } else {
          auth.error = result.error
        }
      }
    }
  } catch (error) {
    console.error('Error en registro:', error)
    auth.error = 'Error al crear la cuenta. Intenta de nuevo.'
  }
}

// Initialize auth on mount
onMounted(() => {
  auth.initializeAuth()
})
</script>

<style scoped>
.auth-page {
  min-height: 80vh;
  display: flex;
  align-items: center;
  padding: 2rem 0;
}

.auth-card {
  background: var(--bs-body-bg);
  border: 1px solid var(--bs-border-color);
  border-radius: 1rem;
  padding: 2rem;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.1);
}

.auth-header {
  margin-bottom: 2rem;
}

.auth-form .form-label {
  color: var(--bs-body-color);
  margin-bottom: 0.5rem;
}

.auth-form .form-control {
  border-radius: 0.5rem;
  border: 1px solid var(--bs-border-color);
  padding: 0.75rem;
  transition: all 0.3s ease;
}

.auth-form .form-control:focus {
  border-color: var(--bs-primary);
  box-shadow: 0 0 0 0.2rem rgba(var(--bs-primary-rgb), 0.25);
}

.auth-form .input-group .btn {
  border-radius: 0 0.5rem 0.5rem 0;
}

.auth-form .btn-primary {
  border-radius: 0.5rem;
  font-weight: 600;
  transition: all 0.3s ease;
}

.auth-form .btn-primary:hover {
  transform: translateY(-1px);
}

.auth-form .btn-primary:disabled {
  transform: none;
  opacity: 0.6;
}

.auth-footer a {
  color: var(--bs-primary);
  transition: color 0.3s ease;
}

.auth-footer a:hover {
  color: var(--bs-primary);
  text-decoration: underline !important;
}

.password-strength {
  background: var(--bs-gray-100);
  border-radius: 0.5rem;
  padding: 0.75rem;
  border: 1px solid var(--bs-border-color);
}

.password-strength .badge {
  font-size: 0.75rem;
  padding: 0.25rem 0.5rem;
}

.form-text {
  color: var(--bs-secondary);
  font-size: 0.875rem;
}

/* Dark theme adjustments */
.dark-theme .auth-card {
  background-color: var(--bs-gray-100);
  border-color: var(--bs-border-color);
}

.dark-theme .password-strength {
  background-color: var(--bs-gray-200);
  border-color: var(--bs-border-color);
}
</style>
