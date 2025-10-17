<template>
  <div class="tickets-page">
    <div class="container-fluid">
      <!-- Header -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <h1 class="display-6 fw-bold mb-2">
                <i class="bi bi-ticket me-2"></i>Gestión de tickets
              </h1>
              <p class="text-muted mb-0">Administrar tickets de soporte y seguimiento</p>
            </div>
            <div class="d-flex gap-2">
              <select v-model="statusFilter" @change="loadTickets" class="form-select form-select-sm">
                <option value="">Todos los estados</option>
                <option value="abierto">Abiertos</option>
                <option value="en_progreso">En Progreso</option>
                <option value="cerrado">Cerrados</option>
                <option value="resuelto">Resueltos</option>
              </select>
              <button class="btn btn-primary btn-sm" @click="loadTickets">
                <i class="bi bi-arrow-clockwise me-1"></i>Actualizar
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Stats Cards -->
      <div class="row g-4 mb-4">
        <div class="col-md-3">
          <div class="card border-0 shadow-sm">
            <div class="card-body text-center">
              <i class="bi bi-ticket text-danger" style="font-size: 2rem;"></i>
              <h4 class="mt-2 mb-1">{{ stats.abiertos || 0 }}</h4>
              <small class="text-muted">Abiertos</small>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card border-0 shadow-sm">
            <div class="card-body text-center">
              <i class="bi bi-clock text-warning" style="font-size: 2rem;"></i>
              <h4 class="mt-2 mb-1">{{ stats.en_progreso || 0 }}</h4>
              <small class="text-muted">En progreso</small>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card border-0 shadow-sm">
            <div class="card-body text-center">
              <i class="bi bi-check-circle text-success" style="font-size: 2rem;"></i>
              <h4 class="mt-2 mb-1">{{ stats.resueltos || 0 }}</h4>
              <small class="text-muted">Resueltos</small>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card border-0 shadow-sm">
            <div class="card-body text-center">
              <i class="bi bi-exclamation-triangle text-danger" style="font-size: 2rem;"></i>
              <h4 class="mt-2 mb-1">{{ stats.urgentes || 0 }}</h4>
              <small class="text-muted">Urgentes</small>
            </div>
          </div>
        </div>
      </div>

      <!-- Tickets Table -->
      <div class="card border-0 shadow-sm">
        <div class="card-header bg-white border-bottom">
          <h5 class="card-title mb-0">
            <i class="bi bi-list-ul me-2"></i>Lista de tickets
          </h5>
        </div>
        <div class="card-body p-0">
          <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Cargando...</span>
            </div>
            <p class="text-muted mt-3">Cargando tickets...</p>
          </div>
          
          <div v-else-if="tickets.length === 0" class="text-center py-5">
            <i class="bi bi-ticket text-muted" style="font-size: 3rem;"></i>
            <p class="text-muted mt-2">No hay tickets disponibles</p>
          </div>
          
          <div v-else class="table-responsive">
            <table class="table table-hover mb-0">
              <thead class="table-light">
                <tr>
                  <th>ID</th>
                  <th>Título</th>
                  <th>Usuario</th>
                  <th>Estado</th>
                  <th>Prioridad</th>
                  <th>Categoría</th>
                  <th>Asignado</th>
                  <th>Fecha</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="ticket in tickets" :key="ticket.id" :class="getTicketRowClass(ticket)">
                  <td>
                    <span class="badge bg-secondary">#{{ ticket.id }}</span>
                  </td>
                  <td>
                    <div class="fw-medium">{{ ticket.title }}</div>
                    <small class="text-muted">{{ ticket.description?.substring(0, 50) }}{{ ticket.description?.length > 50 ? '...' : '' }}</small>
                  </td>
                  <td>
                    <div>{{ ticket.user_name || 'Usuario anónimo' }}</div>
                    <small class="text-muted">ID: {{ ticket.user_id }}</small>
                  </td>
                  <td>
                    <span :class="getStatusBadgeClass(ticket.status)">
                      {{ getStatusText(ticket.status) }}
                    </span>
                  </td>
                  <td>
                    <span :class="getPriorityBadgeClass(ticket.priority)">
                      {{ getPriorityText(ticket.priority) }}
                    </span>
                  </td>
                  <td>
                    <span class="badge bg-info">{{ ticket.category || 'General' }}</span>
                  </td>
                  <td>
                    <span v-if="ticket.assignee_name" class="badge bg-primary">
                      {{ ticket.assignee_name }}
                    </span>
                    <span v-else class="badge bg-warning text-dark">
                      <i class="bi bi-exclamation-triangle me-1"></i>Sin asignar
                    </span>
                  </td>
                  <td>
                    <div>{{ formatDate(ticket.created_at) }}</div>
                    <small class="text-muted">{{ formatTime(ticket.created_at) }}</small>
                  </td>
                  <td>
                    <div class="btn-group btn-group-sm">
                      <button class="btn btn-outline-primary" @click="viewTicket(ticket)">
                        <i class="bi bi-eye"></i>
                      </button>
                      <button class="btn btn-outline-success" @click="assignTicket(ticket)">
                        <i class="bi bi-person-plus"></i>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- Ticket Details Modal -->
    <div v-if="selectedTicket" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="bi bi-ticket me-2"></i>Ticket #{{ selectedTicket.id }}
            </h5>
            <button type="button" class="btn-close" @click="selectedTicket = null"></button>
          </div>
          <div class="modal-body">
            <div class="row g-3">
              <div class="col-md-6">
                <label class="form-label fw-bold">Título:</label>
                <p>{{ selectedTicket.title }}</p>
              </div>
              <div class="col-md-6">
                <label class="form-label fw-bold">Estado:</label>
                <div>
                  <span :class="getStatusBadgeClass(selectedTicket.status)">
                    {{ getStatusText(selectedTicket.status) }}
                  </span>
                </div>
              </div>
              <div class="col-md-6">
                <label class="form-label fw-bold">Prioridad:</label>
                <div>
                  <span :class="getPriorityBadgeClass(selectedTicket.priority)">
                    {{ getPriorityText(selectedTicket.priority) }}
                  </span>
                </div>
              </div>
              <div class="col-md-6">
                <label class="form-label fw-bold">Categoría:</label>
                <p>{{ selectedTicket.category || 'General' }}</p>
              </div>
              <div class="col-12">
                <label class="form-label fw-bold">Descripción:</label>
                <p class="border p-3 rounded bg-light">{{ selectedTicket.description || 'Sin descripción' }}</p>
              </div>
              <div class="col-12" v-if="selectedTicket.resolution">
                <label class="form-label fw-bold">Resolución:</label>
                <p class="border p-3 rounded bg-light">{{ selectedTicket.resolution }}</p>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="selectedTicket = null">Cerrar</button>
            <button type="button" class="btn btn-success" @click="assignTicket(selectedTicket)">
              <i class="bi bi-person-plus me-1"></i>Asignar
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Assign Ticket Modal -->
    <div v-if="assigningTicket" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="bi bi-person-plus me-2"></i>Asignar Ticket #{{ assigningTicket.id }}
            </h5>
            <button type="button" class="btn-close" @click="assigningTicket = null"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label fw-bold">Ticket:</label>
              <p>{{ assigningTicket.title }}</p>
            </div>
            <div class="mb-3">
              <label class="form-label fw-bold">Cliente:</label>
              <p>{{ assigningTicket.user_name || 'Usuario anónimo' }}</p>
            </div>
            <div class="mb-3">
              <label class="form-label fw-bold">Asignar a:</label>
              <select v-model="assignForm.assignee_id" class="form-select" :disabled="atencionUsers.length === 0">
                <option value="">
                  {{ atencionUsers.length === 0 ? 'Cargando usuarios...' : 'Seleccionar usuario de atención al cliente...' }}
                </option>
                <option v-for="user in atencionUsers" :key="user.id" :value="user.id">
                  {{ user.username }} ({{ user.email }})
                </option>
              </select>
              <div v-if="atencionUsers.length === 0" class="form-text text-muted">
                <i class="bi bi-hourglass-split me-1"></i>Cargando usuarios de atención al cliente...
              </div>
            </div>
            <div v-if="assignForm.assignee_id" class="alert alert-info">
              <i class="bi bi-info-circle me-2"></i>
              El ticket será asignado y el usuario de atención al cliente podrá darle seguimiento.
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="assigningTicket = null">Cancelar</button>
            <button type="button" class="btn btn-success" @click="saveAssignment" :disabled="!assignForm.assignee_id || assigning">
              <span v-if="assigning" class="spinner-border spinner-border-sm me-2"></span>
              {{ assigning ? 'Asignando...' : 'Asignar' }}
            </button>
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
  middleware: ['auth', 'admin'],
  layout: 'admin'
})

