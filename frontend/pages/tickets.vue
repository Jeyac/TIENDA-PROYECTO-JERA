<template>
  <div class="tickets-page">
    <div class="container-fluid">
      <!-- Header -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <h2 class="fw-bold mb-3">
                <i class="bi bi-ticket-perforated me-2"></i>Mis Tickets de soporte
              </h2>
              <p class="text-muted">Comunícate con nuestro equipo de atención al cliente</p>
            </div>
            <BaseButton variant="primary" @click="showCreateModal = true">
              <i class="bi bi-plus-circle me-2"></i>Crear nuevo ticket
            </BaseButton>
          </div>
        </div>
      </div>

      <!-- Stats Cards -->
      <div class="row mb-4">
        <div class="col-md-3">
          <div class="card bg-primary text-white">
            <div class="card-body">
              <div class="d-flex justify-content-between">
                <div>
                  <h3 class="mb-0">{{ stats.total }}</h3>
                  <p class="mb-0">Total Tickets</p>
                </div>
                <i class="bi bi-ticket-perforated display-4 opacity-50"></i>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card bg-warning text-white">
            <div class="card-body">
              <div class="d-flex justify-content-between">
                <div>
                  <h3 class="mb-0">{{ stats.abiertos }}</h3>
                  <p class="mb-0">Abiertos</p>
                </div>
                <i class="bi bi-clock display-4 opacity-50"></i>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card bg-info text-white">
            <div class="card-body">
              <div class="d-flex justify-content-between">
                <div>
                  <h3 class="mb-0">{{ stats.en_progreso }}</h3>
                  <p class="mb-0">En Progreso</p>
                </div>
                <i class="bi bi-gear display-4 opacity-50"></i>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card bg-success text-white">
            <div class="card-body">
              <div class="d-flex justify-content-between">
                <div>
                  <h3 class="mb-0">{{ stats.cerrados }}</h3>
                  <p class="mb-0">Resueltos</p>
                </div>
                <i class="bi bi-check-circle display-4 opacity-50"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Filters -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="card">
            <div class="card-body">
              <div class="row align-items-center">
                <div class="col-md-4">
                  <div class="input-group">
                    <input
                      v-model="searchQuery"
                      type="text"
                      class="form-control"
                      placeholder="Buscar tickets..."
                      @input="filterTickets"
                    >
                    <button class="btn btn-outline-secondary" type="button">
                      <i class="bi bi-search"></i>
                    </button>
                  </div>
                </div>
                <div class="col-md-3">
                  <select v-model="statusFilter" @change="filterTickets" class="form-select">
                    <option value="">Todos los estados</option>
                    <option value="abierto">Abierto</option>
                    <option value="en_progreso">En Progreso</option>
                    <option value="cerrado">Cerrado</option>
                    <option value="resuelto">Resuelto</option>
                  </select>
                </div>
                <div class="col-md-3">
                  <select v-model="priorityFilter" @change="filterTickets" class="form-select">
                    <option value="">Todas las prioridades</option>
                    <option value="baja">Baja</option>
                    <option value="media">Media</option>
                    <option value="alta">Alta</option>
                    <option value="urgente">Urgente</option>
                  </select>
                </div>
                <div class="col-md-2">
                  <button class="btn btn-outline-primary w-100" @click="loadTickets">
                    <i class="bi bi-arrow-clockwise"></i> Actualizar
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Tickets List -->
      <div class="card">
        <div class="card-header bg-white border-bottom">
          <h5 class="card-title mb-0">
            <i class="bi bi-list-ul me-2"></i>Mis Tickets
            <span class="badge bg-primary ms-2">{{ filteredTickets.length }}</span>
          </h5>
        </div>
        <div class="card-body p-0">
          <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Cargando...</span>
            </div>
            <p class="text-muted mt-3">Cargando tickets...</p>
          </div>
          
          <div v-else-if="filteredTickets.length === 0" class="text-center py-5">
            <i class="bi bi-ticket-perforated text-muted" style="font-size: 4rem;"></i>
            <h3 class="text-muted mt-3">No tienes tickets</h3>
            <p class="text-muted">Crea tu primer ticket para obtener soporte.</p>
          </div>
          
          <div v-else class="table-responsive">
            <table class="table table-hover mb-0">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Título</th>
                  <th>Estado</th>
                  <th>Prioridad</th>
                  <th>Asignado a</th>
                  <th>Creado</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="ticket in filteredTickets" :key="ticket.id" :class="getTicketRowClass(ticket)">
                  <td class="fw-bold">
                    #{{ ticket.id }}
                    <span v-if="hasUnreadMessages(ticket)" class="badge bg-danger ms-1" title="Nuevos mensajes">
                      <i class="bi bi-chat-dots-fill"></i>
                    </span>
                  </td>
                  <td>
                    <div>
                      <div class="fw-medium">{{ ticket.title }}</div>
                      <small class="text-muted">{{ ticket.description?.substring(0, 50) }}...</small>
                    </div>
                  </td>
                  <td>
                    <span class="badge" :class="getStatusBadgeClass(ticket.status)">
                      {{ getStatusText(ticket.status) }}
                    </span>
                  </td>
                  <td>
                    <span class="badge" :class="getPriorityBadgeClass(ticket.priority)">
                      {{ getPriorityText(ticket.priority) }}
                    </span>
                  </td>
                  <td>
                    <div v-if="ticket.assignee_name">
                      <div class="fw-medium">{{ ticket.assignee_name }}</div>
                      <small class="text-muted">Agente de soporte</small>
                    </div>
                    <span v-else class="text-muted">Sin asignar</span>
                  </td>
                  <td>{{ formatDate(ticket.created_at) }}</td>
                  <td>
                    <button @click="viewTicket(ticket)" class="btn btn-primary btn-sm" title="Ver detalles y chat">
                      <i class="bi bi-gear me-1"></i>Gestionar
                      <span v-if="hasUnreadMessages(ticket)" class="badge bg-danger ms-1">!</span>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        
        <!-- Pagination -->
        <div v-if="filteredTickets.length > itemsPerPage" class="card-footer">
          <Paginator 
            v-model="currentPage" 
            :total-items="filteredTickets.length" 
            :items-per-page="itemsPerPage"
          />
        </div>
      </div>
    </div>

    <!-- Create Ticket Modal -->
    <div class="modal fade" :class="{ show: showCreateModal }" :style="{ display: showCreateModal ? 'block' : 'none' }" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Crear Nuevo Ticket</h5>
            <button type="button" class="btn-close" @click="closeCreateModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="createTicket">
              <div class="row g-3">
                <div class="col-12">
                  <label class="form-label">Título *</label>
                  <input 
                    v-model="ticketForm.title" 
                    type="text" 
                    class="form-control" 
                    required 
                    maxlength="100"
                  />
                </div>
                <div class="col-md-6">
                  <label class="form-label">Prioridad *</label>
                  <select v-model="ticketForm.priority" class="form-select" required>
                    <option value="">Seleccionar prioridad</option>
                    <option value="baja">Baja</option>
                    <option value="media">Media</option>
                    <option value="alta">Alta</option>
                    <option value="urgente">Urgente</option>
                  </select>
                </div>
                <div class="col-md-6">
                  <label class="form-label">Categoría</label>
                  <select v-model="ticketForm.category" class="form-select">
                    <option value="">Seleccionar categoría</option>
                    <option value="tecnico">Técnico</option>
                    <option value="facturacion">Facturación</option>
                    <option value="general">General</option>
                    <option value="producto">Producto</option>
                  </select>
                </div>
                <div class="col-12">
                  <label class="form-label">Descripción *</label>
                  <textarea 
                    v-model="ticketForm.description" 
                    class="form-control" 
                    rows="4" 
                    required 
                    maxlength="1000"
                  ></textarea>
                </div>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <BaseButton variant="secondary" @click="closeCreateModal">Cancelar</BaseButton>
            <BaseButton variant="primary" @click="createTicket" :disabled="creating">
              <InlineSpinner v-if="creating" size="sm" class="me-2" />
              Crear Ticket
            </BaseButton>
          </div>
        </div>
      </div>
    </div>

    <!-- View Ticket Modal -->
    <div class="modal fade" :class="{ show: showViewModal }" :style="{ display: showViewModal ? 'block' : 'none' }" tabindex="-1">
      <div class="modal-dialog modal-xl">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Ticket #{{ selectedTicket?.id }} - {{ selectedTicket?.title }}</h5>
            <button type="button" class="btn-close" @click="closeViewModal"></button>
          </div>
          <div class="modal-body">
            <div v-if="selectedTicket" class="row">
              <div class="col-md-8">
                <div class="card">
                  <div class="card-header">
                    <h6 class="mb-0">Descripción</h6>
                  </div>
                  <div class="card-body">
                    <p>{{ selectedTicket.description }}</p>
                  </div>
                </div>


                <!-- Chat Section -->
                <div class="card mt-3">
                  <div class="card-header bg-success text-white">
                    <h6 class="mb-0"><i class="bi bi-chat-dots me-2"></i>Chat con Soporte</h6>
                  </div>
                  <div class="card-body">
                    <!-- Messages -->
                    <div class="chat-messages mb-3" style="height: 300px; overflow-y: auto; border: 1px solid #dee2e6; padding: 1rem; border-radius: 0.375rem;">
                      <div v-for="message in ticketMessages" :key="message.id" class="mb-3">
                        <div :class="message.user_rol === 'cliente' ? 'text-end' : 'text-start'">
                          <div :class="message.user_rol === 'cliente' ? 'bg-primary text-white' : 'bg-light'" 
                               class="d-inline-block p-2 rounded" style="max-width: 70%;">
                            <div class="fw-bold">{{ message.user_name }}</div>
                            <div>{{ message.description }}</div>
                            <small class="opacity-75">{{ formatDate(message.created_at) }}</small>
                          </div>
                        </div>
                      </div>
                      <div v-if="ticketMessages.length === 0" class="text-center text-muted">
                        <i class="bi bi-chat-dots display-4"></i>
                        <p>No hay mensajes aún. Inicia la conversación.</p>
                      </div>
                    </div>
                    
                    <!-- Message Input -->
                    <div v-if="selectedTicket?.status === 'cerrado' || selectedTicket?.status === 'resuelto'" class="form-text text-warning">
                      <i class="bi bi-exclamation-triangle me-1"></i>
                      Este ticket está {{ selectedTicket?.status === 'cerrado' ? 'cerrado' : 'resuelto' }}. No se pueden enviar más mensajes.
                    </div>
                    <div v-else class="input-group">
                      <input 
                        v-model="newMessage" 
                        type="text" 
                        class="form-control" 
                        placeholder="Escribe tu mensaje aquí..."
                        :disabled="sendingMessage"
                        @keyup.enter="addMessage"
                      >
                      <button 
                        @click="addMessage" 
                        class="btn btn-success" 
                        :disabled="sendingMessage || !newMessage.trim()"
                      >
                        <span v-if="sendingMessage" class="spinner-border spinner-border-sm me-1"></span>
                        <i v-else class="bi bi-send me-1"></i>
                        Enviar
                      </button>
                    </div>
                  </div>
                </div>
              </div>
              
              <div class="col-md-4">
                <div class="card">
                  <div class="card-header">
                    <h6 class="mb-0">Detalles del Ticket</h6>
                  </div>
                  <div class="card-body">
                    <div class="mb-3">
                      <strong>Estado:</strong>
                      <span class="badge ms-2" :class="getStatusBadgeClass(selectedTicket.status)">
                        {{ getStatusText(selectedTicket.status) }}
                      </span>
                    </div>
                    <div class="mb-3">
                      <strong>Prioridad:</strong>
                      <span class="badge ms-2" :class="getPriorityBadgeClass(selectedTicket.priority)">
                        {{ getPriorityText(selectedTicket.priority) }}
                      </span>
                    </div>
                    <div class="mb-3">
                      <strong>Categoría:</strong>
                      <span class="ms-2">{{ selectedTicket.category || 'Sin categoría' }}</span>
                    </div>
                    <div class="mb-3">
                      <strong>Fecha de creación:</strong>
                      <span class="ms-2">{{ formatDate(selectedTicket.created_at) }}</span>
                    </div>
                    <div class="mb-3">
                      <strong>Asignado a:</strong>
                      <span class="ms-2">{{ selectedTicket.assignee_name || 'Sin asignar' }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>


    <!-- Error Alert -->
    <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
      <i class="bi bi-exclamation-triangle me-2"></i>
      {{ error }}
      <button type="button" class="btn-close" @click="error = ''"></button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '~/stores/auth'

// Middleware
definePageMeta({
  middleware: ['user-only']
})

// Stores
const auth = useAuthStore()

// Reactive data
const tickets = ref<any[]>([])
const loading = ref(false)
const creating = ref(false)
const sendingMessage = ref(false)
const error = ref('')

// Stats
const stats = ref({
  total: 0,
  abiertos: 0,
  en_progreso: 0,
  cerrados: 0
})

// Form data
const ticketForm = ref({
  title: '',
  description: '',
  priority: '',
  category: ''
})

// Modal states
const showCreateModal = ref(false)
const showViewModal = ref(false)
const selectedTicket = ref<any>(null)
const ticketMessages = ref<any[]>([])
const newMessage = ref('')

// Filters and pagination
const searchQuery = ref('')
const statusFilter = ref('')
const priorityFilter = ref('')
const currentPage = ref(1)
const itemsPerPage = 10

// Computed properties
const filteredTickets = computed(() => {
  let filtered = tickets.value

  // Search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(t => 
      t.titulo.toLowerCase().includes(query) ||
      t.descripcion.toLowerCase().includes(query)
    )
  }

  // Status filter
  if (statusFilter.value) {
    filtered = filtered.filter(t => t.estado === statusFilter.value)
  }

  // Priority filter
  if (priorityFilter.value) {
    filtered = filtered.filter(t => t.prioridad === priorityFilter.value)
  }

  return filtered
})

