<template>
  <div class="soporte-page">
    <div class="container">
      <!-- Header -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <h1 class="display-6 fw-bold mb-2">
                <i class="bi bi-chat-dots me-2"></i>Centro de soporte
              </h1>
              <p class="text-muted mb-0">Chatea con nuestro asistente virtual o crea un ticket de soporte</p>
            </div>
            <div>
              <NuxtLink to="/tickets" class="btn btn-outline-primary me-2">
                <i class="bi bi-ticket-perforated me-2"></i>Mis tickets
              </NuxtLink>
              <button class="btn btn-primary" @click="showTicketModal = true">
                <i class="bi bi-plus-circle me-2"></i>Nuevo ticket
              </button>
            </div>
          </div>
        </div>
      </div>

      <ClientOnly>
        <div v-if="!auth.isAuthenticated" class="alert alert-warning">
          <i class="bi bi-exclamation-triangle me-2"></i>
          Para usar el chatbot y crear tickets debes iniciar sesión.
          <NuxtLink to="/login?next=/soporte" class="btn btn-primary btn-sm ms-2">
            <i class="bi bi-box-arrow-in-right me-1"></i>Iniciar sesión
          </NuxtLink>
        </div>

        <div v-else class="row">
        <!-- Chat Section -->
        <div class="col-lg-8">
          <div class="card h-100">
            <div class="card-header bg-white border-bottom">
              <h5 class="card-title mb-0">
                <i class="bi bi-robot me-2"></i>Asistente virtual
              </h5>
            </div>
            <div class="card-body p-0">
              <div class="chat-container">
                <div class="messages" ref="msgsRef">
                  <div v-for="(m, i) in messages" :key="i" :class="['message', m.role]">
                    <div class="message-content">
                      <div v-if="m.role === 'bot'" class="message-avatar">
                        <i class="bi bi-robot"></i>
                      </div>
                      <div class="message-text">
                        <div v-html="formatMessage(m.content)"></div>
                        <div v-if="m.suggestTicket || m.suggestCatalog" class="mt-2 d-flex gap-2">
                          <button v-if="m.suggestTicket" class="btn btn-sm btn-outline-primary" @click="createTicketFromChat(m.content)">
                            <i class="bi bi-ticket-perforated me-1"></i>Crear ticket de soporte
                          </button>
                          <button v-if="m.suggestCatalog" class="btn btn-sm btn-success" @click="goToCatalog">
                            <i class="bi bi-shop me-1"></i>Ver catálogo
                          </button>
                        </div>
                      </div>
                      <div v-if="m.role === 'user'" class="message-avatar">
                        <i class="bi bi-person"></i>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="input-area">
                  <div class="input-group">
                    <input 
                      v-model="text" 
                      @keyup.enter="send" 
                      placeholder="Escribe tu mensaje..." 
                      class="form-control"
                      :disabled="loading"
                    />
                    <button @click="send" class="btn btn-primary" :disabled="loading || !text.trim()">
                      <span v-if="loading" class="spinner-border spinner-border-sm me-1"></span>
                      <i v-else class="bi bi-send"></i>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="col-lg-4">
          <div class="card">
            <div class="card-header bg-white border-bottom">
              <h5 class="card-title mb-0">
                <i class="bi bi-lightning me-2"></i>Acciones rápidas
              </h5>
            </div>
            <div class="card-body">
              <div class="d-grid gap-2">
                <button class="btn btn-outline-primary w-100" @click="sendQuickMessage('¿Cómo puedo hacer un pedido?')">
                  <i class="bi bi-cart me-2"></i>Hacer un Pedido
                </button>
                <button class="btn btn-outline-primary w-100" @click="sendQuickMessage('¿Cuáles son los métodos de pago?')">
                  <i class="bi bi-credit-card me-2"></i>Métodos de Pago
                </button>
                <button class="btn btn-outline-primary w-100" @click="sendQuickMessage('¿Cómo puedo hacer una devolución?')">
                  <i class="bi bi-arrow-return-left me-2"></i>Devoluciones
                </button>
                <button class="btn btn-outline-primary w-100" @click="sendQuickMessage('¿Cuánto tardan los envíos?')">
                  <i class="bi bi-truck me-2"></i>Envíos
                </button>
              </div>
            </div>
          </div>

          <!-- FAQ Section -->
          <div class="card mt-3">
            <div class="card-header bg-white border-bottom">
              <h5 class="card-title mb-0">
                <i class="bi bi-question-circle me-2"></i>Preguntas frecuentes
              </h5>
            </div>
            <div class="card-body">
              <div class="accordion" id="faqAccordion">
                <div class="accordion-item">
                  <h2 class="accordion-header">
                    <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#faq1">
                      ¿Cómo puedo hacer un pedido?
                    </button>
                  </h2>
                  <div id="faq1" class="accordion-collapse collapse" data-bs-parent="#faqAccordion">
                    <div class="accordion-body">
                      Navega por nuestro catálogo, añade productos al carrito y procede al checkout. Necesitarás registrarte para completar el pedido.
                    </div>
                  </div>
                </div>
                <div class="accordion-item">
                  <h2 class="accordion-header">
                    <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#faq2">
                      ¿Cuáles son los métodos de pago?
                    </button>
                  </h2>
                  <div id="faq2" class="accordion-collapse collapse" data-bs-parent="#faqAccordion">
                    <div class="accordion-body">
                      Aceptamos tarjetas de crédito/débito, PayPal y transferencias bancarias.
                    </div>
                  </div>
                </div>
                <div class="accordion-item">
                  <h2 class="accordion-header">
                    <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#faq3">
                      ¿Cuánto tardan los envíos?
                    </button>
                  </h2>
                  <div id="faq3" class="accordion-collapse collapse" data-bs-parent="#faqAccordion">
                    <div class="accordion-body">
                      Los envíos tardan entre 2-5 días hábiles. 
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        </div>
      </ClientOnly>

      <!-- Quick Ticket Modal -->
      <ClientOnly>
        <div class="modal fade" :class="{ show: showTicketModal }" :style="{ display: showTicketModal ? 'block' : 'none' }" tabindex="-1">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">
                <i class="bi bi-ticket-perforated me-2"></i>Crear ticket de soporte
              </h5>
              <button type="button" class="btn-close" @click="showTicketModal = false"></button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="createQuickTicket">
                <div class="mb-3">
                  <label for="titulo" class="form-label">Título *</label>
                  <input
                    v-model="quickTicketForm.titulo"
                    type="text"
                    class="form-control"
                    id="titulo"
                    required
                    placeholder="Describe brevemente tu consulta"
                  >
                </div>
                
                <div class="mb-3">
                  <label for="categoria" class="form-label">Categoría *</label>
                  <select v-model="quickTicketForm.categoria" class="form-select" id="categoria" required>
                    <option value="">Selecciona una categoría</option>
                    <option value="soporte">Soporte</option>
                    <option value="ventas">Ventas</option>
                    <option value="tecnico">Técnico</option>
                    <option value="general">General</option>
                  </select>
                </div>
                
                <div class="mb-3">
                  <label for="descripcion" class="form-label">Descripción *</label>
                  <textarea
                    v-model="quickTicketForm.descripcion"
                    class="form-control"
                    id="descripcion"
                    rows="3"
                    required
                    placeholder="Describe detalladamente tu consulta o problema..."
                  ></textarea>
                </div>
                
                <div class="modal-footer">
                  <button type="button" class="btn btn-secondary" @click="showTicketModal = false">
                    Cancelar
                  </button>
                  <button type="submit" class="btn btn-primary" :disabled="creatingTicket">
                    <span v-if="creatingTicket" class="spinner-border spinner-border-sm me-2"></span>
                    {{ creatingTicket ? 'Creando...' : 'Crear Ticket' }}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
        </div>
        <div v-if="showTicketModal" class="modal-backdrop fade show"></div>
      </ClientOnly>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onUnmounted, nextTick } from 'vue'
