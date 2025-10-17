<template>
  <div class="atencion-tickets-page">
    <div class="container-fluid">
      <!-- Header -->
      <div class="row mb-4">
        <div class="col-12">
          <h2 class="fw-bold mb-3">
            <i class="bi bi-ticket-perforated me-2"></i>Tickets Asignados
          </h2>
          <p class="text-muted">Gestiona los tickets que te han sido asignados</p>
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
                  <p class="mb-0">Total Asignados</p>
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
                  <p class="mb-0">Cerrados</p>
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
                  <select v-model="statusFilter" @change="loadTickets" class="form-select">
                    <option value="">Todos los estados</option>
                    <option value="abierto">Abierto</option>
                    <option value="en_progreso">En Progreso</option>
                    <option value="cerrado">Cerrado</option>
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
                    <span v-if="hasAnyUnreadMessages" class="badge bg-danger ms-1 animate-pulse">
                      {{ unreadCount }}
                    </span>
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
            <i class="bi bi-list-ul me-2"></i>Tickets
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
            <h3 class="text-muted mt-3">No hay tickets asignados</h3>
            <p class="text-muted">Los tickets aparecerán aquí cuando sean asignados.</p>
          </div>
          
          <div v-else class="table-responsive">
            <table class="table table-hover mb-0">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Cliente</th>
                  <th>Título</th>
                  <th>Estado</th>
                  <th>Prioridad</th>
                  <th>Categoría</th>
                  <th>Creado</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="ticket in filteredTickets" :key="ticket.id" :class="getTicketRowClass(ticket)">
                  <td class="fw-bold">
                    #{{ ticket.id }}
                    <span v-if="hasUnreadMessages(ticket)" class="badge bg-danger ms-1 animate-pulse" title="Nuevos mensajes">
                      <i class="bi bi-chat-dots-fill"></i>
                    </span>
                  </td>
                  <td>
                    <div>
                      <div class="fw-medium">{{ ticket.user_name }}</div>
                      <small class="text-muted">{{ ticket.user_email }}</small>
                    </div>
                  </td>
                  <td>
                    {{ ticket.title }}
                    <span v-if="hasUnreadMessages(ticket)" class="badge bg-warning ms-1 animate-pulse">Nuevo</span>
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
                  <td>{{ getCategoryText(ticket.category) }}</td>
                  <td>{{ formatDate(ticket.created_at) }}</td>
                  <td>
                    <button @click="viewTicket(ticket)" class="btn btn-sm btn-primary">
                      <i class="bi bi-gear me-1"></i>Gestionar
                      <span v-if="hasUnreadMessages(ticket)" class="badge bg-danger ms-1 animate-pulse">!</span>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Ticket Details Modal -->
      <div class="modal fade" :class="{ show: showDetailsModal }" :style="{ display: showDetailsModal ? 'block' : 'none' }" tabindex="-1">
        <div class="modal-dialog modal-xl">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">
                <i class="bi bi-ticket-perforated me-2"></i>Ticket #{{ selectedTicket?.id }}
              </h5>
              <button type="button" class="btn-close" @click="showDetailsModal = false"></button>
            </div>
            <div class="modal-body">
              <div v-if="selectedTicket">
                <div class="row mb-4">
                  <div class="col-md-8">
                    <h4>{{ selectedTicket.title }}</h4>
                    <p class="text-muted">{{ selectedTicket.description }}</p>
                    
                    <div class="mt-3">
                      <strong>Cliente:</strong>
                      <div class="mt-2">
                        <i class="bi bi-person me-2"></i>{{ selectedTicket.user_name }}
                        <br>
                        <i class="bi bi-envelope me-2"></i>{{ selectedTicket.user_email }}
                      </div>
                    </div>
                  </div>
                  <div class="col-md-4">
                    <div class="card">
                      <div class="card-body">
                        <h6>Información</h6>
                        <p class="mb-1"><strong>Estado:</strong>
                          <span class="badge" :class="getStatusBadgeClass(selectedTicket.status)">
                            {{ getStatusText(selectedTicket.status) }}
                          </span>
                        </p>
                        <p class="mb-1"><strong>Prioridad:</strong>
                          <span class="badge" :class="getPriorityBadgeClass(selectedTicket.priority)">
                            {{ getPriorityText(selectedTicket.priority) }}
                          </span>
                        </p>
                        <p class="mb-1"><strong>Categoría:</strong> {{ getCategoryText(selectedTicket.category) }}</p>
                        <p class="mb-1"><strong>Creado:</strong> {{ formatDate(selectedTicket.created_at) }}</p>
                        <p class="mb-0"><strong>Actualizado:</strong> {{ formatDate(selectedTicket.updated_at) }}</p>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Update Form -->
                <div class="card mb-3">
                  <div class="card-header bg-primary text-white">
                    <h6 class="mb-0"><i class="bi bi-pencil me-2"></i>Actualizar Ticket</h6>
                  </div>
                  <div class="card-body">
                    <div class="row">
                      <div class="col-md-6 mb-3">
                        <label class="form-label">Estado</label>
                        <select v-model="updateForm.status" class="form-select">
                          <option value="abierto">Abierto</option>
                          <option value="en_progreso">En Progreso</option>
                          <option value="resuelto">Resuelto</option>
                          <option value="cerrado">Cerrado</option>
                        </select>
                      </div>
                      <div class="col-12">
                        <button @click="updateTicket" class="btn btn-primary" :disabled="updating">
                          <span v-if="updating" class="spinner-border spinner-border-sm me-2"></span>
                          <i v-else class="bi bi-check-circle me-2"></i>
                          {{ updating ? 'Guardando...' : 'Guardar Cambios' }}
                        </button>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Chat Section -->
                <div class="card mb-3">
                  <div class="card-header bg-success text-white">
                    <h6 class="mb-0"><i class="bi bi-chat-dots me-2"></i>Chat con el Cliente</h6>
                  </div>
                  <div class="card-body">
                    <!-- Messages -->
                    <div class="chat-messages mb-3" style="height: 300px; overflow-y: auto; border: 1px solid #dee2e6; padding: 1rem; border-radius: 0.375rem;">
                      <div v-for="activity in selectedTicket.activities?.filter((a: any) => a.activity_type === 'message')" :key="activity.id" class="mb-3">
                        <div :class="activity.user_id === auth.user?.id ? 'text-end' : 'text-start'">
                          <div :class="activity.user_id === auth.user?.id ? 'bg-primary text-white' : 'bg-light'" 
                               class="d-inline-block p-2 rounded" style="max-width: 70%;">
                            <div class="fw-bold">{{ activity.user_name }}</div>
                            <div>{{ activity.description }}</div>
                            <small class="opacity-75">{{ formatDate(activity.created_at) }}</small>
                          </div>
                        </div>
                      </div>
                      <div v-if="!selectedTicket.activities?.filter((a: any) => a.activity_type === 'message').length" class="text-center text-muted">
                        <i class="bi bi-chat-dots display-4"></i>
                        <p>No hay mensajes aún. Inicia la conversación.</p>
                      </div>
                    </div>
                    
                        <!-- Message Input -->
                        <div class="input-group">
                          <input 
                            v-model="newMessage" 
                            type="text" 
                            class="form-control" 
                            :placeholder="getChatPlaceholder()" 
                            :disabled="isChatDisabled()"
                            @keyup.enter="sendMessage"
                          >
                          <button 
                            @click="sendMessage" 
                            class="btn btn-success" 
                            :disabled="isChatDisabled() || !newMessage.trim() || sendingMessage"
                          >
                            <span v-if="sendingMessage" class="spinner-border spinner-border-sm me-1"></span>
                            <i v-else class="bi bi-send me-1"></i>
                            Enviar
                          </button>
                        </div>
                        <div v-if="isChatDisabled()" class="form-text text-warning">
                          <i class="bi bi-exclamation-triangle me-1"></i>
                          {{ getChatDisabledMessage() }}
                        </div>
                  </div>
                </div>

                <!-- Activities -->
                <div class="card">
                  <div class="card-header">
                    <h6 class="mb-0"><i class="bi bi-clock-history me-2"></i>Historial Completo</h6>
                  </div>
                  <div class="card-body">
                    <div class="timeline">
                      <div v-for="activity in selectedTicket.activities" :key="activity.id" class="timeline-item">
                        <div class="timeline-marker"></div>
                        <div class="timeline-content">
                          <h6>{{ getActivityTypeText(activity.activity_type) }}</h6>
                          <p class="text-muted">{{ activity.description }}</p>
                          <small class="text-muted">
                            {{ formatDate(activity.created_at) }}
                            <span v-if="activity.user_name"> - {{ activity.user_name }}</span>
                          </small>
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
      <div v-if="showDetailsModal" class="modal-backdrop fade show"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRuntimeConfig } from 'nuxt/app'