const paginatedTickets = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredTickets.value.slice(start, end)
})

// Methods
const loadTickets = async () => {
  loading.value = true
  try {
    const response = await auth.makeAuthenticatedRequest('/api/tickets/my')
    if (response.ok) {
      tickets.value = await response.json()
      console.log('Tickets cargados:', tickets.value)
      
      // Cargar actividades para cada ticket para detectar mensajes nuevos
      for (const ticket of tickets.value) {
        if (!ticket.id) {
          console.warn('Ticket sin ID:', ticket)
          ticket.activities = []
          continue
        }
        
        try {
          const activitiesResponse = await auth.makeAuthenticatedRequest(`/api/tickets/${ticket.id}/activities`)
          if (activitiesResponse.ok) {
            ticket.activities = await activitiesResponse.json()
          }
        } catch (err) {
          console.error(`Error cargando actividades del ticket ${ticket.id}:`, err)
          ticket.activities = []
        }
      }
      
      calculateStats()
    } else {
      throw new Error('Error al cargar tickets')
    }
  } catch (err: any) {
    error.value = err.message || 'Error al cargar tickets'
  } finally {
    loading.value = false
  }
}

const calculateStats = () => {
  stats.value = {
    total: tickets.value.length,
    abiertos: tickets.value.filter(t => t.status === 'abierto').length,
    en_progreso: tickets.value.filter(t => t.status === 'en_progreso').length,
    cerrados: tickets.value.filter(t => t.status === 'cerrado' || t.status === 'resuelto').length
  }
}

