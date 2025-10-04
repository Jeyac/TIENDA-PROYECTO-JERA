<template>
  <div class="chats-page">
    <div class="container-fluid">
      <!-- Header -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <h1 class="display-6 fw-bold mb-2">
                <i class="bi bi-chat-dots me-2"></i>Historial de Chats
              </h1>
              <p class="text-muted mb-0">Revisa las conversaciones con el chatbot</p>
            </div>
            <div class="d-flex gap-2">
              <button class="btn btn-outline-secondary" @click="loadChats">
                <i class="bi bi-arrow-clockwise me-2"></i>Actualizar
              </button>
              <button class="btn btn-outline-danger" @click="clearAllChats" :disabled="deleting">
                <i class="bi bi-trash me-2"></i>Limpiar Todo
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Filters -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="card border-0 shadow-sm">
            <div class="card-body">
              <div class="row g-3 align-items-end">
                <div class="col-md-4">
                  <label for="userFilter" class="form-label">Filtrar por Usuario</label>
                  <select
                    v-model="selectedUser"
                    class="form-select"
                    id="userFilter"
                    @change="filterChats"
                  >
                    <option value="">Todos los usuarios</option>
                    <option v-for="user in users" :key="user.id" :value="user.id">
                      {{ user.username }} ({{ user.email }})
                    </option>
                  </select>
                </div>
                <div class="col-md-4">
                  <label for="dateFilter" class="form-label">Filtrar por Fecha</label>
                  <input
                    v-model="selectedDate"
                    type="date"
                    class="form-control"
                    id="dateFilter"
                    @change="filterChats"
                  >
                </div>
                <div class="col-md-4">
                  <button class="btn btn-outline-secondary w-100" @click="clearFilters">
                    <i class="bi bi-x-circle me-2"></i>Limpiar Filtros
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Chats List -->
      <div class="card border-0 shadow-sm">
        <div class="card-header bg-white border-bottom">
          <div class="row align-items-center">
            <div class="col-md-6">
              <h5 class="card-title mb-0">
                <i class="bi bi-list-ul me-2"></i>Conversaciones
                <span class="badge bg-primary ms-2">{{ filteredChats.length }}</span>
              </h5>
            </div>
            <div class="col-md-6 text-end">
              <small class="text-muted">
                Mostrando {{ filteredChats.length }} de {{ chats.length }} chats
              </small>
            </div>
          </div>
        </div>
        <div class="card-body p-0">
          <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Cargando...</span>
            </div>
            <p class="text-muted mt-3">Cargando chats...</p>
          </div>
          
          <div v-else-if="filteredChats.length === 0" class="text-center py-5">
            <i class="bi bi-chat text-muted" style="font-size: 4rem;"></i>
            <h3 class="text-muted mt-3">No hay chats</h3>
            <p class="text-muted">No se encontraron conversaciones con los filtros aplicados.</p>
          </div>
          
          <div v-else class="chats-list">
            <div v-for="chat in filteredChats" :key="chat.id" class="chat-item">
              <div class="chat-header" @click="toggleChat(chat.id)">
                <div class="d-flex justify-content-between align-items-center">
                  <div class="d-flex align-items-center">
                    <div class="avatar bg-primary text-white rounded-circle me-3">
                      {{ chat.usuario_nombre?.charAt(0).toUpperCase() || 'U' }}
                    </div>
                    <div>
                      <h6 class="mb-1">{{ chat.usuario_nombre || 'Usuario Anónimo' }}</h6>
                      <small class="text-muted">{{ chat.usuario_email || 'Sin email' }}</small>
                    </div>
                  </div>
                  <div class="text-end">
                    <div class="d-flex align-items-center gap-2">
                      <span class="badge bg-secondary">{{ chat.mensajes_count || 0 }} mensajes</span>
                      <small class="text-muted">{{ formatDate(chat.fecha_creacion) }}</small>
                      <i class="bi bi-chevron-down" :class="{ 'rotate-180': expandedChats.includes(chat.id) }"></i>
                    </div>
                  </div>
                </div>
              </div>
              
              <div v-if="expandedChats.includes(chat.id)" class="chat-messages">
                <div class="messages-container">
                  <div v-for="message in chat.mensajes" :key="message.id" class="message-item">
                    <div class="message" :class="{ 'user-message': message.tipo === 'usuario', 'bot-message': message.tipo === 'bot' }">
                      <div class="message-header">
                        <strong>{{ message.tipo === 'usuario' ? 'Usuario' : 'Bot' }}</strong>
                        <small class="text-muted ms-2">{{ formatTime(message.fecha_creacion) }}</small>
                      </div>
                      <div class="message-content">
                        {{ message.contenido }}
                      </div>
                    </div>
                  </div>
                </div>
                
                <div class="chat-actions">
                  <button class="btn btn-outline-danger btn-sm" @click="deleteChat(chat.id)">
                    <i class="bi bi-trash me-1"></i>Eliminar Chat
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Delete Confirmation Modal -->
      <div class="modal fade" :class="{ show: showDeleteModal }" :style="{ display: showDeleteModal ? 'block' : 'none' }" tabindex="-1">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title text-danger">
                <i class="bi bi-exclamation-triangle me-2"></i>Confirmar Eliminación
              </h5>
              <button type="button" class="btn-close" @click="showDeleteModal = false"></button>
            </div>
            <div class="modal-body">
              <p>¿Estás seguro de que deseas eliminar esta conversación?</p>
              <p class="text-muted small">Esta acción no se puede deshacer.</p>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="showDeleteModal = false">
                Cancelar
              </button>
              <button type="button" class="btn btn-danger" @click="confirmDelete" :disabled="deleting">
                <span v-if="deleting" class="spinner-border spinner-border-sm me-2"></span>
                {{ deleting ? 'Eliminando...' : 'Eliminar' }}
              </button>
            </div>
          </div>
        </div>
      </div>
      <div v-if="showDeleteModal" class="modal-backdrop fade show"></div>

      <!-- Clear All Confirmation Modal -->
      <div class="modal fade" :class="{ show: showClearModal }" :style="{ display: showClearModal ? 'block' : 'none' }" tabindex="-1">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title text-danger">
                <i class="bi bi-exclamation-triangle me-2"></i>Confirmar Limpieza
              </h5>
              <button type="button" class="btn-close" @click="showClearModal = false"></button>
            </div>
            <div class="modal-body">
              <p>¿Estás seguro de que deseas eliminar TODOS los chats?</p>
              <p class="text-danger small">Esta acción eliminará {{ chats.length }} conversaciones y no se puede deshacer.</p>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="showClearModal = false">
                Cancelar
              </button>
              <button type="button" class="btn btn-danger" @click="confirmClearAll" :disabled="deleting">
                <span v-if="deleting" class="spinner-border spinner-border-sm me-2"></span>
                {{ deleting ? 'Eliminando...' : 'Eliminar Todo' }}
              </button>
            </div>
          </div>
        </div>
      </div>
      <div v-if="showClearModal" class="modal-backdrop fade show"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
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
const chats = ref<any[]>([])
const users = ref<any[]>([])
const loading = ref(false)
const deleting = ref(false)
const error = ref('')

