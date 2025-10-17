<template>
  <div class="orders-page">
    <div class="container-fluid">
      <!-- Header -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <h1 class="display-6 fw-bold mb-2 text-primary">
                <i class="bi bi-bag-check me-2"></i>Gestión de pedidos
              </h1>
              <p class="text-muted mb-0">Administra y supervisa todos los pedidos del sistema</p>
            </div>
            <div class="d-flex gap-2">
              <BaseButton variant="outline-primary" @click="loadOrders" :disabled="loading">
                <i class="bi bi-arrow-clockwise me-2" :class="{ 'spinner-border spinner-border-sm': loading }"></i>
                {{ loading ? 'Cargando...' : 'Actualizar' }}
              </BaseButton>
              <BaseButton variant="success" @click="exportOrders">
                <i class="bi bi-file-earmark-excel me-2"></i>Exportar excel
              </BaseButton>
            </div>
          </div>
        </div>
      </div>

      <!-- Stats Cards -->
      <div class="row mb-4">
        <div class="col-md-3">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-body text-center">
              <div class="text-primary mb-2">
                <i class="bi bi-bag" style="font-size: 2rem;"></i>
              </div>
              <h3 class="fw-bold mb-1">{{ totalOrders }}</h3>
              <p class="text-muted mb-0">Total pedidos</p>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-body text-center">
              <div class="text-warning mb-2">
                <i class="bi bi-clock" style="font-size: 2rem;"></i>
              </div>
              <h3 class="fw-bold mb-1">{{ pendingOrders }}</h3>
              <p class="text-muted mb-0">Pendientes</p>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-body text-center">
              <div class="text-success mb-2">
                <i class="bi bi-check-circle" style="font-size: 2rem;"></i>
              </div>
              <h3 class="fw-bold mb-1">{{ completedOrders }}</h3>
              <p class="text-muted mb-0">Completados</p>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-body text-center">
              <div class="text-info mb-2">
                <i class="bi bi-currency-dollar" style="font-size: 2rem;"></i>
              </div>
              <h3 class="fw-bold mb-1">Q{{ totalRevenue.toFixed(2) }}</h3>
              <p class="text-muted mb-0">Ingresos enviados/entregados</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Filters -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="card border-0 shadow-sm">
            <div class="card-header bg-light border-0">
              <h6 class="mb-0 fw-semibold">
                <i class="bi bi-funnel me-2"></i>Filtros de búsqueda
              </h6>
            </div>
            <div class="card-body">
              <div class="row g-3">
                <div class="col-md-3">
                  <label class="form-label fw-semibold">Buscar</label>
                  <div class="input-group">
                    <span class="input-group-text">
                      <i class="bi bi-search"></i>
                    </span>
                    <input
                      v-model="searchText"
                      type="text"
                      class="form-control"
                      placeholder="Usuario, email o estado..."
                      @input="filterOrders"
                    >
                  </div>
                </div>
                <div class="col-md-2">
                  <label class="form-label fw-semibold">Estado</label>
                  <select
                    v-model="selectedStatus"
                    class="form-select"
                    @change="filterOrders"
                  >
                    <option value="">Todos</option>
                    <option value="pendiente">Pendiente</option>
                    <option value="procesando">Procesando</option>
                    <option value="enviado">Enviado</option>
                    <option value="entregado">Entregado</option>
                    <option value="cancelado">Cancelado</option>
                  </select>
                </div>
                <div class="col-md-2">
                  <label class="form-label fw-semibold">Fecha</label>
                  <input
                    v-model="selectedDate"
                    type="date"
                    class="form-control"
                    @change="filterOrders"
                  >
                </div>
                <div class="col-md-1 d-flex align-items-end">
                  <BaseButton variant="outline-secondary" @click="clearFilters" class="w-100">
                    <i class="bi bi-x-circle"></i>
                  </BaseButton>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Orders Table -->
      <div class="card border-0 shadow-sm">
        <div class="card-header bg-gradient" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
          <div class="row align-items-center">
            <div class="col-md-6">
              <h5 class="card-title mb-0 text-white">
                <i class="bi bi-list-ul me-2"></i>Lista de pedidos
                <span class="badge bg-light text-dark ms-2">{{ filteredOrders.length }}</span>
              </h5>
            </div>
            <div class="col-md-6 text-end">
              <div class="text-white">
                <small class="opacity-75">Total filtrado:</small>
                <strong class="fs-5">Q {{ totalAmount.toFixed(2) }}</strong>
              </div>
            </div>
          </div>
        </div>
        <div class="card-body p-0">
          <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Cargando...</span>
            </div>
            <p class="text-muted mt-3">Cargando pedidos...</p>
          </div>
          
          <EmptyState v-else-if="filteredOrders.length === 0" icon="bi bi-bag" title="No hay pedidos" subtitle="No se encontraron pedidos con los filtros aplicados." />
          
          <div v-else>
            <DataTable
              :items="filteredOrders"
              :columns="[
                { key: 'id', label: 'ID' },
                { key: 'usuario', label: 'Usuario' },
                { key: 'productos', label: 'Productos' },
                { key: 'total', label: 'Total' },
                { key: 'estado', label: 'Estado' },
                { key: 'fecha', label: 'Fecha' },
                { key: 'acciones', label: 'Acciones' }
              ]"
              empty-icon="bi bi-bag"
              empty-title="No hay pedidos"
              empty-subtitle="No se encontraron pedidos con los filtros aplicados."
            >
              <template #row="{ row: order }">
                <td>
                  <div class="fw-bold text-primary">#{{ order.id }}</div>
                </td>
                <td>
                  <div class="d-flex align-items-center">
                    <AvatarCircle :text="order.usuario_nombre || 'U'" size="sm" class="me-3" />
                    <div>
                      <div class="fw-semibold">{{ order.usuario_nombre || 'Usuario' }}</div>
                      <small class="text-muted">{{ order.usuario_email || 'Sin email' }}</small>
                    </div>
                  </div>
                </td>
                <td>
                  <div class="text-center">
                    <span class="badge bg-info-subtle text-info border border-info-subtle px-3 py-2">
                      <i class="bi bi-box me-1"></i>{{ getProductCount(order) }} productos
                    </span>
                  </div>
                </td>
                <td>
                  <div class="text-end">
                    <div class="fw-bold text-success fs-6">Q {{ Number(order.total).toFixed(2) }}</div>
                  </div>
                </td>
                <td>
                  <div class="text-center">
                    <OrderStatusBadge :status="order.estado || 'pendiente'" :text="order.estado || 'pendiente'" />
                  </div>
                </td>
                <td>
                  <div class="text-center">
                    <small class="text-muted">{{ formatDate(order.fecha_creacion) }}</small>
                  </div>
                </td>
                <td>
                  <div class="d-flex justify-content-center gap-1">
                    <BaseButton variant="outline-primary" class="btn-sm" @click="viewOrder(order)" title="Ver detalles">
                      <i class="bi bi-eye"></i>
                    </BaseButton>
                    <BaseButton 
                      variant="outline-success" 
                      class="btn-sm" 
                      @click="updateStatus(order)" 
                      :disabled="order.estado === 'cancelado'"
                      :title="order.estado === 'cancelado' ? 'No se puede modificar un pedido cancelado' : 'Cambiar estado'"
                    >
                      <i class="bi bi-pencil"></i>
                    </BaseButton>
                  </div>
                </td>
              </template>
            </DataTable>
          </div>
        </div>
      </div>

      <!-- Order Details Modal -->
      <div class="modal fade" :class="{ show: showDetailsModal }" :style="{ display: showDetailsModal ? 'block' : 'none' }" tabindex="-1">
        <div class="modal-dialog modal-lg">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">
                <i class="bi bi-bag me-2"></i>Detalles del pedido #{{ selectedOrder?.id }}
              </h5>
              <button type="button" class="btn-close" @click="showDetailsModal = false"></button>
            </div>
            <div class="modal-body">
              <div v-if="selectedOrder" class="order-details">
                <div class="row mb-3">
                  <div class="col-md-4">
                    <h6><i class="bi bi-person me-2"></i>Información del usuario</h6>
                    <p class="mb-1"><strong>Nombre:</strong> {{ selectedOrder.usuario_nombre }}</p>
                    <p class="mb-1"><strong>Email:</strong> {{ selectedOrder.usuario_email }}</p>
                  </div>
                  <div class="col-md-4">
                    <h6><i class="bi bi-bag me-2"></i>Información del pedido</h6>
                    <p class="mb-1"><strong>Estado:</strong> 
                      <span class="badge" :class="getStatusBadgeClass(selectedOrder.estado)">
                        {{ selectedOrder.estado || 'Pendiente' }}
                      </span>
                    </p>
                    <p class="mb-1"><strong>Fecha:</strong> {{ formatDate(selectedOrder.fecha_creacion) }}</p>
                    <p class="mb-1"><strong>Total:</strong> Q {{ Number(selectedOrder.total).toFixed(2) }}</p>
                  </div>
                  <div class="col-md-4">
                    <h6><i class="bi bi-geo-alt me-2"></i>Información de facturación</h6>
                    <div v-if="selectedOrder.datos_facturacion && Object.keys(selectedOrder.datos_facturacion).length > 0">
                      <p v-if="selectedOrder.datos_facturacion.nombre" class="mb-1"><strong>Nombre:</strong> {{ selectedOrder.datos_facturacion.nombre }}</p>
                      <p v-if="selectedOrder.datos_facturacion.email" class="mb-1"><strong>Email:</strong> {{ selectedOrder.datos_facturacion.email }}</p>
                      <p v-if="selectedOrder.datos_facturacion.telefono" class="mb-1"><strong>Teléfono:</strong> {{ selectedOrder.datos_facturacion.telefono }}</p>
                      <p v-if="selectedOrder.datos_facturacion.direccion" class="mb-1"><strong>Dirección:</strong> {{ selectedOrder.datos_facturacion.direccion }}</p>
                      <p v-if="selectedOrder.datos_facturacion.ciudad" class="mb-1"><strong>Ciudad:</strong> {{ selectedOrder.datos_facturacion.ciudad }}</p>
                    </div>
                    <div v-else class="text-muted">
                      <small>No hay información de facturación</small>
                    </div>
                  </div>
                </div>
                
                <div v-if="selectedOrder.productos && selectedOrder.productos.length > 0">
                  <h6><i class="bi bi-box me-2"></i>Productos del Pedido</h6>
                  <div class="table-responsive">
                    <table class="table table-sm table-hover">
                      <thead class="table-light">
                        <tr>
                          <th>Producto</th>
                          <th class="text-center">Cantidad</th>
                          <th class="text-end">Precio Unit.</th>
                          <th class="text-end">Subtotal</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="item in selectedOrder.productos" :key="item.id">
                          <td>
                            <div>
                              <div class="fw-semibold">{{ item.titulo || `Producto ${item.producto_id}` }}</div>
                              <small v-if="item.descripcion" class="text-muted">{{ item.descripcion }}</small>
                              <small v-else class="text-muted">ID: {{ item.producto_id }}</small>
                            </div>
                          </td>
                          <td class="text-center">
                            <span class="badge bg-primary">{{ item.cantidad }}</span>
                          </td>
                          <td class="text-end">
                            <span class="fw-semibold">Q {{ Number(item.precio_unitario || item.precio || 0).toFixed(2) }}</span>
                          </td>
                          <td class="text-end">
                            <span class="fw-bold text-success">Q {{ Number((item.precio_unitario || item.precio || 0) * item.cantidad).toFixed(2) }}</span>
                          </td>
                        </tr>
                      </tbody>
                      <tfoot class="table-light">
                        <tr>
                          <th colspan="3" class="text-end">Total del Pedido:</th>
                          <th class="text-end text-success">Q {{ Number(selectedOrder.total).toFixed(2) }}</th>
                        </tr>
                      </tfoot>
                    </table>
                  </div>
                </div>
                <div v-else class="text-center text-muted py-3">
                  <i class="bi bi-box me-2"></i>No hay productos en este pedido
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <BaseButton variant="secondary" @click="showDetailsModal = false">
                Cerrar
              </BaseButton>
            </div>
          </div>
        </div>
      </div>
      <div v-if="showDetailsModal" class="modal-backdrop fade show"></div>

      <!-- Update Status Modal -->
      <div class="modal fade" :class="{ show: showStatusModal }" :style="{ display: showStatusModal ? 'block' : 'none' }" tabindex="-1">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">
                <i class="bi bi-pencil me-2"></i>Actualizar estado
              </h5>
              <button type="button" class="btn-close" @click="showStatusModal = false"></button>
            </div>
            <div class="modal-body">
              <div v-if="selectedOrder && selectedOrder.estado === 'cancelado'" class="alert alert-warning" role="alert">
                <i class="bi bi-exclamation-triangle me-2"></i>
                <strong>Pedido cancelado:</strong> No se puede modificar el estado de un pedido que ha sido cancelado.
              </div>
              <div v-else class="mb-3">
                <label for="newStatus" class="form-label">Nuevo estado</label>
                <select v-model="newStatus" class="form-select" id="newStatus">
                  <option value="pendiente">Pendiente</option>
                  <option value="procesando">Procesando</option>
                  <option value="enviado">Enviado</option>
                  <option value="entregado">Entregado</option>
                  <option value="cancelado">Cancelado</option>
                </select>
              </div>
            </div>
            <div class="modal-footer">
              <BaseButton variant="secondary" @click="showStatusModal = false">
                Cancelar
              </BaseButton>
              <BaseButton 
                variant="primary" 
                @click="confirmStatusUpdate" 
                :loading="updating" 
                :disabled="updating || (selectedOrder && selectedOrder.estado === 'cancelado')"
              >
                {{ updating ? 'Actualizando...' : 'Actualizar' }}
              </BaseButton>
            </div>
          </div>
        </div>
      </div>
      <div v-if="showStatusModal" class="modal-backdrop fade show"></div>
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
const orders = ref<any[]>([])
const loading = ref(false)
const updating = ref(false)
const error = ref('')