const createTicket = async () => {
  if (creating.value) return // Evitar múltiples clics
  creating.value = true
  try {
    const response = await auth.makeAuthenticatedRequest('/api/tickets/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(ticketForm.value)
    })

    if (response.ok) {
      const newTicket = await response.json()
      tickets.value.unshift(newTicket)
      closeCreateModal()
    } else {
      const errorData = await response.json()
      throw new Error(errorData.error || 'Error al crear ticket')
    }
  } catch (err: any) {
    error.value = err.message || 'Error al crear ticket'
  } finally {
    creating.value = false
  }
}

const viewTicket = async (ticket: any) => {
  selectedTicket.value = ticket
  showViewModal.value = true
  
  // Load messages for this ticket
  if (!ticket.id) {
    console.error('Ticket sin ID:', ticket)
    ticketMessages.value = []
    return
  }
  
  try {
    const response = await auth.makeAuthenticatedRequest(`/api/tickets/${ticket.id}/activities`)
    if (response.ok) {
      const activities = await response.json()
      // Filtrar solo los mensajes (actividades de tipo 'message')
      ticketMessages.value = activities.filter((activity: any) => activity.activity_type === 'message')
    }
  } catch (err) {
    console.error('Error al cargar mensajes:', err)
    ticketMessages.value = []
  }
}

