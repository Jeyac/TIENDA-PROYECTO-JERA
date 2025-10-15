<template>
  <div class="chats-page">
    <div class="container-fluid">
      <!-- Header -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <h1 class="display-6 fw-bold mb-2">
                <i class="bi bi-chat-dots me-2"></i>Historial de chats
              </h1>
              <p class="text-muted mb-0">Revisa las conversaciones con el chatbot</p>
            </div>
            <div class="d-flex gap-2">
              <BaseButton variant="outline-secondary" @click="loadChats">
                <i class="bi bi-arrow-clockwise me-2"></i>Actualizar
              </BaseButton>
              <BaseButton variant="outline-danger" @click="clearAllChats" :disabled="deleting">
                <i class="bi bi-trash me-2"></i>Limpiar todos los chats
              </BaseButton>
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
                  <label for="userSearch" class="form-label">Buscar por usuario</label>
                  <input
                    v-model="userSearchText"
                    type="text"
                    class="form-control"
                    id="userSearch"
                    placeholder="Buscar por nombre o email..."
                    @input="filterChats"
                  >
                </div>
                <div class="col-md-8">
                  <BaseButton variant="outline-secondary" class="w-100" @click="clearFilters">
                    <i class="bi bi-x-circle me-2"></i>Limpiar filtros
                  </BaseButton>
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
          
          <EmptyState v-else-if="filteredChats.length === 0" icon="bi bi-chat" title="No hay chats" subtitle="No se encontraron conversaciones con los filtros aplicados." />
          
          <div v-else class="chats-list">
            <div v-for="chat in filteredChats" :key="chat.id" class="chat-item">
              <div class="chat-header" @click="toggleChat(chat.id)">
                <div class="d-flex justify-content-between align-items-center">
                  <div class="d-flex align-items-center">
                    <AvatarCircle :text="chat.usuario_nombre || 'U'" class="me-3" />
                    <div>
                      <h6 class="mb-1">{{ chat.usuario_nombre || 'Usuario Anónimo' }}</h6>
                      <small class="text-muted">{{ chat.usuario_email || 'Sin email' }}</small>
                      <div v-if="chat.mensajes && chat.mensajes.length > 0" class="mt-1">
                        <small class="text-muted">
                          <strong>Último mensaje:</strong> 
                          {{ chat.mensajes[chat.mensajes.length - 1].contenido.substring(0, 60) }}{{ chat.mensajes[chat.mensajes.length - 1].contenido.length > 60 ? '...' : '' }}
                        </small>
                      </div>
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
                <div class="messages-container" style="max-height: 800px; overflow-y: auto; border: 1px solid #e9ecef; border-radius: 8px; padding: 15px; background-color: #f8f9fa;">
                  <div v-for="message in chat.mensajes" :key="message.id" class="message-item mb-3">
                    <div class="message" :class="message.tipo === 'usuario' ? 'user-message' : 'bot-message'">
                      <div class="message-header d-flex justify-content-between align-items-center mb-2">
                        <div class="d-flex align-items-center">
                          <span class="badge me-2" :class="message.tipo === 'usuario' ? 'bg-primary' : 'bg-success'">
                            {{ message.tipo === 'usuario' ? 'Usuario' : 'Bot' }}
                          </span>
                          <small class="text-muted">{{ formatTime(message.fecha_creacion) }}</small>
                        </div>
                      </div>
                      <div class="message-content p-3 rounded" :class="message.tipo === 'usuario' ? 'bg-primary text-white' : 'bg-white border'">
                        <div style="white-space: pre-wrap; word-wrap: break-word;">{{ message.contenido }}</div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div class="chat-actions">
                  <BaseButton variant="outline-danger" class="btn-sm" @click="deleteChat(chat.id)">
                    <i class="bi bi-trash me-1"></i>Eliminar chat
                  </BaseButton>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Delete Confirmation Modal -->
      <ConfirmModal
        v-model="showDeleteModal"
        title="Confirmar eliminación"
        message="¿Estás seguro de que deseas eliminar esta conversación? Esta acción no se puede deshacer."
        confirmText="Eliminar"
        confirmVariant="Peligro"
        :loading="deleting"
        @confirm="confirmDelete"
      />

      <!-- Clear All Confirmation Modal -->
      <ConfirmModal
        v-model="showClearModal"
        title="Confirmar limpieza"
        :message="`¿Estás seguro de que deseas eliminar TODOS los chats? Esta acción eliminará ${chats.length} conversaciones y no se puede deshacer.`"
        confirmText="Eliminar todos los chats"
        confirmVariant="Peligro"
        :loading="deleting"
        @confirm="confirmClearAll"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
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
const chats = ref<any[]>([])
const loading = ref(false)
const deleting = ref(false)
const error = ref('')

// Filters
const userSearchText = ref('')
const expandedChats = ref<number[]>([])

// Modal states
const showDeleteModal = ref(false)
const showClearModal = ref(false)
const chatToDelete = ref<number | null>(null)

// Computed
const filteredChats = computed(() => {
  let filtered = chats.value

  // Filtro de búsqueda por texto (nombre o email)
  if (userSearchText.value) {
    const searchText = userSearchText.value.toLowerCase()
    filtered = filtered.filter(chat => {
      const nombre = (chat.usuario_nombre || '').toLowerCase()
      const email = (chat.usuario_email || '').toLowerCase()
      return nombre.includes(searchText) || email.includes(searchText)
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


const filterChats = () => {
  // Filtering is handled by computed property
}

const clearFilters = () => {
  userSearchText.value = ''
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

// Usar funciones globales de formateo
const { $formatDate: formatDate, $formatTime: formatTime } = useNuxtApp()

// Lifecycle
onMounted(async () => {
  if (auth.isAuthenticated && auth.isAdmin) {
    await loadChats()
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
  max-height: 800px;
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