// Filters
const selectedStatus = ref('')
const selectedDate = ref('')
const searchText = ref('')

// Modal states
const showDetailsModal = ref(false)
const showStatusModal = ref(false)
const selectedOrder = ref<any>(null)
const newStatus = ref('')

// Computed
const filteredOrders = computed(() => {
  let filtered = orders.value

  if (selectedStatus.value) {
    filtered = filtered.filter(order => order.estado === selectedStatus.value)
  }

  if (selectedDate.value) {
    const filterDate = new Date(selectedDate.value)
    const filterDateString = filterDate.toISOString().split('T')[0] // YYYY-MM-DD
    
    console.log('Filtrando por fecha:', filterDateString)
    
    filtered = filtered.filter(order => {
      if (!order.fecha_creacion) return false
      
      // Convertir la fecha ISO a string YYYY-MM-DD para comparar
      const orderDate = new Date(order.fecha_creacion)
      const orderDateString = orderDate.toISOString().split('T')[0]
      
      console.log('Comparando:', orderDateString, 'con', filterDateString)
      
      return orderDateString === filterDateString
    })
  }

  if (searchText.value) {
    const q = searchText.value.toLowerCase()
    filtered = filtered.filter(order =>
      (order.usuario_nombre && order.usuario_nombre.toLowerCase().includes(q)) ||
      (order.usuario_email && order.usuario_email.toLowerCase().includes(q)) ||
      (order.estado && order.estado.toLowerCase().includes(q)) ||
      String(order.id).includes(q)
    )
  }

  return filtered
})

