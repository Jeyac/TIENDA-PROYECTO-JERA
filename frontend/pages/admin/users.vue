<template>
  <div class="users-page">
    <div class="container-fluid">
      <!-- Header -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <h1 class="display-6 fw-bold mb-2">
                <i class="bi bi-people me-2"></i>Gestión de Usuarios
              </h1>
              <p class="text-muted mb-0">Administra los usuarios del sistema</p>
            </div>
            <button class="btn btn-primary" @click="showCreateModal = true">
              <i class="bi bi-person-plus me-2"></i>Nuevo Usuario
            </button>
          </div>
        </div>
      </div>

      <!-- Users Table -->
      <div class="card border-0 shadow-sm">
        <div class="card-header bg-white border-bottom">
          <div class="row align-items-center">
            <div class="col-md-6">
              <h5 class="card-title mb-0">
                <i class="bi bi-list-ul me-2"></i>Lista de Usuarios
              </h5>
            </div>
            <div class="col-md-6">
              <div class="input-group">
                <input
                  v-model="searchQuery"
                  type="text"
                  class="form-control"
                  placeholder="Buscar usuarios..."
                  @input="filterUsers"
                >
                <button class="btn btn-outline-secondary" type="button">
                  <i class="bi bi-search"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
        <div class="card-body p-0">
          <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Cargando...</span>
            </div>
            <p class="text-muted mt-3">Cargando usuarios...</p>
          </div>
          
          <div v-else-if="filteredUsers.length === 0" class="text-center py-5">
            <i class="bi bi-people text-muted" style="font-size: 4rem;"></i>
            <h3 class="text-muted mt-3">No hay usuarios</h3>
            <p class="text-muted">Comienza agregando el primer usuario.</p>
          </div>
          
          <div v-else class="table-responsive">
            <table class="table table-hover mb-0">
              <thead class="table-light">
                <tr>
                  <th>ID</th>
                  <th>Usuario</th>
                  <th>Email</th>
                  <th>Rol</th>
                  <th>Fecha Registro</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="user in filteredUsers" :key="user.id">
                  <td>{{ user.id }}</td>
                  <td>
                    <div class="d-flex align-items-center">
                      <div class="avatar bg-primary text-white rounded-circle me-2">
                        {{ user.username.charAt(0).toUpperCase() }}
                      </div>
                      <strong>{{ user.username }}</strong>
                    </div>
                  </td>
                  <td>{{ user.email }}</td>
                  <td>
                    <span class="badge" :class="getRoleBadgeClass(user.rol)">
                      {{ user.rol }}
                    </span>
                  </td>
                  <td>{{ formatDate(user.fecha_registro) }}</td>
                  <td>
                    <div class="btn-group" role="group">
                      <button class="btn btn-outline-primary btn-sm" @click="editUser(user)">
                        <i class="bi bi-pencil"></i>
                      </button>
                      <button class="btn btn-outline-danger btn-sm" @click="deleteUser(user)">
                        <i class="bi bi-trash"></i>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Create/Edit User Modal -->
      <div class="modal fade" :class="{ show: showCreateModal || showEditModal }" :style="{ display: (showCreateModal || showEditModal) ? 'block' : 'none' }" tabindex="-1">
        <div class="modal-dialog modal-lg">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">
                <i class="bi bi-person me-2"></i>
                {{ editingUser ? 'Editar Usuario' : 'Nuevo Usuario' }}
              </h5>
              <button type="button" class="btn-close" @click="closeModal"></button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="saveUser">
                <div class="row g-3">
                  <div class="col-md-6">
                    <label for="username" class="form-label">Nombre de Usuario</label>
                    <input
                      v-model="userForm.username"
                      type="text"
                      class="form-control"
                      id="username"
                      required
                      :disabled="saving"
                    >
                  </div>
                  <div class="col-md-6">
                    <label for="email" class="form-label">Email</label>
                    <input
                      v-model="userForm.email"
                      type="email"
                      class="form-control"
                      id="email"
                      required
                      :disabled="saving"
                    >
                  </div>
                  <div class="col-md-6">
                    <label for="password" class="form-label">
                      Contraseña
                      <small class="text-muted">(dejar vacío para mantener actual)</small>
                    </label>
                    <input
                      v-model="userForm.password"
                      type="password"
                      class="form-control"
                      id="password"
                      :required="!editingUser"
                      :disabled="saving"
                    >
                  </div>
                  <div class="col-md-6">
                    <label for="rol" class="form-label">Rol</label>
                    <select
                      v-model="userForm.rol"
                      class="form-select"
                      id="rol"
                      required
                      :disabled="saving"
                    >
                      <option value="cliente">Cliente</option>
                      <option value="administrador">Administrador</option>
                    </select>
                  </div>
                </div>
                
                <div v-if="error" class="alert alert-danger mt-3">
                  <i class="bi bi-exclamation-triangle me-2"></i>{{ error }}
                </div>
                
                <div class="modal-footer">
                  <button type="button" class="btn btn-secondary" @click="closeModal" :disabled="saving">
                    Cancelar
                  </button>
                  <button type="submit" class="btn btn-primary" :disabled="saving">
                    <span v-if="saving" class="spinner-border spinner-border-sm me-2"></span>
                    {{ saving ? 'Guardando...' : 'Guardar' }}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
      <div v-if="showCreateModal || showEditModal" class="modal-backdrop fade show"></div>

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
              <p>¿Estás seguro de que deseas eliminar al usuario <strong>{{ userToDelete?.username }}</strong>?</p>
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
const users = ref<any[]>([])
const searchQuery = ref('')
const loading = ref(false)
const saving = ref(false)
const deleting = ref(false)
const error = ref('')

