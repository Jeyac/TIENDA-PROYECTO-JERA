<template>
  <div class="admin-products-page">
    <!-- Header Section -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h2 class="mb-1">Gestión de productos</h2>
        <p class="text-muted mb-0">Administra el catálogo de productos de la tienda</p>
      </div>
      <BaseButton variant="primary" @click="showAddModal = true">
        <i class="bi bi-plus-circle me-2"></i>Agregar producto
      </BaseButton>
    </div>

    <!-- Filters and Search -->
    <div class="card mb-4">
      <div class="card-body">
        <div class="row g-3">
          <div class="col-md-4">
            <SearchBar v-model="searchQuery" placeholder="Buscar productos..." />
          </div>
          <div class="col-md-3">
            <select v-model="selectedCategory" class="form-select">
              <option value="">Todas las categorías</option>
              <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                {{ cat.nombre }}
              </option>
            </select>
          </div>
          <div class="col-md-3">
            <select v-model="statusFilter" class="form-select">
              <option value="">Todos los estados</option>
              <option value="activo">Activos</option>
              <option value="inactivo">Inactivos</option>
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

    <!-- Products Table -->
    <div class="card">
      <div class="card-body p-0">
        <div v-if="loading" class="text-center py-5">
          <InlineSpinner />
          <p class="text-muted mt-2">Cargando productos...</p>
        </div>

        <div v-else-if="filteredProducts.length === 0" class="text-center py-5">
          <EmptyState 
            icon="bi-box" 
            title="No hay productos" 
            description="No se encontraron productos con los filtros aplicados"
            size="lg"
          />
        </div>

        <div v-else class="table-responsive">
          <table class="table table-hover mb-0">
            <thead class="table-light">
              <tr>
                <th>Imagen</th>
                <th>Producto</th>
                <th>Categoría</th>
                <th>Precio</th>
                <th>Stock</th>
                <th>Pedidos</th>
                <th>Estado</th>
                <th class="text-center">Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="product in paginatedProducts" :key="product.id">
                <td>
                  <div class="product-image-container">
                    <img 
                      v-if="product.imagen_url" 
                      :src="product.imagen_url" 
                      :alt="product.titulo"
                      class="product-thumb"
                      @error="handleImageError"
                    />
                    <div v-else class="product-placeholder">
                      <i class="bi bi-image text-muted"></i>
                    </div>
                  </div>
                </td>
                <td>
                  <div>
                    <h6 class="mb-1">{{ product.titulo }}</h6>
                    <p class="text-muted small mb-0">{{ product.descripcion?.substring(0, 50) }}...</p>
                  </div>
                </td>
                <td>
                  <span class="badge bg-secondary">{{ getCategoryName(product.categoria_id) }}</span>
                </td>
                <td>
                  <span class="fw-bold text-primary">Q {{ Number(product.precio).toFixed(2) }}</span>
                </td>
                <td>
                  <span :class="product.stock > 10 ? 'text-success' : product.stock > 0 ? 'text-warning' : 'text-danger'">
                    {{ product.stock }}
                  </span>
                </td>
                <td>
                  <span class="badge bg-info">
                    {{ product.cantidad_pedida || 0 }}
                  </span>
                </td>
                <td>
                  <StatusBadge :status="product.activo ? 'activo' : 'inactivo'" />
                </td>
                <td class="text-center">
                  <div class="btn-group btn-group-sm">
                    <BaseButton variant="outline-primary" @click="editProduct(product)" title="Editar">
                      <i class="bi bi-pencil"></i>
                    </BaseButton>
                    <BaseButton variant="outline-danger" @click="deleteProduct(product)" title="Eliminar">
                      <i class="bi bi-trash"></i>
                    </BaseButton>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div v-if="filteredProducts.length > itemsPerPage" class="card-footer">
          <Paginator 
            v-model="currentPage" 
            :total-items="filteredProducts.length" 
            :items-per-page="itemsPerPage"
          />
        </div>
      </div>
    </div>

    <!-- Add/Edit Product Modal -->
    <div class="modal fade" :class="{ show: showAddModal || showEditModal }" :style="{ display: (showAddModal || showEditModal) ? 'block' : 'none' }" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              {{ editingProduct ? 'Editar Producto' : 'Agregar Producto' }}
            </h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <form>
              <div class="row g-3">
                <div class="col-md-6">
                  <label class="form-label">Título *</label>
                  <input 
                    v-model="productForm.titulo" 
                    type="text" 
                    class="form-control" 
                    required 
                    maxlength="100"
                  />
                </div>
                <div class="col-md-6">
                  <label class="form-label">Categoría *</label>
                  <div class="position-relative">
                    <input 
                      v-model="productForm.categoria_nombre" 
                      type="text" 
                      class="form-control" 
                      list="categorias-list"
                      placeholder="Escribir o seleccionar categoría"
                      required
                      @input="handleCategoryInput"
                    />
                    <datalist id="categorias-list">
                      <option v-for="cat in categories" :key="cat.id" :value="cat.nombre">
                        {{ cat.nombre }}
                      </option>
                    </datalist>
                    <div v-if="categorySuggestions.length > 0" class="dropdown-menu show w-100" style="position: absolute; top: 100%; z-index: 1000;">
                      <button 
                        v-for="suggestion in categorySuggestions" 
                        :key="suggestion.id"
                        type="button"
                        class="dropdown-item"
                        @click="selectCategory(suggestion)"
                      >
                        {{ suggestion.nombre }}
                      </button>
                    </div>
                  </div>
                </div>
                <div class="col-12">
                  <label class="form-label">Descripción *</label>
                  <textarea 
                    v-model="productForm.descripcion" 
                    class="form-control" 
                    rows="3" 
                    required 
                    maxlength="500"
                  ></textarea>
                </div>
                <div class="col-md-4">
                  <label class="form-label">Precio *</label>
                  <div class="input-group">
                    <span class="input-group-text">Q</span>
                    <input 
                      v-model.number="productForm.precio" 
                      type="number" 
                      step="0.01" 
                      min="0" 
                      class="form-control" 
                      required 
                    />
                  </div>
                </div>
                <div class="col-md-4">
                  <label class="form-label">Stock *</label>
                  <input 
                    v-model.number="productForm.stock" 
                    type="number" 
                    min="0" 
                    class="form-control" 
                    required 
                  />
                </div>
                <div class="col-md-4">
                  <label class="form-label">Estado</label>
                  <select v-model="productForm.activo" class="form-select">
                    <option :value="true">Activo</option>
                    <option :value="false">Inactivo</option>
                  </select>
                </div>
                <div class="col-12">
                  <label class="form-label">Imagen</label>
                  <div class="mb-3">
                    <div class="btn-group w-100" role="group">
                      <input type="radio" class="btn-check" name="imageType" id="imageFile" value="file" v-model="imageType">
                      <label class="btn btn-outline-primary" for="imageFile">Subir archivo</label>
                      
                      <input type="radio" class="btn-check" name="imageType" id="imageUrl" value="url" v-model="imageType">
                      <label class="btn btn-outline-primary" for="imageUrl">URL de imagen</label>
                    </div>
                  </div>
                  
                  <!-- Subir archivo -->
                  <div v-if="imageType === 'file'">
                    <input 
                      ref="imageInput"
                      type="file" 
                      class="form-control" 
                      accept="image/*"
                      @change="handleImageUpload"
                    />
                  </div>
                  
                  <!-- URL de imagen -->
                  <div v-if="imageType === 'url'">
                    <input 
                      v-model="productForm.imagen_url"
                      type="url" 
                      class="form-control" 
                      placeholder="https://ejemplo.com/imagen.jpg"
                    />
                  </div>
                  
                  <div v-if="productForm.imagen_url" class="mt-2">
                    <div class="text-center">
                      <p class="small text-muted mb-2">Vista previa:</p>
                      <img :src="productForm.imagen_url" alt="Preview" class="img-thumbnail" style="max-width: 200px; max-height: 200px; object-fit: cover;" />
                    </div>
                  </div>
                </div>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <BaseButton variant="secondary" @click="closeModal">Cancelar</BaseButton>
            <BaseButton variant="primary" @click="saveProduct" :disabled="saving">
              <InlineSpinner v-if="saving" size="sm" class="me-2" />
              {{ editingProduct ? 'Actualizar' : 'Crear' }}
            </BaseButton>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <ConfirmModal 
      v-model="showDeleteModal"
      title="Eliminar Producto"
      :message="`¿Estás seguro de que quieres eliminar el producto '${productToDelete?.titulo}'?`"
      confirm-text="Eliminar"
      variant="danger"
      @confirm="confirmDelete"
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
  middleware: ['auth', 'admin'],
  layout: 'admin'
})