const totalAmount = computed(() => {
  return filteredOrders.value.reduce((sum, order) => sum + Number(order.total), 0)
})

// Estadísticas para las tarjetas
const totalOrders = computed(() => orders.value.length)
const pendingOrders = computed(() => orders.value.filter(order => order.estado === 'pendiente').length)
const completedOrders = computed(() => orders.value.filter(order => order.estado === 'entregado').length)
const totalRevenue = computed(() => orders.value.filter(order => ['enviado', 'entregado'].includes(order.estado)).reduce((sum, order) => sum + Number(order.total), 0))

// Methods
const loadOrders = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const res = await fetch(`${config.public.apiBase}/api/admin/pedidos`, {
      headers: {
        'Authorization': `Bearer ${auth.token}`
      }
    })
    
    if (res.ok) {
      const data = await res.json()
      console.log('Orders loaded from backend:', data)
      console.log('Sample order fecha_creacion:', data[0]?.fecha_creacion)
      orders.value = data
    } else if (res.status === 401) {
      await auth.logout()
    } else {
      throw new Error('Error al cargar pedidos')
    }
  } catch (err: any) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}


const filterOrders = () => {
  // Filtering is handled by computed property
}

const clearFilters = () => {
  selectedStatus.value = ''
  selectedDate.value = ''
  searchText.value = ''
}