// Modal states
const showCreateModal = ref(false)
const showEditModal = ref(false)
const showDeleteModal = ref(false)
const editingUser = ref<any>(null)
const userToDelete = ref<any>(null)

// Form data
const userForm = reactive({
  username: '',
  email: '',
  password: '',
  rol: 'cliente'
})

// Computed
const filteredUsers = computed(() => {
  if (!searchQuery.value) return users.value
  
  const query = searchQuery.value.toLowerCase()
  return users.value.filter(user => 
    user.username.toLowerCase().includes(query) ||
    user.email.toLowerCase().includes(query) ||
    user.rol.toLowerCase().includes(query)
  )
})

// Methods
const loadUsers = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const res = await fetch(`${config.public.apiBase}/api/admin/usuarios/`, {
      headers: {
        'Authorization': `Bearer ${auth.token}`
      }
    })
    
    if (res.ok) {
      users.value = await res.json()
    } else if (res.status === 401) {
      await auth.logout()
    } else {
      throw new Error('Error al cargar usuarios')
    }
  } catch (err: any) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

const filterUsers = () => {
  // Filtering is handled by computed property
}

const editUser = (user: any) => {
  editingUser.value = user
  userForm.username = user.username
  userForm.email = user.email
  userForm.password = ''
  userForm.rol = user.rol
  showEditModal.value = true
}

const deleteUser = (user: any) => {
  userToDelete.value = user
  showDeleteModal.value = true
}

const saveUser = async () => {
  saving.value = true
  error.value = ''
  
  try {
    const url = editingUser.value 
      ? `${config.public.apiBase}/api/admin/usuarios/${editingUser.value.id}`
      : `${config.public.apiBase}/api/admin/usuarios/`
    
    const method = editingUser.value ? 'PUT' : 'POST'
    
    const body: any = {
      username: userForm.username,
      email: userForm.email,
      rol: userForm.rol
    }
    
    if (userForm.password) {
      body.password = userForm.password
    }
    
    const res = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${auth.token}`
      },
      body: JSON.stringify(body)
    })
    
    if (res.ok) {
      await loadUsers()
      closeModal()
    } else if (res.status === 401) {
      await auth.logout()
    } else {
      const data = await res.json()
      throw new Error(data.error || data.message || 'Error al guardar usuario')
    }
  } catch (err: any) {
    error.value = err.message
  } finally {
    saving.value = false
  }
}

const confirmDelete = async () => {
  if (!userToDelete.value) return
  
  deleting.value = true
  
  try {
    const res = await fetch(`${config.public.apiBase}/api/admin/usuarios/${userToDelete.value.id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${auth.token}`
      }
    })
    
    if (res.ok) {
      await loadUsers()
      showDeleteModal.value = false
      userToDelete.value = null
    } else if (res.status === 401) {
      await auth.logout()
    } else {
      throw new Error('Error al eliminar usuario')
    }
  } catch (err: any) {
    error.value = err.message
  } finally {
    deleting.value = false
  }
}

const closeModal = () => {
  showCreateModal.value = false
  showEditModal.value = false
  editingUser.value = null
  userForm.username = ''
  userForm.email = ''
  userForm.password = ''
  userForm.rol = 'cliente'
  error.value = ''
}

const getRoleBadgeClass = (rol: string) => {
  return rol === 'administrador' ? 'bg-danger' : 'bg-primary'
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString()
}

// Lifecycle
onMounted(() => {
  if (auth.isAuthenticated && auth.isAdmin) {
    loadUsers()
  }
})
</script>

<style scoped>
.users-page {
  padding: 2rem 0;
}

.avatar {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.875rem;
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
