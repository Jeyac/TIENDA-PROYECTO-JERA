<template>
  <div class="products-page">
    <div class="container-fluid">
      <!-- Header -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <h1 class="display-6 fw-bold mb-2">
                <i class="bi bi-box me-2"></i>Gestión de Productos
              </h1>
              <p class="text-muted mb-0">Administra el catálogo de productos</p>
            </div>
            <button class="btn btn-primary" @click="showCreateModal = true">
              <i class="bi bi-plus-circle me-2"></i>Nuevo Producto
            </button>
          </div>
        </div>
      </div>

      <!-- Products Table -->
      <div class="card border-0 shadow-sm">
        <div class="card-header bg-white border-bottom">
          <div class="row align-items-center">
            <div class="col-md-6">
              <h5 class="card-title mb-0">
                <i class="bi bi-list-ul me-2"></i>Lista de Productos
              </h5>
            </div>
            <div class="col-md-6">
              <div class="input-group">
                <input
                  v-model="searchQuery"
                  type="text"
                  class="form-control"
                  placeholder="Buscar productos..."
                  @input="filterProducts"
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
            <p class="text-muted mt-3">Cargando productos...</p>
          </div>
          
          <div v-else-if="filteredProducts.length === 0" class="text-center py-5">
            <i class="bi bi-box text-muted" style="font-size: 4rem;"></i>
            <h3 class="text-muted mt-3">No hay productos</h3>
            <p class="text-muted">Comienza agregando el primer producto.</p>
          </div>
          
          <div v-else class="table-responsive">
            <table class="table table-hover mb-0">
              <thead class="table-light">
                <tr>
                  <th>ID</th>
                  <th>Imagen</th>
                  <th>Título</th>
                  <th>Categoría</th>
                  <th>Precio</th>
                  <th>Estado</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="product in filteredProducts" :key="product.id">
                  <td>{{ product.id }}</td>
                  <td>
                    <div class="product-image">
                      <img 
                        v-if="product.imagen_url" 
                        :src="product.imagen_url" 
                        :alt="product.titulo"
                        class="img-thumbnail"
                        style="width: 50px; height: 50px; object-fit: cover;"
                      >
                      <div v-else class="placeholder-image">
                        <i class="bi bi-image"></i>
                      </div>
                    </div>
                  </td>
                  <td>
                    <div>
                      <strong>{{ product.titulo }}</strong>
                      <br>
                      <small class="text-muted">{{ product.descripcion.substring(0, 50) }}...</small>
                    </div>
                  </td>
                  <td>
                    <span class="badge bg-secondary">{{ product.categoria_nombre || 'Sin categoría' }}</span>
                  </td>
                  <td>
                    <strong class="text-primary">Q {{ Number(product.precio).toFixed(2) }}</strong>
                  </td>
                  <td>
                    <span class="badge" :class="product.activo ? 'bg-success' : 'bg-danger'">
                      {{ product.activo ? 'Activo' : 'Inactivo' }}
                    </span>
                  </td>
                  <td>
                    <div class="btn-group" role="group">
                      <button class="btn btn-outline-primary btn-sm" @click="editProduct(product)">
                        <i class="bi bi-pencil"></i>
                      </button>
                      <button class="btn btn-outline-danger btn-sm" @click="deleteProduct(product)">
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

      <!-- Create/Edit Product Modal -->
      <div class="modal fade" :class="{ show: showCreateModal || showEditModal }" :style="{ display: (showCreateModal || showEditModal) ? 'block' : 'none' }" tabindex="-1">
        <div class="modal-dialog modal-xl">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">
                <i class="bi bi-box me-2"></i>
                {{ editingProduct ? 'Editar Producto' : 'Nuevo Producto' }}
              </h5>
              <button type="button" class="btn-close" @click="closeModal"></button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="saveProduct">
                <div class="row g-3">
                  <div class="col-md-6">
                    <label for="titulo" class="form-label">Título del Producto</label>
                    <input
                      v-model="productForm.titulo"
                      type="text"
                      class="form-control"
                      id="titulo"
                      required
                      :disabled="saving"
                    >
                  </div>
                  <div class="col-md-6">
                    <label for="precio" class="form-label">Precio (Q)</label>
                    <input
                      v-model="productForm.precio"
                      type="number"
                      step="0.01"
                      min="0"
                      class="form-control"
                      id="precio"
                      required
                      :disabled="saving"
                    >
                  </div>
                  <div class="col-md-6">
                    <label for="categoria" class="form-label">Categoría</label>
                    <input
                      v-model="productForm.categoria_nombre"
                      type="text"
                      class="form-control"
                      id="categoria"
                      list="categorias-list"
                      placeholder="Escribe o selecciona una categoría"
                      required
                      :disabled="saving"
                    >
                    <datalist id="categorias-list">
                      <option v-for="category in categories" :key="category.id" :value="category.nombre"></option>
                    </datalist>
                  </div>
                  <div class="col-md-6">
                    <label for="imagen_url" class="form-label">URL de Imagen</label>
                    <input
                      v-model="productForm.imagen_url"
                      type="url"
                      class="form-control"
                      id="imagen_url"
                      placeholder="https://ejemplo.com/imagen.jpg"
                      :disabled="saving"
                    >
                  </div>
                  <div class="col-12">
                    <label for="descripcion" class="form-label">Descripción</label>
                    <textarea
                      v-model="productForm.descripcion"
                      class="form-control"
                      id="descripcion"
                      rows="3"
                      :disabled="saving"
                    ></textarea>
                  </div>
                  <div class="col-md-6">
                    <div class="form-check form-switch">
                      <input
                        v-model="productForm.activo"
                        class="form-check-input"
                        type="checkbox"
                        id="activo"
                        :disabled="saving"
                      >
                      <label class="form-check-label" for="activo">
                        Producto Activo
                      </label>
                    </div>
                  </div>
                </div>
                
                <!-- Image Preview -->
                <div v-if="productForm.imagen_url" class="mt-3">
                  <label class="form-label">Vista Previa</label>
                  <div class="image-preview">
                    <img 
                      :src="productForm.imagen_url" 
                      :alt="productForm.titulo"
                      class="img-fluid rounded"
                      style="max-height: 200px;"
                      @error="imageError = true"
                    >
                    <div v-if="imageError" class="image-error">
                      <i class="bi bi-exclamation-triangle"></i>
                      <p>Error al cargar la imagen</p>
                    </div>
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
              <p>¿Estás seguro de que deseas eliminar el producto <strong>{{ productToDelete?.titulo }}</strong>?</p>
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
const products = ref<any[]>([])
const categories = ref<any[]>([])
const searchQuery = ref('')
const loading = ref(false)
const saving = ref(false)
const deleting = ref(false)
const error = ref('')
const imageError = ref(false)