const addMessage = async () => {
  if (!selectedTicket.value || !newMessage.value.trim()) return
  
  if (!selectedTicket.value.id) {
    console.error('Ticket sin ID:', selectedTicket.value)
    error.value = 'Error: Ticket sin ID válido'
    return
  }

  sendingMessage.value = true
  try {
    const response = await auth.makeAuthenticatedRequest(`/api/tickets/${selectedTicket.value.id}/message`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        message: newMessage.value
      })
    })

    if (response.ok) {
      newMessage.value = ''
      // Recargar mensajes para obtener el mensaje recién enviado
      await viewTicket(selectedTicket.value)
    } else {
      const errorData = await response.json()
      throw new Error(errorData.error || 'Error al enviar mensaje')
    }
  } catch (err: any) {
    error.value = err.message || 'Error al enviar mensaje'
  } finally {
    sendingMessage.value = false
  }
}

const closeTicket = async (ticket: any) => {
  try {
    const response = await auth.makeAuthenticatedRequest(`/api/tickets/${ticket.id}/status`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        estado: 'cerrado'
      })
    })

    if (response.ok) {
      ticket.estado = 'cerrado'
    } else {
      const errorData = await response.json()
      throw new Error(errorData.error || 'Error al cerrar ticket')
    }
  } catch (err: any) {
    error.value = err.message || 'Error al cerrar ticket'
  }
}

