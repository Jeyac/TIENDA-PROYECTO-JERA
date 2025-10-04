<template>
  <div class="admin-redirect-page">
    <div class="container-fluid d-flex align-items-center justify-content-center min-vh-100">
      <div class="text-center">
        <div class="spinner-border text-primary mb-3" role="status">
          <span class="visually-hidden">Cargando...</span>
        </div>
        <h4 class="text-primary">Redirigiendo al Panel de Administración...</h4>
        <p class="text-muted">Por favor espera un momento</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '../stores/auth'

// Middleware para proteger la ruta
definePageMeta({
  middleware: 'admin'
})

const auth = useAuthStore()

// Redirigir inmediatamente al dashboard de admin
onMounted(() => {
  navigateTo('/admin')
})
</script>

<style scoped>
.admin-redirect-page {
  background-color: #f8f9fa;
}
</style>
