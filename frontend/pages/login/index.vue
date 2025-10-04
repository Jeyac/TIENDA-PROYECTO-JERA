<template>
  <div class="auth-page">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-6 col-lg-5">
          <div class="auth-card">
            <div class="auth-header text-center mb-4">
              <i class="bi bi-person-circle display-4 text-primary mb-3"></i>
              <h2 class="fw-bold">Iniciar Sesión</h2>
              <p class="text-muted">Accede a tu cuenta para continuar</p>
            </div>

            <form @submit.prevent="handleLogin" class="auth-form">
              <div class="mb-3">
                <label for="username_or_email" class="form-label fw-semibold">
                  <i class="bi bi-person me-1"></i>Usuario o Correo
                </label>
                <input
                  v-model="form.username_or_email"
                  type="text"
                  class="form-control"
                  id="username_or_email"
                  placeholder="Ingresa tu usuario o correo"
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
                    placeholder="Ingresa tu contraseña"
                    required
                    :disabled="auth.isLoading"
                  >
                  <button
                    class="btn btn-outline-secondary"
                    type="button"
                    @click="showPassword = !showPassword"
                    :disabled="auth.isLoading"
                  >
                    <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
                  </button>
                </div>
              </div>

              <div class="mb-3 text-end">
                <button
                  type="button"
                  class="btn btn-link p-0 text-decoration-none"
                  @click="showResetModal = true"
                  :disabled="auth.isLoading"
                >
                  <i class="bi bi-question-circle me-1"></i>¿Olvidaste tu contraseña?
                </button>
              </div>

              <div v-if="auth.error" class="alert alert-danger" role="alert">
                <i class="bi bi-exclamation-triangle me-2"></i>{{ auth.error }}
              </div>

              <button
                type="submit"
                class="btn btn-primary w-100 py-2 fw-semibold"
                :disabled="auth.isLoading"
              >
                <span v-if="auth.isLoading" class="spinner-border spinner-border-sm me-2"></span>
                <i v-else class="bi bi-box-arrow-in-right me-2"></i>
                {{ auth.isLoading ? 'Iniciando sesión...' : 'Iniciar Sesión' }}
              </button>
            </form>

            <div class="auth-footer text-center mt-4">
              <p class="text-muted mb-0">
                ¿No tienes una cuenta?
                <NuxtLink to="/register" class="text-decoration-none fw-semibold">
                  Regístrate aquí
                </NuxtLink>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de Recuperación de Contraseña -->
    <div class="modal fade" :class="{ show: showResetModal }" :style="{ display: showResetModal ? 'block' : 'none' }" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="bi bi-key me-2"></i>Recuperar Contraseña
            </h5>
            <button type="button" class="btn-close" @click="showResetModal = false"></button>
          </div>
          <div class="modal-body">
            <p class="text-muted mb-3">
              Ingresa tu correo electrónico y te enviaremos un enlace para restablecer tu contraseña.
            </p>
            <form @submit.prevent="handleResetPassword">
              <div class="mb-3">
                <label for="reset_email" class="form-label">Correo Electrónico</label>
                <input
                  v-model="resetForm.email"
                  type="email"
                  class="form-control"
                  id="reset_email"
                  placeholder="tu@correo.com"
                  required
                  :disabled="auth.isLoading"
                >
              </div>
              <div v-if="resetMessage" class="alert" :class="resetMessage.type === 'success' ? 'alert-success' : 'alert-danger'">
                {{ resetMessage.text }}
              </div>
              <div class="d-flex gap-2">
                <button type="button" class="btn btn-secondary flex-fill" @click="showResetModal = false">
                  Cancelar
                </button>
                <button type="submit" class="btn btn-primary flex-fill" :disabled="auth.isLoading">
                  <span v-if="auth.isLoading" class="spinner-border spinner-border-sm me-2"></span>
                  Enviar Enlace
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
    <div v-if="showResetModal" class="modal-backdrop fade show"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRoute, navigateTo } from 'nuxt/app'
import { useAuthStore } from '../../stores/auth'

const auth = useAuthStore()
const route = useRoute()

// Form data
const form = reactive({
  username_or_email: '',
  password: ''
})

// UI state
const showPassword = ref(false)
const showResetModal = ref(false)
const resetForm = reactive({
  email: ''
})
const resetMessage = ref<{ type: 'success' | 'error', text: string } | null>(null)

// Handle login
const handleLogin = async () => {
  const result = await auth.login(form)
  
  if (result.success) {
    // Redirect to intended page or home
    const next = (route.query.next as string) || '/'
    await navigateTo(next)
  }
}

// Handle password reset
const handleResetPassword = async () => {
  const result = await auth.resetPassword(resetForm)
  
  if (result.success) {
    resetMessage.value = { type: 'success', text: result.message || 'Correo enviado exitosamente' }
    setTimeout(() => {
      showResetModal.value = false
      resetMessage.value = null
      resetForm.email = ''
    }, 2000)
  } else {
    resetMessage.value = { type: 'error', text: result.error || 'Error al enviar correo' }
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

.auth-footer a {
  color: var(--bs-primary);
  transition: color 0.3s ease;
}

.auth-footer a:hover {
  color: var(--bs-primary);
  text-decoration: underline !important;
}

.modal-content {
  border-radius: 1rem;
  border: 1px solid var(--bs-border-color);
}

.modal-header {
  border-bottom: 1px solid var(--bs-border-color);
}

.modal-title {
  color: var(--bs-body-color);
}

.btn-link {
  color: var(--bs-primary);
  transition: color 0.3s ease;
}

.btn-link:hover {
  color: var(--bs-primary);
  text-decoration: underline !important;
}

/* Dark theme adjustments */
.dark-theme .auth-card {
  background-color: var(--bs-gray-100);
  border-color: var(--bs-border-color);
}

.dark-theme .modal-content {
  background-color: var(--bs-gray-100);
  border-color: var(--bs-border-color);
}

.dark-theme .modal-header {
  border-bottom-color: var(--bs-border-color);
}
</style>