import { useRuntimeConfig } from 'nuxt/app'
import { useAuthStore } from '../../stores/auth'
import { io } from 'socket.io-client'

definePageMeta({
  middleware: ['user-only'],
  layout: 'default'
})

const config = useRuntimeConfig()
const auth = useAuthStore()
const messages = ref<{role:'user'|'bot', content:string, suggestTicket?: boolean, suggestCatalog?: boolean}[]>([
  { role: 'bot', content: 'Hola, ¿en qué puedo ayudarte?' }
])
const text = ref('')
const msgsRef = ref<HTMLDivElement|null>(null)
const loading = ref(false)
const showTicketModal = ref(false)
const creatingTicket = ref(false)

// Quick ticket form
const quickTicketForm = reactive({
  titulo: '',
  categoria: '',
  descripcion: ''
})

let socket: any

const connectSocket = () => {
  // Si ya hay un socket conectado, no hacer nada
  if (socket && socket.connected) {
    console.log('Socket ya está conectado, no reconectando')
    return
  }
  
  // Si hay un socket pero no está conectado, desconectarlo
  if (socket) {
    console.log('Desconectando socket anterior...')
    socket.disconnect()
  }
  
  console.log('Creando nueva conexión de socket...')
  console.log('Token disponible:', auth.token ? 'Sí' : 'No')
  console.log('Token (primeros 20 chars):', auth.token ? auth.token.substring(0, 20) + '...' : 'N/A')
  
  socket = io(config.public.apiBase as unknown as string, {
    auth: {
      token: auth.token
    },
    extraHeaders: {
      'Authorization': `Bearer ${auth.token}`
    },
    autoConnect: true,
    reconnection: true,
    reconnectionDelay: 2000,
    reconnectionAttempts: 3,
    timeout: 20000,
    forceNew: true,
    transports: ['websocket', 'polling'],
    upgrade: true,
    rememberUpgrade: true
  })
  
  setupSocketListeners()
}

