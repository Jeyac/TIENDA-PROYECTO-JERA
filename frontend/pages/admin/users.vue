<template>
  <div class="users-page">
    <div class="container-fluid">
      <!-- Header -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <h1 class="display-6 fw-bold mb-2">
                <i class="bi bi-people me-2"></i>Gestión de usuarios
              </h1>
              <p class="text-muted mb-0">Administra los usuarios del sistema</p>
            </div>
            <BaseButton variant="primary" @click="showCreateModal = true">
              <i class="bi bi-person-plus me-2"></i>Nuevo usuario
            </BaseButton>
          </div>
        </div>
      </div>

      <!-- Users Table -->
      <div class="card border-0 shadow-sm">
        <div class="card-header bg-white border-bottom">
          <SectionTitle>
            <template #default>
              <i class="bi bi-list-ul me-2"></i>Lista de usuarios
            </template>
            <template #actions>
              <FilterBar v-model="searchQuery" placeholder="Buscar usuarios..." @search="filterUsers" @clear="() => { searchQuery = ''; filterUsers() }" />
            </template>
          </SectionTitle>
        </div>
        <div class="card-body p-0">
          <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Cargando...</span>
            </div>
            <p class="text-muted mt-3">Cargando usuarios...</p>
          </div>
          
          <div v-else>
            <DataTable
              :items="filteredUsers"
              :columns="[
                { key: 'id', label: 'ID' },
                { key: 'usuario', label: 'Usuario' },
                { key: 'email', label: 'Email' },
                { key: 'rol', label: 'Rol' },
                { key: 'estado', label: 'Estado' },
                { key: 'acciones', label: 'Acciones' }
              ]"
              empty-icon="bi bi-people"
              empty-title="No hay usuarios"
              empty-subtitle="Comienza agregando el primer usuario."
            >
              <template #row="{ row: user }">
                <td>{{ user.id }}</td>
                <td>
                  <div class="d-flex align-items-center">
                    <AvatarCircle :text="user.username" size="sm" class="me-2" />
                    <strong>{{ user.username }}</strong>
                  </div>
                </td>
                <td>{{ user.email }}</td>
                <td>
                  <span class="badge" :class="getRoleBadgeClass(user.rol)">
                    {{ formatRoleName(user.rol) }}
                  </span>
                </td>
                <td>
                  <StatusBadge :status="user.activo ? 'activo' : 'inactivo'" />
                </td>
                <td>
                  <div class="btn-group" role="group">
                    <BaseButton variant="outline-primary" class="btn-sm" @click="editUser(user)">
                      <i class="bi bi-pencil"></i>
                    </BaseButton>
                  </div>
                </td>
              </template>
            </DataTable>
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
                    <label for="username" class="form-label">Nombre de usuario</label>
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
                    <div class="input-group">
                      <input
                        v-model="userForm.password"
                        :type="showPassword ? 'text' : 'password'"
                        class="form-control"
                        id="password"
                        :required="!editingUser"
                        :disabled="saving"
                      >
                      <button
                        type="button"
                        class="btn btn-outline-secondary"
                        @click="togglePasswordVisibility"
                        :disabled="saving"
                      >
                        <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
                      </button>
                    </div>
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
                      <option value="atencion_cliente">Atención al cliente</option>
                    </select>
                  </div>
                  
                  <div class="col-12" v-if="editingUser">
                    <div class="form-check">
                      <input
                        v-model="userForm.activo"
                        class="form-check-input"
                        type="checkbox"
                        id="activo"
                        :disabled="saving"
                      >
                      <label class="form-check-label" for="activo">
                        Usuario activo
                      </label>
                    </div>
                  </div>
                </div>
                
                <div v-if="error" class="alert alert-danger mt-3">
                  <i class="bi bi-exclamation-triangle me-2"></i>{{ error }}
                </div>
                
                <div class="modal-footer">
                  <BaseButton variant="secondary" @click="closeModal" :disabled="saving">
                    Cancelar
                  </BaseButton>
                  <BaseButton variant="primary" type="submit" :loading="saving" :disabled="saving">
                    {{ saving ? 'Guardando...' : 'Guardar' }}
                  </BaseButton>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
      <div v-if="showCreateModal || showEditModal" class="modal-backdrop fade show"></div>

      <!-- Delete Confirmation Modal -->
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

const { apiRequest } = useApi()
const auth = useAuthStore()

// Data
const users = ref<any[]>([])
const searchQuery = ref('')
const loading = ref(false)
const saving = ref(false)
const error = ref('')

// Modal states
const showCreateModal = ref(false)
const showEditModal = ref(false)
const editingUser = ref<any>(null)
const showPassword = ref(false)

// Form data
const userForm = reactive({
  username: '',
  email: '',
  password: '',
  rol: 'cliente',
  activo: true
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
    const res = await apiRequest('/api/admin/usuarios/')
    
    if (res.ok) {
      users.value = await res.json()
    } else {
      throw new Error('Error al cargar usuarios')
    }
  } catch (err: any) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value
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
  userForm.activo = user.activo
  showEditModal.value = true
}


const saveUser = async () => {
  saving.value = true
  error.value = ''
  
  try {
    const url = editingUser.value 
      ? `/api/admin/usuarios/${editingUser.value.id}`
      : `/api/admin/usuarios/`
    
    const method = editingUser.value ? 'PUT' : 'POST'
    
    const body: any = {
      username: userForm.username,
      email: userForm.email,
      rol: userForm.rol
    }
    
    if (userForm.password) {
      body.password = userForm.password
    }
    
    // Solo enviar activo si estamos editando un usuario existente
    if (editingUser.value) {
      body.activo = userForm.activo
    }
    
    console.log('Enviando datos del usuario:', body)
    
    const res = await apiRequest(url, {
      method,
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(body)
    })
    
    if (res.ok) {
      await loadUsers()
      closeModal()
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


const closeModal = () => {
  showCreateModal.value = false
  showEditModal.value = false
  editingUser.value = null
  showPassword.value = false
  userForm.username = ''
  userForm.email = ''
  userForm.password = ''
  userForm.rol = 'cliente'
  userForm.activo = true
  error.value = ''
}

const getRoleBadgeClass = (rol: string) => {
  switch (rol) {
    case 'administrador':
      return 'bg-danger'
    case 'atencion_cliente':
      return 'bg-warning'
    case 'cliente':
      return 'bg-primary'
    default:
      return 'bg-secondary'
  }
}

const formatRoleName = (rol: string) => {
  switch (rol) {
    case 'administrador':
      return 'Administrador'
    case 'atencion_cliente':
      return 'Atención al Cliente'
    case 'cliente':
      return 'Cliente'
    default:
      return rol
  }
}

// Usar función global de formateo
const { $formatDate: formatDate } = useNuxtApp()

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