const closeCreateModal = () => {
  showCreateModal.value = false
  ticketForm.value = {
    title: '',
    description: '',
    priority: '',
    category: ''
  }
}

const closeViewModal = () => {
  showViewModal.value = false
  selectedTicket.value = null
  ticketMessages.value = []
  newMessage.value = ''
}


const clearFilters = () => {
  searchQuery.value = ''
  statusFilter.value = ''
  priorityFilter.value = ''
  currentPage.value = 1
}

const getPriorityClass = (priority: string) => {
  const classes = {
    'baja': 'bg-success',
    'media': 'bg-warning',
    'alta': 'bg-danger',
    'urgente': 'bg-dark'
  }
  return classes[priority as keyof typeof classes] || 'bg-secondary'
}

const formatDate = (dateString: string) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const formatTime = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleTimeString('es-ES', { 
    hour: '2-digit', 
    minute: '2-digit' 
  })
}

// Utility functions
const getStatusBadgeClass = (status: string) => {
  const classes: { [key: string]: string } = {
    'abierto': 'bg-warning',
    'en_progreso': 'bg-info',
    'cerrado': 'bg-secondary',
    'resuelto': 'bg-success'
  }
  return classes[status] || 'bg-secondary'
}

const getStatusText = (status: string) => {
  const texts: { [key: string]: string } = {
    'abierto': 'Abierto',
    'en_progreso': 'En Progreso',
    'cerrado': 'Cerrado',
    'resuelto': 'Resuelto'
  }
  return texts[status] || status
}