// Stores
const auth = useAuthStore()

// Reactive data
const products = ref<any[]>([])
const categories = ref<any[]>([])
const loading = ref(false)
const saving = ref(false)
const error = ref('')
const categorySuggestions = ref<any[]>([])

// Form data
const productForm = ref({
  titulo: '',
  descripcion: '',
  precio: 0,
  stock: 0,
  categoria_id: '',
  categoria_nombre: '',
  activo: true,
  imagen_url: ''
})

// Modal states
const showAddModal = ref(false)
const showEditModal = ref(false)
const showDeleteModal = ref(false)
const editingProduct = ref<any>(null)
const productToDelete = ref<any>(null)
const imageType = ref('file')

// Filters and pagination
const searchQuery = ref('')
const selectedCategory = ref('')
const statusFilter = ref('')
const currentPage = ref(1)
const itemsPerPage = 10

// Computed properties
const filteredProducts = computed(() => {
  let filtered = products.value

  // Search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(p => 
      p.titulo.toLowerCase().includes(query) ||
      p.descripcion.toLowerCase().includes(query)
    )
  }

  // Category filter
  if (selectedCategory.value) {
    filtered = filtered.filter(p => p.categoria_id === selectedCategory.value)
  }

  // Status filter
  if (statusFilter.value) {
    const isActive = statusFilter.value === 'activo'
    filtered = filtered.filter(p => p.activo === isActive)
  }

  return filtered
})