import { useAuthStore } from '~/stores/auth'

definePageMeta({
  middleware: ['auth', 'atencion'],
  layout: 'atencion'
})

const config = useRuntimeConfig()
const auth = useAuthStore()

// Data
const tickets = ref<any[]>([])
const loading = ref(false)
const updating = ref(false)
const showDetailsModal = ref(false)
const selectedTicket = ref<any>(null)

// Filters
const searchQuery = ref('')
const statusFilter = ref('')
const priorityFilter = ref('')

// Update form
const updateForm = reactive({
  status: ''
})

// Chat
const newMessage = ref('')
const sendingMessage = ref(false)

// Stats
const stats = computed(() => {
  const total = tickets.value.length
  const abiertos = tickets.value.filter(t => t.status === 'abierto').length
  const en_progreso = tickets.value.filter(t => t.status === 'en_progreso').length
  const cerrados = tickets.value.filter(t => t.status === 'cerrado').length
  return { total, abiertos, en_progreso, cerrados }
})

// Filtered tickets
const filteredTickets = computed(() => {
  let filtered = tickets.value
  
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(ticket => 
      ticket.title.toLowerCase().includes(query) ||
      ticket.description.toLowerCase().includes(query) ||
      ticket.user_name.toLowerCase().includes(query)
    )
  }
  
  if (priorityFilter.value) {
    filtered = filtered.filter(ticket => ticket.priority === priorityFilter.value)
  }
  
  return filtered.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
})

