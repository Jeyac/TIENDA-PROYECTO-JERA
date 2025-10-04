<template>
  <div class="analytics-page">
    <div class="container-fluid">
      <!-- Header -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <h1 class="display-6 fw-bold mb-2">
                <i class="bi bi-graph-up me-2"></i>Analytics
              </h1>
              <p class="text-muted mb-0">Panel de control y métricas del sistema</p>
            </div>
            <div class="text-end">
              <small class="text-muted">Última actualización: {{ lastUpdate }}</small>
            </div>
          </div>
        </div>
      </div>

      <!-- KPIs Cards -->
      <div class="row g-4 mb-4">
        <div class="col-md-3">
          <div class="card kpi-card border-0 shadow-sm">
            <div class="card-body text-center">
              <div class="kpi-icon bg-primary text-white rounded-circle mx-auto mb-3">
                <i class="bi bi-people"></i>
              </div>
              <h3 class="fw-bold text-primary">{{ kpis.total_usuarios || 0 }}</h3>
              <p class="text-muted mb-0">Total Usuarios</p>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card kpi-card border-0 shadow-sm">
            <div class="card-body text-center">
              <div class="kpi-icon bg-success text-white rounded-circle mx-auto mb-3">
                <i class="bi bi-box"></i>
              </div>
              <h3 class="fw-bold text-success">{{ kpis.total_productos || 0 }}</h3>
              <p class="text-muted mb-0">Total Productos</p>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card kpi-card border-0 shadow-sm">
            <div class="card-body text-center">
              <div class="kpi-icon bg-warning text-white rounded-circle mx-auto mb-3">
                <i class="bi bi-bag"></i>
              </div>
              <h3 class="fw-bold text-warning">{{ kpis.total_pedidos || 0 }}</h3>
              <p class="text-muted mb-0">Total Pedidos</p>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card kpi-card border-0 shadow-sm">
            <div class="card-body text-center">
              <div class="kpi-icon bg-info text-white rounded-circle mx-auto mb-3">
                <i class="bi bi-chat-dots"></i>
              </div>
              <h3 class="fw-bold text-info">{{ kpis.total_chats || 0 }}</h3>
              <p class="text-muted mb-0">Total Chats</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Charts Row -->
      <div class="row g-4 mb-4">
        <div class="col-lg-8">
          <div class="card border-0 shadow-sm">
            <div class="card-header bg-white border-bottom">
              <h5 class="card-title mb-0">
                <i class="bi bi-bar-chart me-2"></i>Pedidos por Mes
              </h5>
            </div>
            <div class="card-body">
              <div class="chart-placeholder">
                <i class="bi bi-graph-up text-muted" style="font-size: 4rem;"></i>
                <p class="text-muted mt-2">Gráfico de pedidos por mes</p>
                <small class="text-muted">Integración con Chart.js pendiente</small>
              </div>
            </div>
          </div>
        </div>
        <div class="col-lg-4">
          <div class="card border-0 shadow-sm">
            <div class="card-header bg-white border-bottom">
              <h5 class="card-title mb-0">
                <i class="bi bi-pie-chart me-2"></i>Productos por Categoría
              </h5>
            </div>
            <div class="card-body">
              <div class="chart-placeholder">
                <i class="bi bi-pie-chart text-muted" style="font-size: 4rem;"></i>
                <p class="text-muted mt-2">Distribución por categorías</p>
                <small class="text-muted">Integración con Chart.js pendiente</small>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Activity -->
      <div class="row g-4">
        <div class="col-lg-6">
          <div class="card border-0 shadow-sm">
            <div class="card-header bg-white border-bottom">
              <h5 class="card-title mb-0">
                <i class="bi bi-clock-history me-2"></i>Pedidos Recientes
              </h5>
            </div>
            <div class="card-body">
              <div v-if="recentOrders.length === 0" class="text-center py-4">
                <i class="bi bi-bag text-muted" style="font-size: 3rem;"></i>
                <p class="text-muted mt-2">No hay pedidos recientes</p>
              </div>
              <div v-else class="list-group list-group-flush">
                <div v-for="order in recentOrders" :key="order.id" class="list-group-item px-0 border-0">
                  <div class="d-flex justify-content-between align-items-center">
                    <div>
                      <h6 class="mb-1">{{ order.usuario_nombre || 'Usuario' }}</h6>
                      <p class="text-muted mb-0 small">{{ order.fecha_creacion }}</p>
                    </div>
                    <div class="text-end">
                      <span class="badge bg-primary">Q {{ Number(order.total).toFixed(2) }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-lg-6">
          <div class="card border-0 shadow-sm">
            <div class="card-header bg-white border-bottom">
              <h5 class="card-title mb-0">
                <i class="bi bi-chat-text me-2"></i>Chats Recientes
              </h5>
            </div>
            <div class="card-body">
              <div v-if="recentChats.length === 0" class="text-center py-4">
                <i class="bi bi-chat text-muted" style="font-size: 3rem;"></i>
                <p class="text-muted mt-2">No hay chats recientes</p>
              </div>
              <div v-else class="list-group list-group-flush">
                <div v-for="chat in recentChats" :key="chat.id" class="list-group-item px-0 border-0">
                  <div class="d-flex justify-content-between align-items-center">
                    <div>
                      <h6 class="mb-1">{{ chat.usuario_nombre || 'Usuario' }}</h6>
                      <p class="text-muted mb-0 small">{{ chat.mensaje.substring(0, 50) }}...</p>
                    </div>
                    <div class="text-end">
                      <small class="text-muted">{{ chat.fecha_creacion }}</small>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Cargando...</span>
        </div>
        <p class="text-muted mt-3">Cargando analytics...</p>
      </div>

      <!-- Error State -->
      <div v-if="error" class="alert alert-danger" role="alert">
        <i class="bi bi-exclamation-triangle me-2"></i>{{ error }}
        <button class="btn btn-outline-danger btn-sm ms-2" @click="loadData">
          <i class="bi bi-arrow-clockwise me-1"></i>Reintentar
        </button>
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
  middleware: 'admin',
  layout: 'admin'
})