// Filters
const selectedUser = ref('')
const selectedDate = ref('')
const expandedChats = ref<number[]>([])

// Modal states
const showDeleteModal = ref(false)
const showClearModal = ref(false)
const chatToDelete = ref<number | null>(null)

// Computed
const filteredChats = computed(() => {
  let filtered = chats.value

  if (selectedUser.value) {
    filtered = filtered.filter(chat => chat.usuario_id === parseInt(selectedUser.value))
  }

  if (selectedDate.value) {
    const selectedDateObj = new Date(selectedDate.value)
    filtered = filtered.filter(chat => {
      const chatDate = new Date(chat.fecha_creacion)
      return chatDate.toDateString() === selectedDateObj.toDateString()
    })
  }

  return filtered
})

// Methods
const loadChats = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const res = await fetch(`${config.public.apiBase}/api/admin/chats`, {
      headers: {
        'Authorization': `Bearer ${auth.token}`
      }
    })
    
    if (res.ok) {
      chats.value = await res.json()
    } else if (res.status === 401) {
      await auth.logout()
    } else {
      throw new Error('Error al cargar chats')
    }
  } catch (err: any) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

const loadUsers = async () => {
  try {
    const res = await fetch(`${config.public.apiBase}/api/admin/usuarios/`, {
      headers: {
        'Authorization': `Bearer ${auth.token}`
      }
    })
    
    if (res.ok) {
      users.value = await res.json()
    }
  } catch (err) {
    console.error('Error cargando usuarios:', err)
  }
}