const paginatedProducts = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredProducts.value.slice(start, end)
})

// Methods
const loadProducts = async () => {
  loading.value = true
  try {
    const response = await auth.makeAuthenticatedRequest('/api/productos?all=1')
    if (response.ok) {
      products.value = await response.json()
    } else {
      throw new Error('Error al cargar productos')
    }
  } catch (err: any) {
    error.value = err.message || 'Error al cargar productos'
  } finally {
    loading.value = false
  }
}

const loadCategories = async () => {
  try {
    const response = await auth.makeAuthenticatedRequest('/api/categorias')
    if (response.ok) {
      categories.value = await response.json()
    }
  } catch (err) {
    console.error('Error al cargar categorías:', err)
  }
}

const handleCategoryInput = () => {
  const input = productForm.value.categoria_nombre.toLowerCase()
  if (input.length > 0) {
    categorySuggestions.value = categories.value.filter(cat => 
      cat.nombre.toLowerCase().includes(input)
    )
  } else {
    categorySuggestions.value = []
  }
}

const selectCategory = (category: any) => {
  productForm.value.categoria_nombre = category.nombre
  productForm.value.categoria_id = category.id
  categorySuggestions.value = []
}

const editProduct = (product: any) => {
  editingProduct.value = product
  const category = categories.value.find(cat => cat.id === product.categoria_id)
  productForm.value = {
    titulo: product.titulo,
    descripcion: product.descripcion,
    precio: product.precio,
    stock: product.stock,
    categoria_id: product.categoria_id,
    categoria_nombre: category ? category.nombre : '',
    activo: product.activo,
    imagen_url: product.imagen_url || ''
  }
  
  // Detectar si la imagen es una URL o archivo
  if (product.imagen_url && (product.imagen_url.startsWith('http://') || product.imagen_url.startsWith('https://'))) {
    imageType.value = 'url'
  } else {
    imageType.value = 'file'
  }
  
  showEditModal.value = true
}

const deleteProduct = (product: any) => {
  productToDelete.value = product
  showDeleteModal.value = true
}

const confirmDelete = async () => {
  if (!productToDelete.value) return

  try {
    // Verificar que el producto existe en la lista actual
    const productExists = products.value.find(p => p.id === productToDelete.value.id)
    if (!productExists) {
      throw new Error('El producto no existe en la lista actual')
    }

    const response = await auth.makeAuthenticatedRequest(`/api/productos/${productToDelete.value.id}`, {
      method: 'DELETE'
    })

    if (response.ok) {
      products.value = products.value.filter(p => p.id !== productToDelete.value.id)
      showDeleteModal.value = false
      productToDelete.value = null
    } else {
      const errorData = await response.json()
      if (response.status === 404) {
        throw new Error('El producto no existe o ya fue eliminado')
      } else {
        throw new Error(errorData.error || errorData.message || 'Error al eliminar producto')
      }
    }
  } catch (err: any) {
    error.value = err.message || 'Error al eliminar producto'
  }
}

const handleImageUpload = async (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  
  if (!file) return

  // Validate file size (max 5MB)
  if (file.size > 5 * 1024 * 1024) {
    error.value = 'La imagen no puede ser mayor a 5MB'
    return
  }

  // Validate file type
  if (!file.type.startsWith('image/')) {
    error.value = 'Solo se permiten archivos de imagen'
    return
  }

  // Show preview immediately
  const reader = new FileReader()
  reader.onload = (e) => {
    productForm.value.imagen_url = e.target?.result as string
  }
  reader.readAsDataURL(file)

  try {
    const formData = new FormData()
    formData.append('image', file)

    console.log('Subiendo imagen:', file.name, file.size, file.type)

    const response = await auth.makeAuthenticatedRequest('/api/images/upload', {
      method: 'POST',
      body: formData
    })

    console.log('Respuesta de subida:', response.status, response.ok)

    if (response.ok) {
      const data = await response.json()
      console.log('Datos recibidos:', data)
      productForm.value.imagen_url = data.url
    } else {
      const errorData = await response.json()
      console.error('Error en subida:', errorData)
      throw new Error(errorData.error || 'Error al subir la imagen')
    }
  } catch (err: any) {
    console.error('Error completo:', err)
    error.value = err.message || 'Error al subir la imagen'
    // Reset preview on error
    productForm.value.imagen_url = ''
  }
}