const viewOrder = (order: any) => {
  console.log('Order data:', order)
  console.log('Order productos:', order.productos)
  selectedOrder.value = order
  showDetailsModal.value = true
}

const updateStatus = (order: any) => {
  // Verificar que el pedido no esté cancelado
  if (order.estado === 'cancelado') {
    alert('No se puede modificar el estado de un pedido cancelado')
    return
  }
  
  selectedOrder.value = order
  newStatus.value = order.estado || 'pendiente'
  showStatusModal.value = true
}

const confirmStatusUpdate = async () => {
  if (!selectedOrder.value) return
  
  // Verificar que el pedido no esté cancelado
  if (selectedOrder.value.estado === 'cancelado') {
    alert('No se puede modificar el estado de un pedido cancelado')
    return
  }
  
  updating.value = true
  
  try {
    const res = await fetch(`${config.public.apiBase}/api/admin/pedidos/${selectedOrder.value.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${auth.token}`
      },
      body: JSON.stringify({ estado: newStatus.value })
    })
    
    if (res.ok) {
      await loadOrders()
      showStatusModal.value = false
      
      // Emitir notificación si se canceló el pedido
      if (newStatus.value === 'cancelado') {
        if (typeof window !== 'undefined') {
          window.dispatchEvent(new CustomEvent('stockActualizado', { 
            detail: { message: `Stock restaurado para pedido #${selectedOrder.value.id}` } 
          }))
        }
      }
      
      selectedOrder.value = null
    } else if (res.status === 401) {
      await auth.logout()
    } else {
      throw new Error('Error al actualizar estado')
    }
  } catch (err: any) {
    error.value = err.message
  } finally {
    updating.value = false
  }
}

