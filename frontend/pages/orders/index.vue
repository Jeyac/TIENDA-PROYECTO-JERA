<template>
  <div class="orders-page">
    <!-- Header Section -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h2 class="mb-1">Mis Pedidos</h2>
        <p class="text-muted mb-0">Gestiona tus pedidos y compras</p>
      </div>
    </div>

    <!-- Filters -->
    <div class="card mb-4">
      <div class="card-body">
        <div class="row g-3">
          <div class="col-md-4">
            <SearchBar v-model="searchQuery" placeholder="Buscar pedidos..." />
          </div>
          <div class="col-md-3">
            <select v-model="statusFilter" class="form-select">
              <option value="">Todos los estados</option>
              <option value="pendiente">Pendiente</option>
              <option value="procesando">Procesando</option>
              <option value="enviado">Enviado</option>
              <option value="entregado">Entregado</option>
              <option value="cancelado">Cancelado</option>
            </select>
          </div>
          <div class="col-md-3">
            <select v-model="dateFilter" class="form-select">
              <option value="">Todas las fechas</option>
              <option value="today">Hoy</option>
              <option value="week">Esta semana</option>
              <option value="month">Este mes</option>
              <option value="year">Este año</option>
            </select>
          </div>
          <div class="col-md-2">
            <BaseButton variant="outline-secondary" @click="clearFilters" class="w-100">
              <i class="bi bi-x-circle me-1"></i>Limpiar
            </BaseButton>
          </div>
        </div>
      </div>
    </div>

    <!-- Orders List -->
    <div class="card">
      <div class="card-body p-0">
        <div v-if="loading" class="text-center py-5">
          <InlineSpinner />
          <p class="text-muted mt-2">Cargando pedidos...</p>
        </div>

        <div v-else-if="filteredOrders.length === 0" class="text-center py-5">
          <EmptyState 
            icon="bi-bag" 
            title="No hay pedidos" 
            description="No se encontraron pedidos con los filtros aplicados"
            size="lg"
          />
        </div>

        <div v-else>
          <div v-for="order in paginatedOrders" :key="order.id" class="border-bottom p-4">
            <div class="row align-items-center">
              <div class="col-md-2">
                <div class="text-center">
                  <h6 class="mb-1">Pedido #{{ order.id }}</h6>
                  <small class="text-muted">{{ formatDate(order.fecha_creacion) }}</small>
                </div>
              </div>
              <div class="col-md-3">
                <div>
                  <h6 class="mb-1">{{ order.items_count }} productos</h6>
                  <small class="text-muted">{{ order.items_preview }}</small>
                </div>
              </div>
              <div class="col-md-2">
                <div class="text-center">
                  <h5 class="mb-0 text-primary">Q {{ Number(order.total).toFixed(2) }}</h5>
                </div>
              </div>
              <div class="col-md-2">
                <div class="text-center">
                  <OrderStatusBadge :status="order.estado" />
                </div>
              </div>
              <div class="col-md-3">
                <div class="text-end">
                  <BaseButton variant="outline-primary" @click="viewOrder(order)" class="me-2">
                    <i class="bi bi-eye me-1"></i>Ver Detalles
                  </BaseButton>
                  <!-- Botón de cancelar deshabilitado -->
                  <!-- <BaseButton v-if="order.estado === 'pendiente'" variant="outline-danger" @click="cancelOrder(order)">
                    <i class="bi bi-x-circle me-1"></i>Cancelar
                  </BaseButton> -->
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Pagination -->
        <div v-if="filteredOrders.length > itemsPerPage" class="card-footer">
          <Paginator 
            v-model="currentPage" 
            :total-items="filteredOrders.length" 
            :items-per-page="itemsPerPage"
          />
        </div>
      </div>
    </div>

    <!-- Order Details Modal -->
    <div class="modal fade" :class="{ show: showViewModal }" :style="{ display: showViewModal ? 'block' : 'none' }" tabindex="-1">
      <div class="modal-dialog modal-xl">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Pedido #{{ selectedOrder?.id }}</h5>
            <button type="button" class="btn-close" @click="closeViewModal"></button>
          </div>
          <div class="modal-body">
            <div v-if="selectedOrder" class="row">
              <div class="col-md-8">
                <!-- Order Items -->
                <div class="card">
                  <div class="card-header">
                    <h6 class="mb-0">Productos del Pedido</h6>
                  </div>
                  <div class="card-body">
                    <div v-if="orderItems.length === 0" class="text-center text-muted py-3">
                      No hay productos en este pedido
                    </div>
                    <div v-else>
                      <div v-for="item in orderItems" :key="item.id" class="d-flex align-items-center mb-3 p-3 border rounded">
                        <div class="flex-grow-1">
                          <h6 class="mb-1">{{ item.producto_titulo || `Producto ${item.producto_id}` }}</h6>
                          <p class="text-muted small mb-0">{{ item.producto_descripcion || 'Sin descripción' }}</p>
                        </div>
                        <div class="text-end">
                          <div class="fw-bold">Q {{ Number(item.precio || item.precio_unitario || 0).toFixed(2) }}</div>
                          <small class="text-muted">Cantidad: {{ item.cantidad }}</small>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <div class="col-md-4">
                <!-- Order Summary -->
                <div class="card">
                  <div class="card-header">
                    <h6 class="mb-0">Resumen del Pedido</h6>
                  </div>
                  <div class="card-body">
                    <div class="mb-3">
                      <strong>Estado:</strong>
                      <OrderStatusBadge :status="selectedOrder.estado" class="ms-2" />
                    </div>
                    <div class="mb-3">
                      <strong>Fecha de creación:</strong>
                      <span class="ms-2">{{ formatDate(selectedOrder.fecha_creacion) }}</span>
                    </div>
                    <div class="mb-3">
                      <strong>Total de productos:</strong>
                      <span class="ms-2">{{ selectedOrder.items_count }}</span>
                    </div>
                    <hr>
                    <div class="d-flex justify-content-between">
                      <strong>Total:</strong>
                      <strong class="text-primary">Q {{ Number(selectedOrder.total).toFixed(2) }}</strong>
                    </div>
                  </div>
                </div>

                <!-- Billing Information -->
                <div class="card mt-3">
                  <div class="card-header">
                    <h6 class="mb-0">
                      <i class="bi bi-receipt me-2"></i>Información de Facturación
                    </h6>
                  </div>
                  <div class="card-body">
                    <div v-if="selectedOrder.datos_facturacion && Object.keys(selectedOrder.datos_facturacion).length > 0">
                      <div v-if="selectedOrder.datos_facturacion.nombre" class="mb-2">
                        <strong>Nombre:</strong>
                        <span class="ms-2">{{ selectedOrder.datos_facturacion.nombre }}</span>
                      </div>
                      <div v-if="selectedOrder.datos_facturacion.email" class="mb-2">
                        <strong>Email:</strong>
                        <span class="ms-2">{{ selectedOrder.datos_facturacion.email }}</span>
                      </div>
                      <div v-if="selectedOrder.datos_facturacion.telefono" class="mb-2">
                        <strong>Teléfono:</strong>
                        <span class="ms-2">{{ selectedOrder.datos_facturacion.telefono }}</span>
                      </div>
                      <div v-if="selectedOrder.datos_facturacion.direccion" class="mb-2">
                        <strong>Dirección:</strong>
                        <span class="ms-2">{{ selectedOrder.datos_facturacion.direccion }}</span>
                      </div>
                      <div v-if="selectedOrder.datos_facturacion.ciudad" class="mb-2">
                        <strong>Ciudad:</strong>
                        <span class="ms-2">{{ selectedOrder.datos_facturacion.ciudad }}</span>
                      </div>
                      <div v-if="selectedOrder.datos_facturacion.codigo_postal" class="mb-2">
                        <strong>Código Postal:</strong>
                        <span class="ms-2">{{ selectedOrder.datos_facturacion.codigo_postal }}</span>
                      </div>
                      <div v-if="selectedOrder.datos_facturacion.pais" class="mb-2">
                        <strong>País:</strong>
                        <span class="ms-2">{{ selectedOrder.datos_facturacion.pais }}</span>
                      </div>
                    </div>
                    <div v-else class="text-muted text-center py-3">
                      <i class="bi bi-info-circle me-2"></i>
                      No hay información de facturación disponible para este pedido
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Cancel Order Confirmation Modal -->
    <ConfirmModal 
      v-model="showCancelModal"
      title="Cancelar Pedido"
      :message="`¿Estás seguro de que quieres cancelar el pedido #${orderToCancel?.id}?`"
      confirm-text="Cancelar Pedido"
      variant="danger"
      @confirm="confirmCancelOrder"
    />

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
const orders = ref<any[]>([])
const orderItems = ref<any[]>([])
const loading = ref(false)
const error = ref('')

