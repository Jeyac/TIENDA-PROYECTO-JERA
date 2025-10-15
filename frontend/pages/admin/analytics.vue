<template>
  <div class="analytics-page">
    <div class="container-fluid">
      <!-- Header -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <h1 class="display-6 fw-bold mb-2">
                <i class="bi bi-graph-up me-2"></i>Analitica
              </h1>
              <p class="text-muted mb-0">Panel de control y métricas del sistema</p>
              <div v-if="kpisPending" class="text-primary small d-flex align-items-center mt-1">
                <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                Cargando KPIs...
              </div>
            </div>
            <div class="text-end">
              <small class="text-muted">Última actualización: {{ lastUpdate }}</small>
            </div>
          </div>
        </div>
      </div>

      <!-- KPIs Cards -->
      <div class="row g-4 mb-4">
        <KpiCard icon="bi bi-people" label="Total Usuarios" :value="kpis.usuarios_total || 0" color="primary" />
        <KpiCard icon="bi bi-box" label="Total Productos" :value="kpis.productos_total || 0" color="success" />
        <KpiCard icon="bi bi-currency-dollar" label="Ingresos Enviados/Entregados" :value="`Q${kpis.ingresos_total || 0}`" color="info" />
        <KpiCard icon="bi bi-chat-dots" label="Conversaciones" :value="conversationAnalytics.total_conversaciones || 0" color="warning" />
      </div>

      <!-- Chatbot Analytics -->
      <div class="row g-4 mb-4">
        <!-- Temas más preguntados -->
        <div class="col-lg-6">
          <div class="card" :class="$analyticsUi?.kpiCard || 'border-0 shadow-sm'">
            <div class="card-header bg-white border-bottom">
              <h5 class="card-title mb-0">
                <i class="bi bi-question-circle me-2"></i>Temas más preguntados
              </h5>
            </div>
            <div class="card-body">
              <div v-if="!conversationAnalytics.temas_mas_preguntados || conversationAnalytics.temas_mas_preguntados.length === 0" class="text-center py-4">
                <i class="bi bi-chat-quote text-muted" style="font-size: 2rem;"></i>
                <p class="text-muted mt-2">No hay datos de temas disponibles</p>
              </div>
              <div v-else class="list-group list-group-flush">
                <div v-for="(tema, index) in conversationAnalytics.temas_mas_preguntados" :key="index" class="list-group-item px-0 border-0">
                  <div class="d-flex justify-content-between align-items-center">
                    <div>
                      <h6 class="mb-1 text-capitalize">{{ tema.palabra }}</h6>
                    </div>
                    <div class="text-end">
                      <span class="badge bg-info">{{ tema.frecuencia }} veces</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Respuestas más frecuentes -->
        <div class="col-lg-6">
          <div class="card" :class="$analyticsUi?.kpiCard || 'border-0 shadow-sm'">
            <div class="card-header bg-white border-bottom">
              <h5 class="card-title mb-0">
                <i class="bi bi-chat-dots me-2"></i>Respuestas más frecuentes
              </h5>
            </div>
            <div class="card-body">
              <div v-if="!conversationAnalytics.respuestas_mas_frecuentes || conversationAnalytics.respuestas_mas_frecuentes.length === 0" class="text-center py-4">
                <i class="bi bi-robot text-muted" style="font-size: 2rem;"></i>
                <p class="text-muted mt-2">No hay datos de respuestas disponibles</p>
              </div>
              <div v-else class="list-group list-group-flush">
                <div v-for="(respuesta, index) in conversationAnalytics.respuestas_mas_frecuentes" :key="index" class="list-group-item px-0 border-0">
                  <div class="d-flex justify-content-between align-items-start">
                    <div class="flex-grow-1">
                      <p class="mb-1 small text-muted">{{ respuesta.respuesta.length > 80 ? respuesta.respuesta.substring(0, 80) + '...' : respuesta.respuesta }}</p>
                    </div>
                    <div class="text-end ms-2">
                      <span class="badge bg-success">{{ respuesta.frecuencia }} veces</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Activity -->
      <div class="row g-4">
        <div class="col-lg-12">
          <div class="card" :class="$analyticsUi?.kpiCard || 'border-0 shadow-sm'">
            <div class="card-header bg-white border-bottom">
              <h5 class="card-title mb-0">
                <i class="bi bi-clock-history me-2"></i>Pedidos recientes
              </h5>
              <InlineSpinner v-if="ordersPending">Cargando pedidos...</InlineSpinner>
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
                      <p class="text-muted mb-0 small">{{ formatDate(order.fecha_creacion) }}</p>
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
      </div>


      <!-- Loading State -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Cargando...</span>
        </div>
        <p class="text-muted mt-3">Cargando analiticas...</p>
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
  middleware: ['auth', 'admin'],
  layout: 'admin'
})

