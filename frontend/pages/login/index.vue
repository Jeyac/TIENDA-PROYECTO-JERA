<template>
  <div class="auth-page">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-6 col-lg-5">
          <div class="auth-card">
            <div class="auth-header text-center mb-4">
              <i class="bi bi-person-circle display-4 text-primary mb-3"></i>
              <h2 class="fw-bold">Iniciar sesión</h2>
              <p class="text-muted">Accede a tu cuenta para continuar</p>
            </div>

            <form @submit.prevent="handleLogin" class="auth-form">
              <div class="mb-3">
                <label for="username_or_email" class="form-label fw-semibold">
                  <i class="bi bi-person me-1"></i>Usuario o correo
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
                type="button"
                class="btn btn-outline-secondary btn-modern"
                @click="showPassword = !showPassword"
                :disabled="auth.isLoading"
              >
                <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
              </button>
                </div>
              </div>

              <div class="mb-3 text-end">
              <BaseButton
                type="button"
                class="btn btn-link p-0 text-decoration-none"
                variant="link"
                @click="showResetModal = true"
                :disabled="auth.isLoading"
              >
                <i class="bi bi-question-circle me-1"></i>¿Olvidaste tu contraseña?
              </BaseButton>
              </div>

              <div v-if="auth.error" class="alert alert-danger" role="alert">
                <i class="bi bi-exclamation-triangle me-2"></i>{{ auth.error }}
              </div>

              <BaseButton
                type="submit"
                class="w-100 py-2 fw-semibold"
                variant="primary"
                :loading="auth.isLoading"
                :disabled="auth.isLoading"
              >
                <i v-if="!auth.isLoading" class="bi bi-box-arrow-in-right me-2"></i>
                {{ auth.isLoading ? 'Iniciando sesión...' : 'Iniciar Sesión' }}
              </BaseButton>
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
              <i class="bi bi-key me-2"></i>Recuperar contraseña
            </h5>
            <button type="button" class="btn-close" @click="showResetModal = false"></button>
          </div>
          <div class="modal-body">
            <p class="text-muted mb-3">
              Ingresa tu correo electrónico y te enviaremos un enlace para restablecer tu contraseña.
            </p>
            <form @submit.prevent="handleResetPassword">
              <div class="mb-3">
                <label for="reset_email" class="form-label">Correo electrónico</label>
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
                <BaseButton type="button" variant="secondary" class="flex-fill" @click="showResetModal = false">
                  Cancelar
                </BaseButton>
                <BaseButton type="submit" variant="primary" class="flex-fill" :loading="auth.isLoading" :disabled="auth.isLoading">
                  Enviar Enlace
                </BaseButton>
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
  
  if (result.success && result.user) {
    // Redirigir según el rol del usuario
    let redirect = (route.query.next as string) || '/'
    
    // Si no hay un destino específico, redirigir según el rol
    if (!route.query.next) {
      switch (result.user.rol) {
        case 'atencion_cliente':
          redirect = '/atencion/tickets'
          break
        default:
          redirect = '/'
      }
    }
    
    await navigateTo(redirect)
  }
}

// Handle password reset
const handleResetPassword = async () => {
  const result = await auth.resetPassword(resetForm.email)
  
  if (result.success) {
    resetMessage.value = { type: 'success', text: result.message || 'Correo enviado exitosamente' }
    setTimeout(() => {
      showResetModal.value = false
      resetMessage.value = null
      resetForm.email = ''
    }, 2000)
  } else {
    resetMessage.value = { type: 'error', text: result.message || 'Error al enviar correo' }
  }
}

// Initialize auth on mount
onMounted(() => {
  auth.initializeAuth()
})
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
  overflow: hidden;
}

.auth-page::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%);
  pointer-events: none;
  animation: float 6s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(5deg); }
}

.auth-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 2.5rem;
  padding: 3.5rem;
  box-shadow: 
    0 25px 50px rgba(102, 126, 234, 0.2),
    0 10px 20px rgba(102, 126, 234, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  position: relative;
  overflow: hidden;
  transform: translateY(0);
  transition: all 0.3s ease;
}

.auth-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, transparent 100%);
  pointer-events: none;
}

.auth-card:hover {
  transform: translateY(-5px);
  box-shadow: 
    0 35px 70px rgba(102, 126, 234, 0.25),
    0 15px 30px rgba(102, 126, 234, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

.auth-header {
  margin-bottom: 2rem;
}

.auth-form .form-label {
  color: var(--bs-body-color);
  margin-bottom: 0.5rem;
}

/* Los estilos globales ya se aplican automáticamente */

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