const getPriorityBadgeClass = (priority: string) => {
  const classes: { [key: string]: string } = {
    'baja': 'bg-success',
    'media': 'bg-warning',
    'alta': 'bg-danger',
    'urgente': 'bg-dark'
  }
  return classes[priority] || 'bg-secondary'
}

const getPriorityText = (priority: string) => {
  const texts: { [key: string]: string } = {
    'baja': 'Baja',
    'media': 'Media',
    'alta': 'Alta',
    'urgente': 'Urgente'
  }
  return texts[priority] || priority
}

const getTicketRowClass = (ticket: any) => {
  if (ticket.status === 'cerrado' || ticket.status === 'resuelto') {
    return 'table-secondary'
  }
  if (hasUnreadMessages(ticket)) {
    return 'table-warning'
  }
  return ''
}

const hasUnreadMessages = (ticket: any) => {
  // No mostrar notificaciones en tickets cerrados o resueltos
  if (ticket.status === 'cerrado' || ticket.status === 'resuelto') return false
  
  if (!ticket.activities || ticket.activities.length === 0) return false
  
  // Obtener todos los mensajes ordenados por fecha
  const messages = ticket.activities
    .filter((activity: any) => activity.activity_type === 'message')
    .sort((a: any, b: any) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime())
  
  if (messages.length === 0) return false
  
  // Si el último mensaje es del agente (no del cliente), hay un mensaje no leído
  const lastMessage = messages[messages.length - 1]
  return lastMessage && lastMessage.user_rol !== 'cliente'
}

const filterTickets = () => {
  // La lógica de filtrado ya está en el computed filteredTickets
}

// Lifecycle
onMounted(async () => {
  if (auth.isAuthenticated) {
    await loadTickets()
  }
})
</script>

<style scoped>
.tickets-page {
  padding: 0;
}

.modal.show {
  background-color: rgba(0, 0, 0, 0.5);
}

/* Chat styles */
.chat-container {
  border-radius: 8px;
  overflow: hidden;
}

.chat-messages {
  scrollbar-width: thin;
  scrollbar-color: #ccc transparent;
}

.chat-messages::-webkit-scrollbar {
  width: 6px;
}

.chat-messages::-webkit-scrollbar-track {
  background: transparent;
}

.chat-messages::-webkit-scrollbar-thumb {
  background-color: #ccc;
  border-radius: 3px;
}

.message-bubble {
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.message-user .message-bubble {
  background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
}

.message-agent .message-bubble {
  background: #ffffff;
  border: 1px solid #e9ecef;
}

.table th {
  border-top: none;
  font-weight: 600;
  color: var(--bs-gray-700);
}

.table td {
  vertical-align: middle;
}

.btn-group-sm .btn {
  padding: 0.25rem 0.5rem;
}

.card {
  border-radius: 1rem;
  border: 1px solid var(--bs-border-color);
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
  margin-bottom: 1.5rem;
}

.form-control:focus,
.form-select:focus {
  border-color: var(--bs-primary);
  box-shadow: 0 0 0 0.2rem rgba(var(--bs-primary-rgb), 0.25);
}

.alert {
  border-radius: 0.75rem;
  border: none;
}

.badge {
  font-weight: 500;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .table-responsive {
    font-size: 0.875rem;
  }
  
  .btn-group-sm .btn {
    padding: 0.2rem 0.4rem;
  }
}
</style>