const filterChats = () => {
  // Filtering is handled by computed property
}

const clearFilters = () => {
  selectedUser.value = ''
  selectedDate.value = ''
}

const toggleChat = (chatId: number) => {
  const index = expandedChats.value.indexOf(chatId)
  if (index > -1) {
    expandedChats.value.splice(index, 1)
  } else {
    expandedChats.value.push(chatId)
  }
}

const deleteChat = (chatId: number) => {
  chatToDelete.value = chatId
  showDeleteModal.value = true
}

const confirmDelete = async () => {
  if (!chatToDelete.value) return
  
  deleting.value = true
  
  try {
    const res = await fetch(`${config.public.apiBase}/api/admin/chats/${chatToDelete.value}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${auth.token}`
      }
    })
    
    if (res.ok) {
      await loadChats()
      showDeleteModal.value = false
      chatToDelete.value = null
    } else if (res.status === 401) {
      await auth.logout()
    } else {
      throw new Error('Error al eliminar chat')
    }
  } catch (err: any) {
    error.value = err.message
  } finally {
    deleting.value = false
  }
}

const clearAllChats = () => {
  showClearModal.value = true
}

const confirmClearAll = async () => {
  deleting.value = true
  
  try {
    const res = await fetch(`${config.public.apiBase}/api/admin/chats/clear`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${auth.token}`
      }
    })
    
    if (res.ok) {
      await loadChats()
      showClearModal.value = false
    } else if (res.status === 401) {
      await auth.logout()
    } else {
      throw new Error('Error al limpiar chats')
    }
  } catch (err: any) {
    error.value = err.message
  } finally {
    deleting.value = false
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString()
}

const formatTime = (dateString: string) => {
  return new Date(dateString).toLocaleTimeString()
}

// Lifecycle
onMounted(async () => {
  if (auth.isAuthenticated && auth.isAdmin) {
    await Promise.all([
      loadChats(),
      loadUsers()
    ])
  }
})
</script>

<style scoped>
.chats-page {
  padding: 2rem 0;
}

.avatar {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.875rem;
  font-weight: bold;
}

.chat-item {
  border-bottom: 1px solid var(--bs-border-color);
}

.chat-item:last-child {
  border-bottom: none;
}

.chat-header {
  padding: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.chat-header:hover {
  background-color: var(--bs-gray-100);
}

.chat-messages {
  background-color: var(--bs-gray-50);
  border-top: 1px solid var(--bs-border-color);
}

.messages-container {
  max-height: 400px;
  overflow-y: auto;
  padding: 1rem;
}

.message-item {
  margin-bottom: 1rem;
}

.message-item:last-child {
  margin-bottom: 0;
}

.message {
  padding: 0.75rem;
  border-radius: 0.5rem;
  max-width: 80%;
}

.user-message {
  background-color: var(--bs-primary);
  color: white;
  margin-left: auto;
}

.bot-message {
  background-color: var(--bs-light);
  color: var(--bs-dark);
  margin-right: auto;
}

.message-header {
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
}

.message-content {
  white-space: pre-wrap;
  word-wrap: break-word;
}

.chat-actions {
  padding: 1rem;
  border-top: 1px solid var(--bs-border-color);
  background-color: var(--bs-white);
}

.rotate-180 {
  transform: rotate(180deg);
}

.bi-chevron-down {
  transition: transform 0.3s ease;
}

/* Dark theme adjustments */
.dark-theme .chat-header:hover {
  background-color: var(--bs-gray-200);
}

.dark-theme .chat-messages {
  background-color: var(--bs-gray-200);
}

.dark-theme .bot-message {
  background-color: var(--bs-gray-300);
  color: var(--bs-dark);
}

.dark-theme .chat-actions {
  background-color: var(--bs-gray-100);
}
</style>