// Contar mensajes no leídos
const unreadCount = computed(() => {
  return tickets.value.filter(ticket => hasUnreadMessages(ticket)).length
})

const hasAnyUnreadMessages = computed(() => {
  return unreadCount.value > 0
})

// Methods
const loadTickets = async () => {
  loading.value = true
  
  try {
    const url = statusFilter.value 
      ? `${config.public.apiBase}/api/tickets/assigned?status=${statusFilter.value}`
      : `${config.public.apiBase}/api/tickets/assigned`
      
    const res = await fetch(url, {
      headers: {
        'Authorization': `Bearer ${auth.token}`
      }
    })
    
    if (res.ok) {
      tickets.value = await res.json()
    } else if (res.status === 401) {
      await auth.logout()
    }
  } catch (err) {
    console.error('Error cargando tickets:', err)
  } finally {
    loading.value = false
  }
}

const viewTicket = async (ticket: { id: number }) => {
  console.log('📥 ATENCION CHAT: Cargando ticket:', ticket.id)
  
  try {
    // Cargar detalles
    const resTicket = await fetch(`${config.public.apiBase}/api/tickets/${ticket.id}`, {
      headers: {
        'Authorization': `Bearer ${auth.token}`
      }
    })
    
    if (!resTicket.ok) {
      if (resTicket.status === 401) await auth.logout()
      return
    }
    
    const ticketData = await resTicket.json()
    console.log('📥 ATENCION CHAT: Datos del ticket cargados')
    
    // Cargar actividades
    const resActivities = await fetch(`${config.public.apiBase}/api/tickets/${ticket.id}/activities`, {
      headers: {
        'Authorization': `Bearer ${auth.token}`
      }
    })
    
    console.log('📥 ATENCION CHAT: Respuesta actividades:', resActivities.status, resActivities.ok)
    
    if (resActivities.ok) {
      const activities = await resActivities.json()
      console.log('📥 ATENCION CHAT: Actividades recibidas:', activities.length)
      console.log('📥 ATENCION CHAT: Actividades:', activities)
      
      // Mostrar la estructura de cada actividad
      activities.forEach((activity: any, index: number) => {
        console.log(`📥 ATENCION CHAT: Actividad ${index}:`, {
          id: activity.id,
          activity_type: activity.activity_type,
          description: activity.description,
          user_name: activity.user_name,
          user_rol: activity.user_rol,
          created_at: activity.created_at
        })
      })
      
      const messages = activities.filter((activity: any) => activity.activity_type === 'message')
      console.log('📥 ATENCION CHAT: Mensajes filtrados:', messages.length)
      console.log('📥 ATENCION CHAT: Mensajes:', messages)
      
      ticketData.activities = activities
    } else {
      ticketData.activities = []
    }
    
    selectedTicket.value = ticketData
    console.log('📥 ATENCION CHAT: Ticket asignado con', selectedTicket.value.activities?.length || 0, 'actividades')
    updateForm.status = ticketData.status
    showDetailsModal.value = true
    
    // Solo marcar como visto si había mensajes no leídos
    if (hasUnreadMessages(ticketData)) {
      markTicketAsViewed(ticket.id)
    }
    
    // Hacer scroll al final del chat
    setTimeout(() => {
      scrollToBottom()
    }, 100)
    
  } catch (err) {
    console.error('Error:', err)
  }
}