const updateSocketAuth = () => {
  if (socket) {
    // Solo reconectar si el socket no está conectado o si hay problemas de autenticación
    if (!socket.connected) {
      console.log('Socket desconectado, reconectando...')
      connectSocket()
    } else {
      console.log('Socket conectado, manteniendo conexión activa')
    }
  }
}

const setupSocketListeners = () => {
  socket.on('connect', () => {
    console.log('Conectado al chat de la tienda online - Socket ID:', socket.id)
  })
  
  socket.on('connect_error', (error: any) => {
    console.error('Error de conexión:', error)
    // No reconectar automáticamente aquí, dejar que el sistema de reconexión automática lo maneje
  })
  
  socket.on('reconnect', (attemptNumber: any) => {
    console.log('Socket reconectado después de', attemptNumber, 'intentos')
    // El socket se reconectó automáticamente, pero puede que no tenga el token
    // Solo reconectar manualmente si hay un error de autenticación
  })
  
  socket.on('disconnect', (reason: any) => {
    console.log('Desconectado del chat:', reason)
  })
  
  socket.on('server_message', (data: any) => {
    messages.value.push({ role: 'bot', content: data?.message || 'Conectado' })
  })
  
  socket.on('answer', (data: any) => {
    const suggestTicket = data?.message?.toLowerCase().includes('ticket') || 
                         data?.message?.toLowerCase().includes('soporte') ||
                         data?.message?.toLowerCase().includes('especialista') ||
                         data?.message?.toLowerCase().includes('puedes crear un ticket de soporte')
    
    const suggestCatalog = data?.message?.toLowerCase().includes('te interesa') || 
                          data?.message?.toLowerCase().includes('puedes ver todos los productos') ||
                          data?.message?.toLowerCase().includes('catálogo') ||
                          data?.message?.toLowerCase().includes('catalogo') ||
                          data?.message?.toLowerCase().includes('producto') ||
                          data?.message?.toLowerCase().includes('productos') ||
                          data?.message?.toLowerCase().includes('categoría') ||
                          data?.message?.toLowerCase().includes('categoria') ||
                          data?.message?.toLowerCase().includes('precio') ||
                          data?.message?.toLowerCase().includes('stock') ||
                          data?.message?.toLowerCase().includes('disponible') ||
                          data?.message?.toLowerCase().includes('comprar') ||
                          data?.message?.toLowerCase().includes('ver más') ||
                          data?.message?.toLowerCase().includes('saber más')
    
    messages.value.push({ 
      role: 'bot', 
      content: data?.message || 'Sin respuesta',
      suggestTicket: suggestTicket,
      suggestCatalog: suggestCatalog
    })
    nextTick(() => msgsRef.value && (msgsRef.value.scrollTop = msgsRef.value.scrollHeight))
  })
  
  socket.on('error', (data: any) => {
    const errorMessage = data?.message || 'Error de conexión'
    console.log('Error del socket:', errorMessage)
    
    // Solo reconectar si realmente es un error de autenticación y el socket no está conectado
    if ((errorMessage.includes('Sesión expirada') || errorMessage.includes('sesión expirada')) && !socket.connected) {
      console.log('Error de sesión expirada, reconectando socket...')
      connectSocket()
    } else {
      // Mostrar el error al usuario sin reconectar
      messages.value.push({ role: 'bot', content: errorMessage })
    }
    
    nextTick(() => msgsRef.value && (msgsRef.value.scrollTop = msgsRef.value.scrollHeight))
  })
}