const config = useRuntimeConfig()
const auth = useAuthStore()

// Data
const kpis = ref<any>({})
const recentOrders = ref<any[]>([])
const recentChats = ref<any[]>([])
const loading = ref(false)
const error = ref('')
const lastUpdate = ref('')

// Methods
const loadData = async () => {
  loading.value = true
  error.value = ''
  
  try {
    // Load KPIs
    const kpisRes = await fetch(`${config.public.apiBase}/api/admin/kpis`, {
      headers: {
        'Authorization': `Bearer ${auth.token}`
      }
    })
    
    if (kpisRes.ok) {
      kpis.value = await kpisRes.json()
    } else if (kpisRes.status === 401) {
      await auth.logout()
      return
    }

    // Load recent orders
    const ordersRes = await fetch(`${config.public.apiBase}/api/admin/pedidos`, {
      headers: {
        'Authorization': `Bearer ${auth.token}`
      }
    })
    
    if (ordersRes.ok) {
      const orders = await ordersRes.json()
      recentOrders.value = orders.slice(0, 5) // Last 5 orders
    }

    // Load recent chats
    const chatsRes = await fetch(`${config.public.apiBase}/api/admin/chats`, {
      headers: {
        'Authorization': `Bearer ${auth.token}`
      }
    })
    
    if (chatsRes.ok) {
      const chats = await chatsRes.json()
      recentChats.value = chats.slice(0, 5) // Last 5 chats
    }

    lastUpdate.value = new Date().toLocaleString()
  } catch (err: any) {
    error.value = err.message || 'Error al cargar los datos'
  } finally {
    loading.value = false
  }
}

// Lifecycle
onMounted(() => {
  if (auth.isAuthenticated && auth.isAdmin) {
    loadData()
  }
})
</script>

<style scoped>
.analytics-page {
  padding: 2rem 0;
}

.kpi-card {
  transition: transform 0.3s ease;
}

.kpi-card:hover {
  transform: translateY(-5px);
}

.kpi-icon {
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.chart-placeholder {
  height: 300px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: var(--bs-gray-100);
  border-radius: 0.5rem;
}

.list-group-item {
  padding: 1rem 0;
}

.list-group-item:not(:last-child) {
  border-bottom: 1px solid var(--bs-border-color) !important;
}

/* Dark theme adjustments */
.dark-theme .chart-placeholder {
  background-color: var(--bs-gray-200);
}

.dark-theme .card-header {
  background-color: var(--bs-gray-100) !important;
}
</style>