const config = useRuntimeConfig()
const auth = useAuthStore()

// Data
const tickets = ref<any[]>([])
const selectedTicket = ref<any>(null)
const assigningTicket = ref<any>(null)
const atencionUsers = ref<any[]>([])
const loading = ref(false)
const assigning = ref(false)
const statusFilter = ref('')

const stats = ref({
  abiertos: 0,
  en_progreso: 0,
  resueltos: 0,
  urgentes: 0
})

const assignForm = ref({
  assignee_id: ''
})

// Methods
const loadTickets = async () => {
  loading.value = true
  try {
    const { apiRequest } = useApi()
    const params = statusFilter.value ? `?status=${statusFilter.value}` : ''
    const response = await apiRequest(`/api/tickets/${params}`)
    
    if (response.ok) {
      tickets.value = await response.json()
      calculateStats()
    }
  } catch (error) {
    console.error('Error cargando tickets:', error)
  } finally {
    loading.value = false
  }
}

const calculateStats = () => {
  stats.value = {
    abiertos: tickets.value.filter(t => t.status === 'abierto').length,
    en_progreso: tickets.value.filter(t => t.status === 'en_progreso').length,
    resueltos: tickets.value.filter(t => t.status === 'resuelto').length,
    urgentes: tickets.value.filter(t => t.priority === 'urgente').length
  }
}