const updateTicket = async () => {
  if (!selectedTicket.value) return
  
  updating.value = true
  
  try {
    const res = await fetch(`${config.public.apiBase}/api/tickets/${selectedTicket.value.id}/status`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${auth.token}`
      },
      body: JSON.stringify(updateForm)
    })
    
    if (res.ok) {
      await loadTickets()
      showDetailsModal.value = false
    } else if (res.status === 401) {
      await auth.logout()
    }
  } catch (err) {
    console.error('Error:', err)
  } finally {
    updating.value = false
  }
}

const sendMessage = async () => {
  if (!newMessage.value.trim() || !selectedTicket.value || isChatDisabled()) return
  
  console.log('📤 ATENCION CHAT: Enviando mensaje:', newMessage.value)
  console.log('📤 ATENCION CHAT: Ticket ID:', selectedTicket.value.id)
  console.log('📤 ATENCION CHAT: Actividades antes:', selectedTicket.value.activities?.length || 0)
  
  sendingMessage.value = true
  
  try {
    const res = await fetch(`${config.public.apiBase}/api/tickets/${selectedTicket.value.id}/message`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${auth.token}`
      },
      body: JSON.stringify({ message: newMessage.value })
    })
    
    console.log('📤 ATENCION CHAT: Respuesta del servidor:', res.status, res.ok)
    
    if (res.ok) {
      newMessage.value = ''
      console.log('📤 ATENCION CHAT: Mensaje enviado exitosamente, recargando...')
      // Recargar solo los datos del ticket sin marcar como visto
      await reloadTicketData(selectedTicket.value.id)
    } else if (res.status === 401) {
      await auth.logout()
    }
  } catch (err) {
    console.error('Error enviando mensaje:', err)
  } finally {
    sendingMessage.value = false
  }
}

const isChatDisabled = () => {
  if (!selectedTicket.value) return true
  return selectedTicket.value.status === 'cerrado' || selectedTicket.value.status === 'resuelto'
}

const getChatPlaceholder = () => {
  if (isChatDisabled()) {
    return 'El chat está deshabilitado para tickets cerrados/resueltos'
  }
  return 'Escribe tu mensaje...'
}

const getChatDisabledMessage = () => {
  if (!selectedTicket.value) return ''
  
  if (selectedTicket.value.status === 'cerrado') {
    return 'No se pueden enviar mensajes en tickets cerrados. Cambia el estado a "En Progreso" para reabrir el chat.'
  }
  if (selectedTicket.value.status === 'resuelto') {
    return 'No se pueden enviar mensajes en tickets resueltos. Cambia el estado a "En Progreso" para reabrir el chat.'
  }
  return ''
}

const hasUnreadMessages = (ticket: { id: number; activities?: Array<{ activity_type: string; user_rol: string; created_at: string }>; status?: string }) => {
  // No mostrar notificaciones en tickets cerrados o resueltos
  if (ticket.status === 'cerrado' || ticket.status === 'resuelto') return false
  
  if (!ticket.activities || ticket.activities.length === 0) return false
  
  // Obtener todos los mensajes
  const messages = ticket.activities.filter((activity) => activity.activity_type === 'message')
  if (messages.length === 0) return false
  
  // Obtener la última vez que se vio este ticket
  const lastViewedKey = `ticket_${ticket.id}_last_viewed`
  const lastViewed = localStorage.getItem(lastViewedKey)
  
  if (!lastViewed) {
    // Si nunca se ha visto, mostrar notificación
    return true
  }
  
  // Buscar si hay mensajes más recientes que la última vez que se vio
  const lastViewedTime = new Date(lastViewed).getTime()
  return messages.some(message => new Date(message.created_at).getTime() > lastViewedTime)
}

const markTicketAsViewed = (ticketId: number) => {
  const lastViewedKey = `ticket_${ticketId}_last_viewed`
  localStorage.setItem(lastViewedKey, new Date().toISOString())
  console.log('👁️ TICKET: Marcado como visto:', ticketId)
}