const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement
  img.style.display = 'none'
}

const saveProduct = async () => {
  // Prevenir múltiples ejecuciones
  if (saving.value) {
    console.log('Ya se está guardando el producto, ignorando clic')
    return
  }
  
  saving.value = true
  try {
    // Buscar o crear categoría
    let categoriaId = productForm.value.categoria_id
    
    // Verificar si el nombre de categoría ha cambiado o si es una nueva categoría
    const currentCategory = categories.value.find(cat => cat.id === categoriaId)
    const categoryNameChanged = currentCategory && currentCategory.nombre !== productForm.value.categoria_nombre
    
    if ((!categoriaId || categoryNameChanged) && productForm.value.categoria_nombre) {
      // Buscar si la categoría ya existe
      const existingCategory = categories.value.find(cat => 
        cat.nombre.toLowerCase() === productForm.value.categoria_nombre.toLowerCase()
      )
      
      if (existingCategory) {
        categoriaId = existingCategory.id
      } else {
        // Crear nueva categoría
        console.log('Creando nueva categoría:', productForm.value.categoria_nombre)
        const categoryResponse = await auth.makeAuthenticatedRequest('/api/categorias', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ 
            nombre: productForm.value.categoria_nombre,
            descripcion: `Categoría: ${productForm.value.categoria_nombre}`
          })
        })
        
        if (categoryResponse.ok) {
          const newCategory = await categoryResponse.json()
          categoriaId = newCategory.id
          categories.value.push(newCategory)
          console.log('Categoría creada exitosamente:', newCategory)
        } else {
          const errorData = await categoryResponse.json()
          throw new Error(errorData.message || 'Error al crear la categoría')
        }
      }
    }

    const url = editingProduct.value 
      ? `/api/productos/${editingProduct.value.id}`
      : '/api/productos'
    
    const method = editingProduct.value ? 'PUT' : 'POST'

    // Preparar datos del producto
    const productData: any = {
      ...productForm.value,
      categoria_id: categoriaId
    }
    delete productData.categoria_nombre

    const response = await auth.makeAuthenticatedRequest(url, {
      method,
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(productData)
    })

    if (response.ok) {
      // Recargar la lista completa para evitar duplicados
      await loadProducts()
      closeModal()
    } else {
      const errorData = await response.json()
      throw new Error(errorData.error || errorData.message || 'Error al guardar producto')
    }
  } catch (err: any) {
    error.value = err.message || 'Error al guardar producto'
  } finally {
    saving.value = false
  }
}

const closeModal = () => {
  showAddModal.value = false
  showEditModal.value = false
  editingProduct.value = null
  imageType.value = 'file'
  categorySuggestions.value = []
  productForm.value = {
    titulo: '',
    descripcion: '',
    precio: 0,
    stock: 0,
    categoria_id: '',
    categoria_nombre: '',
    activo: true,
    imagen_url: ''
  }
  
  // Reset file input
  const imageInput = document.querySelector('input[type="file"]') as HTMLInputElement
  if (imageInput) {
    imageInput.value = ''
  }
}

const clearFilters = () => {
  searchQuery.value = ''
  selectedCategory.value = ''
  statusFilter.value = ''
  currentPage.value = 1
}

const getCategoryName = (categoryId: string) => {
  const category = categories.value.find(c => c.id === categoryId)
  return category ? category.nombre : 'Sin categoría'
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
.admin-products-page {
  padding: 0;
}

.product-image-container {
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  overflow: hidden;
  background-color: var(--bs-gray-100);
}

.product-thumb {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.product-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: var(--bs-gray-400);
}

.modal.show {
  background-color: rgba(0, 0, 0, 0.5);
}

.table th {
  border-top: none;
  font-weight: 600;
  color: var(--bs-gray-700);
}

.table td {
  vertical-align: middle;
}

.btn-group-sm .btn {
  padding: 0.25rem 0.5rem;
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

.badge {
  font-weight: 500;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .table-responsive {
    font-size: 0.875rem;
  }
  
  .product-image-container {
    width: 40px;
    height: 40px;
  }
  
  .btn-group-sm .btn {
    padding: 0.2rem 0.4rem;
  }
}
</style>