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
                  id="username"
                  placeholder="Ingresa tu nombre de usuario"
                  required
                  minlength="3"
                  maxlength="50"
                  :disabled="auth.isLoading"
                >
                <div class="form-text">
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
                  id="email"
                  placeholder="tu@correo.com"
                  required
                  :disabled="auth.isLoading"
                >
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

// Password validation computed properties
const hasUppercase = computed(() => /[A-Z]/.test(form.password))
const hasLowercase = computed(() => /[a-z]/.test(form.password))
const hasNumber = computed(() => /\d/.test(form.password))

// Form validation
const isFormValid = computed(() => {
  return form.username.length >= 3 &&
         form.email.includes('@') &&
         form.password.length >= 8 &&
         form.password === form.confirm_password &&
         hasUppercase.value &&
         hasLowercase.value &&
         hasNumber.value
})

// Handle registration
const handleRegister = async () => {
  if (!isFormValid.value) return

  // Preparar datos para el backend (sin confirm_password)
  const userData = {
    username: form.username,
    email: form.email,
    password: form.password
  }

  const result = await auth.register(userData)
  
  if (result.success) {
    successMessage.value = result.message || 'Cuenta creada exitosamente'
    setTimeout(async () => {
      await navigateTo('/login')
    }, 2000)
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
