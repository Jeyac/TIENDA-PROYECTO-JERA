<template>
  <div class="orders-page">
    <div class="container-fluid">
      <!-- Header -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <h1 class="display-6 fw-bold mb-2">
                <i class="bi bi-bag me-2"></i>Historial de Pedidos
              </h1>
              <p class="text-muted mb-0">Gestiona todos los pedidos de los usuarios</p>
            </div>
            <div class="d-flex gap-2">
              <button class="btn btn-outline-secondary" @click="loadOrders">
                <i class="bi bi-arrow-clockwise me-2"></i>Actualizar
              </button>
              <button class="btn btn-outline-success" @click="exportOrders">
                <i class="bi bi-download me-2"></i>Exportar
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
                <div class="col-md-3">
                  <label for="userFilter" class="form-label">Filtrar por Usuario</label>
                  <select
                    v-model="selectedUser"
                    class="form-select"
                    id="userFilter"
                    @change="filterOrders"
                  >
                    <option value="">Todos los usuarios</option>
                    <option v-for="user in users" :key="user.id" :value="user.id">
                      {{ user.username }} ({{ user.email }})
                    </option>
                  </select>
                </div>
                <div class="col-md-3">
                  <label for="statusFilter" class="form-label">Estado del Pedido</label>
                  <select
                    v-model="selectedStatus"
                    class="form-select"
                    id="statusFilter"
                    @change="filterOrders"
                  >
                    <option value="">Todos los estados</option>
                    <option value="pendiente">Pendiente</option>
                    <option value="procesando">Procesando</option>
                    <option value="enviado">Enviado</option>
                    <option value="entregado">Entregado</option>
                    <option value="cancelado">Cancelado</option>
                  </select>
                </div>
                <div class="col-md-3">
                  <label for="dateFrom" class="form-label">Desde</label>
                  <input
                    v-model="dateFrom"
                    type="date"
                    class="form-control"
                    id="dateFrom"
                    @change="filterOrders"
                  >
                </div>
                <div class="col-md-3">
                  <label for="dateTo" class="form-label">Hasta</label>
                  <input
                    v-model="dateTo"
                    type="date"
                    class="form-control"
                    id="dateTo"
                    @change="filterOrders"
                  >
                </div>
              </div>
              <div class="row mt-3">
                <div class="col-12">
                  <button class="btn btn-outline-secondary" @click="clearFilters">
                    <i class="bi bi-x-circle me-2"></i>Limpiar Filtros
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Orders Table -->
      <div class="card border-0 shadow-sm">
        <div class="card-header bg-white border-bottom">
          <div class="row align-items-center">
            <div class="col-md-6">
              <h5 class="card-title mb-0">
                <i class="bi bi-list-ul me-2"></i>Pedidos
                <span class="badge bg-primary ms-2">{{ filteredOrders.length }}</span>
              </h5>
            </div>
            <div class="col-md-6 text-end">
              <small class="text-muted">
                Total: Q {{ totalAmount.toFixed(2) }}
              </small>
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
          
          <div v-else-if="filteredOrders.length === 0" class="text-center py-5">
            <i class="bi bi-bag text-muted" style="font-size: 4rem;"></i>
            <h3 class="text-muted mt-3">No hay pedidos</h3>
            <p class="text-muted">No se encontraron pedidos con los filtros aplicados.</p>
          </div>
          
          <div v-else class="table-responsive">
            <table class="table table-hover mb-0">
              <thead class="table-light">
                <tr>
                  <th>ID</th>
                  <th>Usuario</th>
                  <th>Productos</th>
                  <th>Total</th>
                  <th>Estado</th>
                  <th>Fecha</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="order in filteredOrders" :key="order.id">
                  <td>{{ order.id }}</td>
                  <td>
                    <div class="d-flex align-items-center">
                      <div class="avatar bg-primary text-white rounded-circle me-2">
                        {{ order.usuario_nombre?.charAt(0).toUpperCase() || 'U' }}
                      </div>
                      <div>
                        <strong>{{ order.usuario_nombre || 'Usuario' }}</strong>
                        <br>
                        <small class="text-muted">{{ order.usuario_email || 'Sin email' }}</small>
                      </div>
                    </div>
                  </td>
                  <td>
                    <span class="badge bg-info">{{ order.productos_count || 0 }} productos</span>
                  </td>
                  <td>
                    <strong class="text-primary">Q {{ Number(order.total).toFixed(2) }}</strong>
                  </td>
                  <td>
                    <span class="badge" :class="getStatusBadgeClass(order.estado)">
                      {{ order.estado || 'Pendiente' }}
                    </span>
                  </td>
                  <td>
                    <small>{{ formatDate(order.fecha_creacion) }}</small>
                  </td>
                  <td>
                    <div class="btn-group" role="group">
                      <button class="btn btn-outline-primary btn-sm" @click="viewOrder(order)">
                        <i class="bi bi-eye"></i>
                      </button>
                      <button class="btn btn-outline-success btn-sm" @click="updateStatus(order)">
                        <i class="bi bi-pencil"></i>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Order Details Modal -->
      <div class="modal fade" :class="{ show: showDetailsModal }" :style="{ display: showDetailsModal ? 'block' : 'none' }" tabindex="-1">
        <div class="modal-dialog modal-lg">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">
                <i class="bi bi-bag me-2"></i>Detalles del Pedido #{{ selectedOrder?.id }}
              </h5>
              <button type="button" class="btn-close" @click="showDetailsModal = false"></button>
            </div>
            <div class="modal-body">
              <div v-if="selectedOrder" class="order-details">
                <div class="row mb-3">
                  <div class="col-md-6">
                    <h6>Información del Usuario</h6>
                    <p class="mb-1"><strong>Nombre:</strong> {{ selectedOrder.usuario_nombre }}</p>
                    <p class="mb-1"><strong>Email:</strong> {{ selectedOrder.usuario_email }}</p>
                  </div>
                  <div class="col-md-6">
                    <h6>Información del Pedido</h6>
                    <p class="mb-1"><strong>Estado:</strong> 
                      <span class="badge" :class="getStatusBadgeClass(selectedOrder.estado)">
                        {{ selectedOrder.estado || 'Pendiente' }}
                      </span>
                    </p>
                    <p class="mb-1"><strong>Fecha:</strong> {{ formatDate(selectedOrder.fecha_creacion) }}</p>
                    <p class="mb-1"><strong>Total:</strong> Q {{ Number(selectedOrder.total).toFixed(2) }}</p>
                  </div>
                </div>
                
                <div v-if="selectedOrder.productos && selectedOrder.productos.length > 0">
                  <h6>Productos</h6>
                  <div class="table-responsive">
                    <table class="table table-sm">
                      <thead>
                        <tr>
                          <th>Producto</th>
                          <th>Cantidad</th>
                          <th>Precio</th>
                          <th>Subtotal</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="item in selectedOrder.productos" :key="item.id">
                          <td>{{ item.titulo }}</td>
                          <td>{{ item.cantidad }}</td>
                          <td>Q {{ Number(item.precio).toFixed(2) }}</td>
                          <td>Q {{ Number(item.precio * item.cantidad).toFixed(2) }}</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="showDetailsModal = false">
                Cerrar
              </button>
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
                <i class="bi bi-pencil me-2"></i>Actualizar Estado
              </h5>
              <button type="button" class="btn-close" @click="showStatusModal = false"></button>
            </div>
            <div class="modal-body">
              <div class="mb-3">
                <label for="newStatus" class="form-label">Nuevo Estado</label>
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
              <button type="button" class="btn btn-secondary" @click="showStatusModal = false">
                Cancelar
              </button>
              <button type="button" class="btn btn-primary" @click="confirmStatusUpdate" :disabled="updating">
                <span v-if="updating" class="spinner-border spinner-border-sm me-2"></span>
                {{ updating ? 'Actualizando...' : 'Actualizar' }}
              </button>
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
  middleware: 'admin',
  layout: 'admin'
})