const reloadTicketData = async (ticketId: number) => {
  try {
    // Cargar actividades
    const resActivities = await fetch(`${config.public.apiBase}/api/tickets/${ticketId}/activities`, {
      headers: {
        'Authorization': `Bearer ${auth.token}`
      }
    })
    
    if (resActivities.ok) {
      const activities = await resActivities.json()
      console.log('🔄 RELOAD: Actividades recargadas:', activities.length)
      
      // Actualizar las actividades del ticket seleccionado
      if (selectedTicket.value) {
        selectedTicket.value.activities = activities
      }
      
      // Hacer scroll al final después de recargar
      setTimeout(() => {
        scrollToBottom()
      }, 100)
    }
  } catch (err) {
    console.error('Error recargando datos del ticket:', err)
  }
}

const scrollToBottom = () => {
  const chatContainer = document.querySelector('.chat-messages')
  if (chatContainer) {
    chatContainer.scrollTop = chatContainer.scrollHeight
  }
}

const getTicketRowClass = (ticket: { id: number; activities?: Array<{ activity_type: string; user_rol: string; created_at: string }>; status?: string }) => {
  if (hasUnreadMessages(ticket)) {
    return 'table-warning border-warning border-3'
  }
  return ''
}

const filterTickets = () => {
  // Handled by computed
}

// Helper functions
const getStatusBadgeClass = (status: string) => {
  const classes: { [key: string]: string } = {
    'abierto': 'bg-warning',
    'en_progreso': 'bg-info',
    'resuelto': 'bg-success',
    'cerrado': 'bg-secondary'
  }
  return classes[status] || 'bg-secondary'
}

const getStatusText = (status: string) => {
  const texts: { [key: string]: string } = {
    'abierto': 'Abierto',
    'en_progreso': 'En Progreso',
    'resuelto': 'Resuelto',
    'cerrado': 'Cerrado'
  }
  return texts[status] || status
}

const getPriorityBadgeClass = (priority: string) => {
  const classes: { [key: string]: string } = {
    'baja': 'bg-success',
    'media': 'bg-primary',
    'alta': 'bg-warning',
    'urgente': 'bg-danger'
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

const getCategoryText = (category: string) => {
  const categories: { [key: string]: string } = {
    'consulta_general': 'Consulta General',
    'problema_tecnico': 'Problema Técnico',
    'solicitud_pedido': 'Solicitud de Pedido',
    'devolucion': 'Devolución',
    'facturacion': 'Facturación',
    'soporte': 'Soporte',
    'otro': 'Otro'
  }
  return categories[category] || category
}

const getActivityTypeText = (type: string) => {
  const types: { [key: string]: string } = {
    'created': 'Creado',
    'status_changed': 'Estado Cambiado',
    'assigned': 'Asignado',
    'comment': 'Comentario',
    'message': 'Mensaje',
    'resolved': 'Resuelto',
    'closed': 'Cerrado'
  }
  return types[type] || type
}

// Usar función global de formateo
const { $formatDate: formatDate } = useNuxtApp()

// Lifecycle
onMounted(() => {
  if (auth.isAuthenticated) {
    loadTickets()
    
    // Actualizar automáticamente cada 30 segundos
    const interval = setInterval(() => {
      if (auth.isAuthenticated) {
        loadTickets()
      }
    }, 30000)
    
    // Limpiar el intervalo cuando el componente se desmonte
    onUnmounted(() => {
      clearInterval(interval)
    })
  }
})
</script>

<style scoped>
.atencion-tickets-page {
  padding: 0;
}

.card {
  margin-bottom: 1.5rem;
}

.table {
  font-size: 0.9rem;
}

.timeline {
  position: relative;
  padding-left: 2rem;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 0.75rem;
  top: 0;
  bottom: 0;
  width: 2px;
  background-color: var(--bs-border-color);
}

.timeline-item {
  position: relative;
  margin-bottom: 1.5rem;
}

.timeline-marker {
  position: absolute;
  left: -2rem;
  top: 0.25rem;
  width: 0.75rem;
  height: 0.75rem;
  background-color: var(--bs-primary);
  border-radius: 50%;
  border: 2px solid white;
  box-shadow: 0 0 0 2px var(--bs-primary);
}

.timeline-content {
  background-color: var(--bs-gray-100);
  padding: 1rem;
  border-radius: 0.5rem;
  border-left: 3px solid var(--bs-primary);
}

/* Animación de pulso para notificaciones */
@keyframes pulse {
  0% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
  100% {
    opacity: 1;
  }
}

.animate-pulse {
  animation: pulse 2s infinite;
}

/* Resaltado mejorado para tickets con mensajes no leídos */
.table-warning {
  background-color: rgba(255, 193, 7, 0.1) !important;
  border-left: 4px solid #ffc107 !important;
}

.table-warning:hover {
  background-color: rgba(255, 193, 7, 0.2) !important;
}

</style>