const config = useRuntimeConfig()
const auth = useAuthStore()

// Usar función global de formateo con timezone local
const { $formatDate: formatDate } = useNuxtApp()

// Data
const kpis = ref<any>({})
const recentOrders = ref<any[]>([])
const conversationAnalytics = ref<any>({})
const loading = ref(false)
const error = ref('')
const lastUpdate = ref('')

// Pending/Error flags for UI
const kpisPending = ref(false)
const ordersPending = ref(false)
const kpisErrMsg = ref('')
const ordersErrMsg = ref('')

// Methods
const loadData = async () => {
  loading.value = true
  error.value = ''
  
  try {
    // Load KPIs con $fetch
    const kpisUrl = `${config.public.apiBase}/api/admin/kpis`
    kpisPending.value = true
    kpisErrMsg.value = ''
    try {
      const data = await $fetch<any>(kpisUrl, { headers: { 'Authorization': `Bearer ${auth.token}` } })
      console.log('KPIs recibidos:', data)
      kpis.value = data
    } catch (e: any) {
      if (e?.statusCode === 401) { await auth.logout(); return }
      console.error('Error cargando KPIs:', e)
      kpisErrMsg.value = e?.message || 'Error al cargar KPIs'
    } finally {
      kpisPending.value = false
    }

    // Load recent orders con $fetch
    const ordersUrl = `${config.public.apiBase}/api/admin/pedidos`
    ordersPending.value = true
    ordersErrMsg.value = ''
    try {
      const data = await $fetch<any[]>(ordersUrl, { headers: { 'Authorization': `Bearer ${auth.token}` } })
      recentOrders.value = (data || []).slice(0, 5)
    } catch (e: any) {
      console.error('Error cargando pedidos:', e)
      ordersErrMsg.value = e?.message || 'Error al cargar pedidos'
    } finally {
      ordersPending.value = false
    }


    // Load conversation analytics
    try {
      console.log('🔍 FRONTEND: Cargando analytics de conversaciones...')
      const conversationUrl = `${config.public.apiBase}/api/analytics/conversations`
      console.log('🔍 FRONTEND: URL:', conversationUrl)
      
      const conversationData = await $fetch<any>(conversationUrl, { 
        headers: { 'Authorization': `Bearer ${auth.token}` } 
      })
      
      console.log('📊 FRONTEND: Datos recibidos:', conversationData)
      console.log('📊 FRONTEND: Temas más preguntados:', conversationData.temas_mas_preguntados)
      console.log('📊 FRONTEND: Total temas:', conversationData.temas_mas_preguntados?.length || 0)
      
      if (conversationData.temas_mas_preguntados && conversationData.temas_mas_preguntados.length > 0) {
        console.log('📊 FRONTEND: Estructura del primer tema:', conversationData.temas_mas_preguntados[0])
        console.log('📊 FRONTEND: Campos disponibles:', Object.keys(conversationData.temas_mas_preguntados[0]))
      }
      
      console.log('📊 FRONTEND: Respuestas más frecuentes:', conversationData.respuestas_mas_frecuentes)
      console.log('📊 FRONTEND: Total respuestas:', conversationData.respuestas_mas_frecuentes?.length || 0)
      
      if (conversationData.respuestas_mas_frecuentes && conversationData.respuestas_mas_frecuentes.length > 0) {
        console.log('📊 FRONTEND: Estructura de la primera respuesta:', conversationData.respuestas_mas_frecuentes[0])
        console.log('📊 FRONTEND: Campos disponibles en respuesta:', Object.keys(conversationData.respuestas_mas_frecuentes[0]))
      }
      
      conversationAnalytics.value = conversationData
      console.log('✅ FRONTEND: Analytics cargados correctamente')
    } catch (e: any) {
      console.error('❌ FRONTEND ERROR: Error cargando analítica de conversaciones:', e)
      console.error('❌ FRONTEND ERROR: Status:', e?.statusCode)
      console.error('❌ FRONTEND ERROR: Message:', e?.message)
      if (e?.statusCode === 401) {
        await auth.logout()
      }
    }

    lastUpdate.value = new Date().toLocaleString('es-ES', {
      timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone
    })
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