const config = useRuntimeConfig()
const auth = useAuthStore()

// Data
const orders = ref<any[]>([])
const users = ref<any[]>([])
const loading = ref(false)
const updating = ref(false)
const error = ref('')

// Filters
const selectedUser = ref('')
const selectedStatus = ref('')
const dateFrom = ref('')
const dateTo = ref('')

// Modal states
const showDetailsModal = ref(false)
const showStatusModal = ref(false)
const selectedOrder = ref<any>(null)
const newStatus = ref('')

// Computed
const filteredOrders = computed(() => {
  let filtered = orders.value

  if (selectedUser.value) {
    filtered = filtered.filter(order => order.usuario_id === parseInt(selectedUser.value))
  }

  if (selectedStatus.value) {
    filtered = filtered.filter(order => order.estado === selectedStatus.value)
  }

  if (dateFrom.value) {
    const fromDate = new Date(dateFrom.value)
    filtered = filtered.filter(order => new Date(order.fecha_creacion) >= fromDate)
  }

  if (dateTo.value) {
    const toDate = new Date(dateTo.value)
    toDate.setHours(23, 59, 59, 999)
    filtered = filtered.filter(order => new Date(order.fecha_creacion) <= toDate)
  }

  return filtered
})

const totalAmount = computed(() => {
  return filteredOrders.value.reduce((sum, order) => sum + Number(order.total), 0)
})

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
      orders.value = await res.json()
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

const filterOrders = () => {
  // Filtering is handled by computed property
}

const clearFilters = () => {
  selectedUser.value = ''
  selectedStatus.value = ''
  dateFrom.value = ''
  dateTo.value = ''
}

const viewOrder = (order: any) => {
  selectedOrder.value = order
  showDetailsModal.value = true
}

const updateStatus = (order: any) => {
  selectedOrder.value = order
  newStatus.value = order.estado || 'pendiente'
  showStatusModal.value = true
}

const confirmStatusUpdate = async () => {
  if (!selectedOrder.value) return
  
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

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString()
}

// Lifecycle
onMounted(async () => {
  if (auth.isAuthenticated && auth.isAdmin) {
    await Promise.all([
      loadOrders(),
      loadUsers()
    ])
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
