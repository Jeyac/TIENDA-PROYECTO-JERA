<template>
  <div class="profile-page">
    <div class="container">
      <div class="row">
        <div class="col-12">
          <h1 class="display-6 fw-bold mb-4">
            <i class="bi bi-person-circle me-2"></i>Mi Perfil
          </h1>
        </div>
      </div>
      
      <div class="row">
        <div class="col-md-6">
          <div class="card">
            <div class="card-header">
              <h5 class="card-title mb-0">Información Personal</h5>
            </div>
            <div class="card-body">
              <div v-if="auth.isAuthenticated" class="text-center">
                <div class="mb-3">
                  <i class="bi bi-person-circle text-primary" style="font-size: 4rem;"></i>
                </div>
                <h4>{{ auth.userName }}</h4>
                <p class="text-muted">{{ auth.userEmail }}</p>
                <span class="badge bg-primary">{{ auth.user?.rol || 'Usuario' }}</span>
              </div>
              <div v-else class="text-center">
                <p class="text-muted">No hay información de usuario disponible</p>
              </div>
            </div>
          </div>
        </div>
        
        <div class="col-md-6">
          <div class="card">
            <div class="card-header">
              <h5 class="card-title mb-0">Acciones Rápidas</h5>
            </div>
            <div class="card-body">
              <div class="d-grid gap-2">
                <NuxtLink to="/orders" class="btn btn-outline-primary">
                  <i class="bi bi-bag me-2"></i>Ver Mis Pedidos
                </NuxtLink>
                <NuxtLink to="/carrito" class="btn btn-outline-success">
                  <i class="bi bi-cart me-2"></i>Ver Carrito
                </NuxtLink>
                <NuxtLink to="/catalogo" class="btn btn-outline-info">
                  <i class="bi bi-grid me-2"></i>Ver Catálogo
                </NuxtLink>
                <button class="btn btn-outline-danger" @click="auth.logout()">
                  <i class="bi bi-box-arrow-right me-2"></i>Cerrar Sesión
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '../../stores/auth'

// Middleware para proteger la ruta
definePageMeta({
  middleware: 'auth'
})

const auth = useAuthStore()
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
  background-color: #f8f9fa;
  padding: 20px 0;
}
</style>