// Modal states
const showCreateModal = ref(false)
const showEditModal = ref(false)
const showDeleteModal = ref(false)
const editingProduct = ref<any>(null)
const productToDelete = ref<any>(null)

// Form data
const productForm = reactive({
  titulo: '',
  descripcion: '',
  precio: '',
  categoria_nombre: '',
  imagen_url: '',
  activo: true
})

// Computed
const filteredProducts = computed(() => {
  if (!searchQuery.value) return products.value
  
  const query = searchQuery.value.toLowerCase()
  return products.value.filter(product => 
    product.titulo.toLowerCase().includes(query) ||
    product.descripcion.toLowerCase().includes(query) ||
    (product.categoria_nombre && product.categoria_nombre.toLowerCase().includes(query))
  )
})

// Methods
const loadProducts = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const res = await fetch(`${config.public.apiBase}/api/productos/?all=1`, {
      headers: {
        'Authorization': `Bearer ${auth.token}`
      }
    })
    
    if (res.ok) {
      products.value = await res.json()
    } else if (res.status === 401) {
      await auth.logout()
    } else {
      throw new Error('Error al cargar productos')
    }
  } catch (err: any) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

const loadCategories = async () => {
  try {
    const res = await fetch(`${config.public.apiBase}/api/categorias/`)
    if (res.ok) {
      categories.value = await res.json()
    }
  } catch (err) {
    console.error('Error cargando categorías:', err)
  }
}

const filterProducts = () => {
  // Filtering is handled by computed property
}

const editProduct = (product: any) => {
  editingProduct.value = product
  productForm.titulo = product.titulo
  productForm.descripcion = product.descripcion
  productForm.precio = product.precio.toString()
  productForm.categoria_nombre = product.categoria_nombre || ''
  productForm.imagen_url = product.imagen_url || ''
  productForm.activo = Boolean(product.activo)
  imageError.value = false
  showEditModal.value = true
}

const deleteProduct = (product: any) => {
  productToDelete.value = product
  showDeleteModal.value = true
}

const saveProduct = async () => {
  saving.value = true
  error.value = ''
  imageError.value = false
  
  try {
    const url = editingProduct.value 
      ? `${config.public.apiBase}/api/productos/${editingProduct.value.id}`
      : `${config.public.apiBase}/api/productos/`
    
    const method = editingProduct.value ? 'PUT' : 'POST'
    
    const body = {
      titulo: productForm.titulo,
      descripcion: productForm.descripcion,
      precio: parseFloat(productForm.precio),
      categoria_nombre: productForm.categoria_nombre,
      imagen_url: productForm.imagen_url,
      activo: productForm.activo
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
      await loadProducts()
      closeModal()
    } else if (res.status === 401) {
      await auth.logout()
    } else {
      const data = await res.json()
      throw new Error(data.error || data.message || 'Error al guardar producto')
    }
  } catch (err: any) {
    error.value = err.message
  } finally {
    saving.value = false
  }
}

const confirmDelete = async () => {
  if (!productToDelete.value) return
  
  deleting.value = true
  
  try {
    const res = await fetch(`${config.public.apiBase}/api/productos/${productToDelete.value.id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${auth.token}`
      }
    })
    
    if (res.ok) {
      await loadProducts()
      showDeleteModal.value = false
      productToDelete.value = null
    } else if (res.status === 401) {
      await auth.logout()
    } else {
      throw new Error('Error al eliminar producto')
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
  editingProduct.value = null
  productForm.titulo = ''
  productForm.descripcion = ''
  productForm.precio = ''
  productForm.categoria_nombre = ''
  productForm.imagen_url = ''
  productForm.activo = true
  error.value = ''
  imageError.value = false
}

// Lifecycle
onMounted(async () => {
  if (auth.isAuthenticated && auth.isAdmin) {
    await Promise.all([
      loadProducts(),
      loadCategories()
    ])
  }
})
</script>

<style scoped>
.products-page {
  padding: 2rem 0;
}

.product-image {
  width: 50px;
  height: 50px;
}

.placeholder-image {
  width: 50px;
  height: 50px;
  background: var(--bs-gray-200);
  border-radius: 0.375rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--bs-gray-500);
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

.image-preview {
  position: relative;
  display: inline-block;
}

.image-error {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: var(--bs-gray-200);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: var(--bs-gray-500);
  border-radius: 0.375rem;
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

.dark-theme .placeholder-image {
  background-color: var(--bs-gray-300);
}

.dark-theme .image-error {
  background-color: var(--bs-gray-300);
}
</style>