const exportOrders = () => {
  // Simple CSV export
  const csvContent = [
    ['ID', 'Usuario', 'Email', 'Total', 'Estado', 'Fecha'].join(','),
    ...filteredOrders.value.map(order => [
      order.id,
      order.usuario_nombre || '',
      order.usuario_email || '',
      order.total,
      order.estado || 'pendiente',
      order.fecha_creacion
    ].join(','))
  ].join('\n')
  
  const blob = new Blob([csvContent], { type: 'text/csv' })
  const url = window.URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `pedidos_${new Date().toISOString().split('T')[0]}.csv`
  a.click()
  window.URL.revokeObjectURL(url)
}

const getStatusBadgeClass = (status: string) => {
  const statusClasses: { [key: string]: string } = {
    'pendiente': 'bg-warning',
    'procesando': 'bg-info',
    'enviado': 'bg-primary',
    'entregado': 'bg-success',
    'cancelado': 'bg-danger'
  }
  return statusClasses[status] || 'bg-secondary'
}

// Usar función global de formateo con timezone local
const { $formatDate: formatDate } = useNuxtApp()

// Función para calcular cantidad de productos
const getProductCount = (order: any) => {
  if (order.productos_count) {
    return order.productos_count
  }
  if (order.productos && Array.isArray(order.productos)) {
    return order.productos.reduce((total: number, item: any) => total + (item.cantidad || 0), 0)
  }
  return 0
}

// Lifecycle
onMounted(async () => {
  if (auth.isAuthenticated && auth.isAdmin) {
    await loadOrders()
  }
})
</script>

<style scoped>
.orders-page {
  padding: 2rem 0;
}

.avatar {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: bold;
}

.table th {
  border-top: none;
  font-weight: 600;
  color: var(--bs-gray-700);
}

.table td {
  vertical-align: middle;
}

.btn-group .btn {
  border-radius: 0.375rem;
}

.btn-group .btn:not(:last-child) {
  margin-right: 0.25rem;
}

.order-details {
  font-size: 0.9rem;
}

.modal-content {
  border-radius: 1rem;
  border: 1px solid var(--bs-border-color);
}

.modal-header {
  border-bottom: 1px solid var(--bs-border-color);
}

/* Dark theme adjustments */
.dark-theme .table-light {
  background-color: var(--bs-gray-200) !important;
}

.dark-theme .modal-content {
  background-color: var(--bs-gray-100);
  border-color: var(--bs-border-color);
}

.dark-theme .modal-header {
  border-bottom-color: var(--bs-border-color);
}
</style>