onMounted(() => {
  if (!auth.isAuthenticated) return
  
  // Conectar socket inicial
  connectSocket()
  
  // Escuchar cuando se renueva el token (solo para logging)
  window.addEventListener('tokenRefreshed', (event: any) => {
    console.log('Token renovado, socket mantendrá conexión activa')
    // El socket mantendrá la conexión activa, no necesitamos reconectar
  })
})

onUnmounted(() => {
  // Limpiar event listener y desconectar socket
  window.removeEventListener('tokenRefreshed', () => {})
  if (socket) {
    socket.disconnect()
  }
})

const send = () => {
  if (!text.value.trim() || !socket || loading.value) return
  
  loading.value = true
  messages.value.push({ role: 'user', content: text.value })
  socket.emit('ask', { message: text.value })
  text.value = ''
  
  nextTick(() => msgsRef.value && (msgsRef.value.scrollTop = msgsRef.value.scrollHeight))
  
  // Simular tiempo de respuesta
  setTimeout(() => {
    loading.value = false
  }, 1000)
}

const sendQuickMessage = (message: string) => {
  text.value = message
  send()
}

const createQuickTicket = async () => {
  creatingTicket.value = true
  
  try {
    const res = await fetch(`${config.public.apiBase}/api/tickets/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${auth.token}`
      },
      body: JSON.stringify({
        title: quickTicketForm.titulo,
        description: quickTicketForm.descripcion,
        category: quickTicketForm.categoria,
        priority: 'media'
      })
    })
    
    if (res.ok) {
      showTicketModal.value = false
      quickTicketForm.titulo = ''
      quickTicketForm.categoria = ''
      quickTicketForm.descripcion = ''
      
      // Mostrar mensaje de éxito
      messages.value.push({ 
        role: 'bot', 
        content: '¡Ticket creado exitosamente! Puedes verlo en la sección "Mis Tickets".' 
      })
    } else if (res.status === 401) {
      await auth.logout()
    } else {
      const data = await res.json()
      throw new Error(data.error || 'Error al crear ticket')
    }
  } catch (err: any) {
    console.error('Error creando ticket:', err)
    messages.value.push({ 
      role: 'bot', 
      content: 'Hubo un error al crear el ticket. Por favor, inténtalo de nuevo.' 
    })
  } finally {
    creatingTicket.value = false
  }
}