// Modal states
const showViewModal = ref(false)
const showCancelModal = ref(false)
const selectedOrder = ref<any>(null)
const orderToCancel = ref<any>(null)

// Filters and pagination
const searchQuery = ref('')
const statusFilter = ref('')
const dateFilter = ref('')
const currentPage = ref(1)
const itemsPerPage = 10

// Computed properties
const filteredOrders = computed(() => {
  let filtered = orders.value

  // Search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(o => 
      o.id.toString().includes(query) ||
      o.items_preview.toLowerCase().includes(query)
    )
  }

  // Status filter
  if (statusFilter.value) {
    filtered = filtered.filter(o => o.estado === statusFilter.value)
  }

  // Date filter
  if (dateFilter.value) {
    const now = new Date()
    const orderDate = new Date()
    
    filtered = filtered.filter(o => {
      orderDate.setTime(new Date(o.fecha_creacion).getTime())
      
      switch (dateFilter.value) {
        case 'today':
          return orderDate.toDateString() === now.toDateString()
        case 'week':
          const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000)
          return orderDate >= weekAgo
        case 'month':
          return orderDate.getMonth() === now.getMonth() && orderDate.getFullYear() === now.getFullYear()
        case 'year':
          return orderDate.getFullYear() === now.getFullYear()
        default:
          return true
      }
    })
  }

  return filtered
})

