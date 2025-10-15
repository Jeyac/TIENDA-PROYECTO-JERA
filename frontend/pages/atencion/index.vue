<template>
  <div class="atencion-dashboard">
    <div class="row">
      <div class="col-12">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <div>
            <h2 class="fw-bold mb-1">Panel de Atención al Cliente</h2>
            <p class="text-muted mb-0">Gestiona tickets y chats de soporte</p>
          </div>
          <div class="d-flex gap-2">
            <BaseButton variant="primary" @click="navigateTo('/atencion/tickets')">
              <i class="bi bi-ticket me-2"></i>Ver Tickets
            </BaseButton>
            <BaseButton variant="success" @click="navigateTo('/atencion/chats')">
              <i class="bi bi-chat-dots me-2"></i>Chats en Vivo
            </BaseButton>
          </div>
        </div>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="row g-4 mb-4">
      <div class="col-md-4">
        <div class="card border-0 shadow-sm">
          <div class="card-body text-center">
            <div class="bg-primary bg-opacity-10 rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style="width: 60px; height: 60px;">
              <i class="bi bi-ticket text-primary" style="font-size: 1.5rem;"></i>
            </div>
            <h4 class="fw-bold text-primary">{{ stats.ticketsPendientes }}</h4>
            <p class="text-muted mb-0">Tickets Pendientes</p>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card border-0 shadow-sm">
          <div class="card-body text-center">
            <div class="bg-success bg-opacity-10 rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style="width: 60px; height: 60px;">
              <i class="bi bi-chat-dots text-success" style="font-size: 1.5rem;"></i>
            </div>
            <h4 class="fw-bold text-success">{{ stats.chatsActivos }}</h4>
            <p class="text-muted mb-0">Chats Activos</p>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card border-0 shadow-sm">
          <div class="card-body text-center">
            <div class="bg-warning bg-opacity-10 rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style="width: 60px; height: 60px;">
              <i class="bi bi-clock text-warning" style="font-size: 1.5rem;"></i>
            </div>
            <h4 class="fw-bold text-warning">{{ stats.tiempoPromedio }}min</h4>
            <p class="text-muted mb-0">Tiempo Promedio</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="row">
      <div class="col-12">
        <div class="card border-0 shadow-sm">
          <div class="card-header bg-white border-0 pb-0">
            <h5 class="fw-bold mb-0">Acciones Rápidas</h5>
          </div>
          <div class="card-body">
            <div class="row g-3">
              <div class="col-md-6">
                <div class="d-flex align-items-center p-3 border rounded">
                  <div class="bg-primary bg-opacity-10 rounded-circle d-flex align-items-center justify-content-center me-3" style="width: 50px; height: 50px;">
                    <i class="bi bi-ticket text-primary"></i>
                  </div>
                  <div class="flex-grow-1">
                    <h6 class="fw-bold mb-1">Gestionar Tickets</h6>
                    <p class="text-muted small mb-0">Revisar y responder tickets de soporte</p>
                  </div>
                  <BaseButton variant="outline-primary" size="sm" @click="navigateTo('/atencion/tickets')">
                    Ir
                  </BaseButton>
                </div>
              </div>
              <div class="col-md-6">
                <div class="d-flex align-items-center p-3 border rounded">
                  <div class="bg-success bg-opacity-10 rounded-circle d-flex align-items-center justify-content-center me-3" style="width: 50px; height: 50px;">
                    <i class="bi bi-chat-dots text-success"></i>
                  </div>
                  <div class="flex-grow-1">
                    <h6 class="fw-bold mb-1">Chats en Vivo</h6>
                    <p class="text-muted small mb-0">Atender conversaciones en tiempo real</p>
                  </div>
                  <BaseButton variant="outline-success" size="sm" @click="navigateTo('/atencion/chats')">
                    Ir
                  </BaseButton>
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
import { useAuthStore } from '~/stores/auth'

// Middleware
definePageMeta({
  middleware: ['auth', 'atencion'],
  layout: 'admin'
})

// Stores
const auth = useAuthStore()

// Stats data
const stats = ref({
  ticketsPendientes: 0,
  chatsActivos: 0,
  tiempoPromedio: 0
})

// Load stats
const loadStats = async () => {
  try {
    // Aquí cargarías las estadísticas reales desde la API
    // Por ahora usamos datos de ejemplo
    stats.value = {
      ticketsPendientes: 12,
      chatsActivos: 3,
      tiempoPromedio: 8
    }
  } catch (error) {
    console.error('Error cargando estadísticas:', error)
  }
}

onMounted(() => {
  loadStats()
})
</script>

<style scoped>
.atencion-dashboard {
  padding: 0;
}

.card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1) !important;
}

.bg-opacity-10 {
  background-color: rgba(var(--bs-primary-rgb), 0.1) !important;
}
</style>