const viewTicket = (ticket: { id: number }) => {
  selectedTicket.value = ticket
}

const assignTicket = (ticket: any) => {
  assigningTicket.value = ticket
  assignForm.value = {
    assignee_id: ticket.assigned_to || ''
  }
  selectedTicket.value = null
}

const loadAtencionUsers = async () => {
  try {
    console.log('Cargando usuarios de atención al cliente...')
    const response = await auth.makeAuthenticatedRequest(
      `${config.public.apiBase}/api/admin/usuarios/atencion`
    )
    
    console.log('Response status:', response.status)
    
    if (response.ok) {
      const data = await response.json()
      console.log('Usuarios cargados:', data)
      atencionUsers.value = data
    } else {
      const errorText = await response.text()
      console.error('Error response:', response.status, errorText)
    }
  } catch (error) {
    console.error('Error cargando usuarios de atención:', error)
  }
}

const saveAssignment = async () => {
  if (!assigningTicket.value || !assignForm.value.assignee_id) return
  
  assigning.value = true
  try {
    const response = await auth.makeAuthenticatedRequest(
      `${config.public.apiBase}/api/tickets/${assigningTicket.value.id}/assign`,
      {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ assignee_id: parseInt(assignForm.value.assignee_id) })
      }
    )
    
    if (response.ok) {
      await loadTickets()
      assigningTicket.value = null
      assignForm.value.assignee_id = ''
    } else {
      const error = await response.json()
      console.error('Error asignando ticket:', error)
      alert(error.error || 'Error al asignar ticket')
    }
  } catch (error) {
    console.error('Error asignando ticket:', error)
    alert('Error al asignar ticket')
  } finally {
    assigning.value = false
  }
}

const getStatusBadgeClass = (status: string) => {
  const classes = {
    'abierto': 'badge bg-danger',
    'en_progreso': 'badge bg-warning',
    'cerrado': 'badge bg-secondary',
    'resuelto': 'badge bg-success'
  }
  return classes[status as keyof typeof classes] || 'badge bg-secondary'
}

const getStatusText = (status: string) => {
  const texts = {
    'abierto': 'Abierto',
    'en_progreso': 'En Progreso',
    'cerrado': 'Cerrado',
    'resuelto': 'Resuelto'
  }
  return texts[status as keyof typeof texts] || status
}

const getTicketRowClass = (ticket: any) => {
  // Iluminar tickets sin asignar
  if (!ticket.assignee_name) {
    return 'table-warning border-warning border-3'
  }
  return ''
}

const getPriorityBadgeClass = (priority: string) => {
  const classes = {
    'baja': 'badge bg-success',
    'media': 'badge bg-info',
    'alta': 'badge bg-warning',
    'urgente': 'badge bg-danger'
  }
  return classes[priority as keyof typeof classes] || 'badge bg-secondary'
}

const getPriorityText = (priority: string) => {
  const texts = {
    'baja': 'Baja',
    'media': 'Media',
    'alta': 'Alta',
    'urgente': 'Urgente'
  }
  return texts[priority as keyof typeof texts] || priority
}

// Usar funciones globales de formateo
const { $formatDate: formatDate, $formatTime: formatTime } = useNuxtApp()

// Lifecycle
onMounted(() => {
  if (auth.isAuthenticated && auth.isAdmin) {
    loadTickets()
    loadAtencionUsers()
  }
})
</script>

<style scoped>
.tickets-page {
  padding: 2rem 0;
}

.table th {
  border-top: none;
  font-weight: 600;
  color: var(--bs-gray-700);
}

.badge {
  font-size: 0.75rem;
}

.modal {
  z-index: 1055;
}

/* Resaltado para tickets sin asignar */
.table-warning {
  background-color: rgba(255, 193, 7, 0.1) !important;
  border-left: 4px solid #ffc107 !important;
}

.table-warning:hover {
  background-color: rgba(255, 193, 7, 0.2) !important;
}
</style>
