<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card">
          <div class="card-header text-center">
            <h2>Restablecer Contraseña</h2>
          </div>
          <div class="card-body">
            <div v-if="!token">
              <p>Ingresa tu email para recibir un enlace de restablecimiento de contraseña.</p>
              <form @submit.prevent="requestReset">
                <div class="mb-3">
                  <label for="email" class="form-label">Email</label>
                  <input type="email" class="form-control" id="email" v-model="email" required>
                </div>
                <button type="submit" class="btn btn-primary w-100">Enviar enlace de restablecimiento</button>
              </form>
            </div>
            <div v-else-if="!tokenValidating && !tokenValid">
              <p class="text-danger">El token de restablecimiento es inválido o ha expirado.</p>
              <NuxtLink to="/login" class="btn btn-secondary w-100">Volver al login</NuxtLink>
            </div>
            <div v-else-if="tokenValidating">
              <p>Validando token...</p>
            </div>
            <div v-else-if="tokenValid">
              <p>Ingresa tu nueva contraseña.</p>
              <form @submit.prevent="confirmReset">
                <div class="mb-3">
                  <label for="newPassword" class="form-label">Nueva contraseña</label>
                  <input type="password" class="form-control" id="newPassword" v-model="newPassword" required minlength="8">
                </div>
                <div class="mb-3">
                  <label for="confirmPassword" class="form-label">Confirmar contraseña</label>
                  <input type="password" class="form-control" id="confirmPassword" v-model="confirmPassword" required>
                </div>
                <button type="submit" class="btn btn-primary w-100">Cambiar contraseña</button>
              </form>
            </div>
            <div v-if="message" :class="{'alert alert-success': isSuccess, 'alert alert-danger': !isSuccess}" class="mt-3">
              {{ message }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '~/stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const token = ref(route.query.token || null)
const newPassword = ref('')
const confirmPassword = ref('')
const message = ref('')
const isSuccess = ref(false)
const tokenValid = ref(false)
const tokenValidating = ref(false)

const requestReset = async () => {
  try {
    const response = await authStore.resetPassword(email.value)
    message.value = response.message
    isSuccess.value = true
  } catch (error) {
    message.value = error.message || 'Error al solicitar el restablecimiento de contraseña.'
    isSuccess.value = false
  }
}

const validateToken = async () => {
  if (!token.value) return
  tokenValidating.value = true
  try {
    const response = await authStore.validateResetToken(token.value)
    tokenValid.value = response.valid
  } catch (error) {
    tokenValid.value = false
    message.value = error.message || 'Token inválido o expirado.'
    isSuccess.value = false
  } finally {
    tokenValidating.value = false
  }
}

const confirmReset = async () => {
  if (newPassword.value !== confirmPassword.value) {
    message.value = 'Las contraseñas no coinciden.'
    isSuccess.value = false
    return
  }
  if (newPassword.value.length < 8) {
    message.value = 'La contraseña debe tener al menos 8 caracteres.'
    isSuccess.value = false
    return
  }
  try {
    const response = await authStore.confirmPasswordReset(token.value, newPassword.value)
    message.value = response.message
    isSuccess.value = true
    setTimeout(() => {
      router.push('/login')
    }, 3000)
  } catch (error) {
    message.value = error.message || 'Error al cambiar la contraseña.'
    isSuccess.value = false
  }
}

onMounted(() => {
  if (token.value) {
    validateToken()
  }
})
</script>

<style scoped>
/* Estilos específicos para esta página si son necesarios */
</style>