const createTicketFromChat = (content: string) => {
  // Detectar si es una consulta específica de acciones rápidas
  let titulo = 'Consulta desde chat'
  let categoria = 'general'
  let descripcion = content
  
  if (content.includes('Consulta sobre:')) {
    // Es una consulta de acción rápida
    const lines = content.split('\n')
    const consultaLine = lines.find(line => line.startsWith('Consulta sobre:'))
    if (consultaLine) {
      const consulta = consultaLine.replace('Consulta sobre:', '').trim()
      titulo = `Consulta: ${consulta}`
      
      // Mapear consulta a categoría
      if (consulta.includes('pedido')) categoria = 'ventas'
      else if (consulta.includes('pago')) categoria = 'ventas'
      else if (consulta.includes('devolución')) categoria = 'soporte'
      else if (consulta.includes('envío')) categoria = 'soporte'
      
      descripcion = `Consulta sobre: ${consulta}\n\nPor favor, proporciona más detalles sobre tu consulta específica.`
    }
  }
  
  quickTicketForm.titulo = titulo
  quickTicketForm.categoria = categoria
  quickTicketForm.descripcion = descripcion
  showTicketModal.value = true
}

const createQuickTicketFromAction = (question: string, category: string) => {
  // Mapear categorías a las categorías del sistema
  const categoryMap: { [key: string]: string } = {
    'pedidos': 'ventas',
    'pagos': 'ventas',
    'devoluciones': 'soporte',
    'envios': 'soporte'
  }
  
  // Crear mensaje en el chat que sugiere crear ticket
  const ticketMessage = `Consulta sobre: ${question}\n\nSi necesitas ayuda especializada, puedes crear un ticket de soporte y nuestro equipo te ayudará personalmente.`
  
  // Agregar mensaje al chat con sugerencia de ticket
  messages.value.push({ 
    role: 'bot', 
    content: ticketMessage,
    suggestTicket: true
  })
  
  // Scroll al final del chat
  nextTick(() => msgsRef.value && (msgsRef.value.scrollTop = msgsRef.value.scrollHeight))
}

const goToCatalog = () => {
  // Redirigir al catálogo
  navigateTo('/catalogo')
}

const formatMessage = (content: string) => {
  // Convertir saltos de línea a <br>
  let formatted = content.replace(/\n/g, '<br>')
  
  // Convertir URLs a enlaces
  formatted = formatted.replace(
    /(https?:\/\/[^\s]+)/g, 
    '<a href="$1" target="_blank" class="text-primary">$1</a>'
  )
  
  return formatted
}
</script>

<style scoped>
.soporte-page {
  padding: 2rem 0;
}

.chat-container {
  height: 500px;
  display: flex;
  flex-direction: column;
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  background-color: var(--bs-gray-50);
}

.message {
  margin-bottom: 1rem;
}

.message-content {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
}

.message.user .message-content {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  flex-shrink: 0;
}

.message.bot .message-avatar {
  background-color: var(--bs-primary);
  color: white;
}

.message.user .message-avatar {
  background-color: var(--bs-secondary);
  color: white;
}

.message-text {
  max-width: 70%;
  padding: 0.75rem 1rem;
  border-radius: 1rem;
  word-wrap: break-word;
}

.message.bot .message-text {
  background-color: white;
  border: 1px solid var(--bs-border-color);
}

.message.user .message-text {
  background-color: var(--bs-primary);
  color: white;
}

.input-area {
  padding: 1rem;
  border-top: 1px solid var(--bs-border-color);
  background-color: white;
}

.card {
  border-radius: 1rem;
  border: 1px solid var(--bs-border-color);
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

.modal-content {
  border-radius: 1rem;
  border: 1px solid var(--bs-border-color);
}

.modal-header {
  border-bottom: 1px solid var(--bs-border-color);
}

/* Dark theme adjustments */
.dark-theme .messages {
  background-color: var(--bs-gray-200);
}

.dark-theme .message.bot .message-text {
  background-color: var(--bs-gray-100);
  border-color: var(--bs-border-color);
}

.dark-theme .input-area {
  background-color: var(--bs-gray-100);
  border-top-color: var(--bs-border-color);
}
</style>


