<template>
  <div class="orders-page">
    <div class="container">
      <div class="row">
        <div class="col-12">
          <h1 class="display-6 fw-bold mb-4">
            <i class="bi bi-bag me-2"></i>Mis Pedidos
          </h1>
        </div>
      </div>
      
      <div class="row">
        <div class="col-12">
          <div class="card">
            <div class="card-header">
              <h5 class="card-title mb-0">Historial de Pedidos</h5>
            </div>
            <div class="card-body">
              <div v-if="loading" class="text-center py-4">
                <div class="spinner-border text-primary" role="status">
                  <span class="visually-hidden">Cargando...</span>
                </div>
                <p class="mt-2 text-muted">Cargando pedidos...</p>
              </div>
              
              <div v-else-if="error" class="alert alert-danger">
                <i class="bi bi-exclamation-triangle me-2"></i>{{ error }}
              </div>
              
              <div v-else-if="orders.length === 0" class="text-center py-5">
                <i class="bi bi-bag text-muted" style="font-size: 4rem;"></i>
                <h3 class="text-muted mt-3">No tienes pedidos aún</h3>
                <p class="text-muted">¡Explora nuestro catálogo y haz tu primer pedido!</p>
                <NuxtLink to="/catalogo" class="btn btn-primary">
                  <i class="bi bi-grid me-2"></i>Ver Catálogo
                </NuxtLink>
              </div>
              
              <div v-else>
                <div v-for="order in orders" :key="order.id" class="card mb-3">
                  <div class="card-body">
                    <div class="row align-items-center">
                      <div class="col-md-3">
                        <h6 class="mb-1">Pedido #{{ order.id }}</h6>
                        <small class="text-muted">{{ formatDate(order.fecha_creacion) }}</small>
                      </div>
                      <div class="col-md-3">
                        <span class="badge bg-primary">{{ order.estado || 'Pendiente' }}</span>
                      </div>
                      <div class="col-md-3">
                        <strong>Q {{ Number(order.total).toFixed(2) }}</strong>
                      </div>
                      <div class="col-md-3 text-end">
                        <button class="btn btn-outline-primary btn-sm" @click="viewOrderDetails(order)">
                          <i class="bi bi-eye me-1"></i>Ver Detalles
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRuntimeConfig } from 'nuxt/app'
import { useAuthStore } from '../../stores/auth'

// Middleware para proteger la ruta
definePageMeta({
  middleware: 'auth'
})

const config = useRuntimeConfig()
const auth = useAuthStore()

// Data
const orders = ref<any[]>([])
const loading = ref(false)
const error = ref('')

// Methods
const loadOrders = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const response = await fetch(`${config.public.apiBase}/api/pedidos/`, {
      headers: {
        'Authorization': `Bearer ${auth.token}`
      }
    })
    
    if (response.ok) {
      orders.value = await response.json()
    } else if (response.status === 401) {
      await auth.logout()
    } else {
      error.value = 'Error al cargar los pedidos'
    }
  } catch (err: any) {
    error.value = err.message || 'Error de conexión'
  } finally {
    loading.value = false
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('es-GT', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const viewOrderDetails = (order: any) => {
  // Por ahora solo mostramos un alert, pero aquí podrías abrir un modal o navegar a una página de detalles
  alert(`Detalles del pedido #${order.id}\nTotal: Q ${Number(order.total).toFixed(2)}\nEstado: ${order.estado || 'Pendiente'}`)
}

// Lifecycle
onMounted(() => {
  loadOrders()
})
</script>

<style scoped>
.orders-page {
  min-height: 100vh;
  background-color: #f8f9fa;
  padding: 20px 0;
}
</style>