const paginatedOrders = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredOrders.value.slice(start, end)
})

// Methods
const loadOrders = async () => {
  loading.value = true
  try {
    const response = await auth.makeAuthenticatedRequest('/api/pedidos/mis')
    if (response.ok) {
      orders.value = await response.json()
    } else {
      throw new Error('Error al cargar pedidos')
    }
  } catch (err: any) {
    error.value = err.message || 'Error al cargar pedidos'
  } finally {
    loading.value = false
  }
}

const viewOrder = async (order: any) => {
  selectedOrder.value = order
  showViewModal.value = true
  
  // Load order items and billing information
  try {
    const response = await auth.makeAuthenticatedRequest(`/api/pedidos/${order.id}`)
    if (response.ok) {
      const orderData = await response.json()
      orderItems.value = orderData.items || []
      
      // Update billing information if available
      if (orderData.datos_facturacion) {
        selectedOrder.value.datos_facturacion = orderData.datos_facturacion
      }
    }
  } catch (err) {
    console.error('Error al cargar items del pedido:', err)
    orderItems.value = []
  }
}

const cancelOrder = (order: any) => {
  orderToCancel.value = order
  showCancelModal.value = true
}

const confirmCancelOrder = async () => {
  if (!orderToCancel.value) return

  try {
    const response = await auth.makeAuthenticatedRequest(`/api/pedidos/${orderToCancel.value.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        estado: 'cancelado'
      })
    })

    if (response.ok) {
      orderToCancel.value.estado = 'cancelado'
      showCancelModal.value = false
      orderToCancel.value = null
    } else {
      const errorData = await response.json()
      throw new Error(errorData.error || 'Error al cancelar pedido')
    }
  } catch (err: any) {
    error.value = err.message || 'Error al cancelar pedido'
  }
}

const closeViewModal = () => {
  showViewModal.value = false
  selectedOrder.value = null
  orderItems.value = []
}

const clearFilters = () => {
  searchQuery.value = ''
  statusFilter.value = ''
  dateFilter.value = ''
  currentPage.value = 1
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

// Lifecycle
onMounted(async () => {
  if (auth.isAuthenticated) {
    await loadOrders()
  }
})
</script>

<style scoped>
.orders-page {
  padding: 0;
}

.modal.show {
  background-color: rgba(0, 0, 0, 0.5);
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

.border-bottom:last-child {
  border-bottom: none !important;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .d-flex {
    flex-direction: column;
  }
  
  .text-end {
    text-align: start !important;
    margin-top: 1rem;
  }
}
</style>
