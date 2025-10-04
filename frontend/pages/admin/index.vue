<template>
  <div class="admin-dashboard">
    <div class="container-fluid">
      <!-- Header -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <h1 class="display-6 fw-bold mb-2">
                <i class="bi bi-shield-check me-2"></i>Panel de Administración
              </h1>
              <p class="text-muted mb-0">Bienvenido, {{ auth.userName }}</p>
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

      <!-- Admin Sections -->
      <div class="row g-4">
        <div class="col-md-6 col-lg-4">
          <div class="card admin-section-card h-100">
            <div class="card-body text-center">
              <div class="admin-icon bg-primary text-white rounded-circle mx-auto mb-3">
                <i class="bi bi-graph-up"></i>
              </div>
              <h5 class="card-title fw-bold">Analytics</h5>
              <p class="card-text text-muted">Métricas y estadísticas del sistema</p>
              <NuxtLink to="/admin/analytics" class="btn btn-primary">
                <i class="bi bi-arrow-right me-1"></i>Ver Analytics
              </NuxtLink>
            </div>
          </div>
        </div>

        <div class="col-md-6 col-lg-4">
          <div class="card admin-section-card h-100">
            <div class="card-body text-center">
              <div class="admin-icon bg-success text-white rounded-circle mx-auto mb-3">
                <i class="bi bi-people"></i>
              </div>
              <h5 class="card-title fw-bold">Gestión de Usuarios</h5>
              <p class="card-text text-muted">Administrar usuarios del sistema</p>
              <NuxtLink to="/admin/users" class="btn btn-success">
                <i class="bi bi-arrow-right me-1"></i>Gestionar Usuarios
              </NuxtLink>
            </div>
          </div>
        </div>

        <div class="col-md-6 col-lg-4">
          <div class="card admin-section-card h-100">
            <div class="card-body text-center">
              <div class="admin-icon bg-warning text-white rounded-circle mx-auto mb-3">
                <i class="bi bi-box"></i>
              </div>
              <h5 class="card-title fw-bold">Gestión de Productos</h5>
              <p class="card-text text-muted">Administrar catálogo de productos</p>
              <NuxtLink to="/admin/products" class="btn btn-warning">
                <i class="bi bi-arrow-right me-1"></i>Gestionar Productos
              </NuxtLink>
            </div>
          </div>
        </div>

        <div class="col-md-6 col-lg-4">
          <div class="card admin-section-card h-100">
            <div class="card-body text-center">
              <div class="admin-icon bg-info text-white rounded-circle mx-auto mb-3">
                <i class="bi bi-bag"></i>
              </div>
              <h5 class="card-title fw-bold">Historial de Pedidos</h5>
              <p class="card-text text-muted">Ver todos los pedidos del sistema</p>
              <NuxtLink to="/admin/orders" class="btn btn-info">
                <i class="bi bi-arrow-right me-1"></i>Ver Pedidos
              </NuxtLink>
            </div>
          </div>
        </div>

        <div class="col-md-6 col-lg-4">
          <div class="card admin-section-card h-100">
            <div class="card-body text-center">
              <div class="admin-icon bg-secondary text-white rounded-circle mx-auto mb-3">
                <i class="bi bi-chat-dots"></i>
              </div>
              <h5 class="card-title fw-bold">Historial de Chats</h5>
              <p class="card-text text-muted">Ver conversaciones con el chatbot</p>
              <NuxtLink to="/admin/chats" class="btn btn-secondary">
                <i class="bi bi-arrow-right me-1"></i>Ver Chats
              </NuxtLink>
            </div>
          </div>
        </div>

        <div class="col-md-6 col-lg-4">
          <div class="card admin-section-card h-100">
            <div class="card-body text-center">
              <div class="admin-icon bg-dark text-white rounded-circle mx-auto mb-3">
                <i class="bi bi-file-earmark-arrow-up"></i>
              </div>
              <h5 class="card-title fw-bold">Archivos RAG</h5>
              <p class="card-text text-muted">Subir archivos para el chatbot</p>
              <NuxtLink to="/admin/rag" class="btn btn-dark">
                <i class="bi bi-arrow-right me-1"></i>Gestionar Archivos
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Activity -->
      <div class="row mt-5">
        <div class="col-md-6">
          <div class="card">
            <div class="card-header">
              <h5 class="card-title mb-0">
                <i class="bi bi-clock-history me-2"></i>Actividad Reciente
              </h5>
            </div>
            <div class="card-body">
              <div v-if="loading" class="text-center py-3">
                <div class="spinner-border text-primary" role="status">
                  <span class="visually-hidden">Cargando...</span>
                </div>
              </div>
              <div v-else-if="error" class="alert alert-danger">
                {{ error }}
              </div>
              <div v-else-if="recentOrders.length === 0" class="text-muted text-center py-3">
                No hay actividad reciente
              </div>
              <div v-else>
                <div v-for="order in recentOrders" :key="order.id" class="d-flex align-items-center mb-3">
                  <div class="flex-shrink-0">
                    <i class="bi bi-bag text-primary"></i>
                  </div>
                  <div class="flex-grow-1 ms-3">
                    <div class="fw-semibold">Pedido #{{ order.id }}</div>
                    <div class="text-muted small">{{ order.fecha_creacion }}</div>
                  </div>
                  <div class="text-end">
                    <span class="badge bg-primary">Q {{ Number(order.total).toFixed(2) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="col-md-6">
          <div class="card">
            <div class="card-header">
              <h5 class="card-title mb-0">
                <i class="bi bi-chat-dots me-2"></i>Chats Recientes
              </h5>
            </div>
            <div class="card-body">
              <div v-if="loading" class="text-center py-3">
                <div class="spinner-border text-primary" role="status">
                  <span class="visually-hidden">Cargando...</span>
                </div>
              </div>
              <div v-else-if="error" class="alert alert-danger">
                {{ error }}
              </div>
              <div v-else-if="recentChats.length === 0" class="text-muted text-center py-3">
                No hay chats recientes
              </div>
              <div v-else>
                <div v-for="chat in recentChats" :key="chat.id" class="d-flex align-items-center mb-3">
                  <div class="flex-shrink-0">
                    <i class="bi bi-chat-dots text-info"></i>
                  </div>
                  <div class="flex-grow-1 ms-3">
                    <div class="fw-semibold">Usuario #{{ chat.usuario_id }}</div>
                    <div class="text-muted small">{{ chat.fecha_creacion }}</div>
                  </div>
                  <div class="text-end">
                    <span class="badge bg-info">{{ chat.mensajes_count }} mensajes</span>
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
    error.value = err.message || 'Error cargando datos'
  } finally {
    loading.value = false
  }
}

// Lifecycle
onMounted(() => {
  loadData()
})
</script>

<style scoped>
.admin-dashboard {
  min-height: 100vh;
  background-color: #f8f9fa;
  padding: 20px 0;
}

.kpi-card {
  transition: transform 0.2s ease-in-out;
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

.admin-section-card {
  transition: transform 0.2s ease-in-out;
  border: 1px solid #e9ecef;
}

.admin-section-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}

.admin-icon {
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
}
</style>
