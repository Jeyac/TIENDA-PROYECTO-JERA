<template>
  <div class="catalog-page">
    <div class="container">
      <div class="row mb-4">
        <div class="col-12">
          <h1 class="display-5 fw-bold text-center mb-3">
            <i class="bi bi-grid me-2"></i>Catálogo de productos
          </h1>
          <p class="text-center text-muted lead">
            Descubre nuestra amplia selección de productos de calidad
          </p>
        </div>
      </div>

      <!-- Controles de búsqueda y filtros -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="search-filters-card">
            <div class="row g-3 align-items-end">
              <div class="col-md-6">
                <label for="searchInput" class="form-label fw-semibold">
                  <i class="bi bi-search me-1"></i>Buscar productos
                </label>
                <div class="input-group">
                  <input
                    v-model="searchQuery"
                    type="text"
                    class="form-control"
                    id="searchInput"
                    placeholder="Buscar por nombre o descripción..."
                    @input="handleSearch"
                  >
                  <BaseButton variant="outline-secondary" type="button" @click="clearSearch">
                    <i class="bi bi-x-lg"></i>
                  </BaseButton>
                </div>
              </div>
              <div class="col-md-4">
                <label for="categoryFilter" class="form-label fw-semibold">
                  <i class="bi bi-funnel me-1"></i>Categoría
                </label>
                <select
                  v-model="selectedCategory"
                  class="form-select"
                  id="categoryFilter"
                  @change="handleCategoryFilter"
                >
                  <option value="">Todas las categorías</option>
                  <option v-for="category in categories" :key="category.id" :value="category.id">
                    {{ category.nombre }}
                  </option>
                </select>
              </div>
              <div class="col-md-2">
                <BaseButton variant="outline-secondary" class="w-100" @click="clearFilters">
                  <i class="bi bi-arrow-clockwise me-1"></i>Limpiar
                </BaseButton>
              </div>
            </div>
            
            <!-- Resultados de búsqueda -->
            <div v-if="searchQuery || selectedCategory" class="mt-3">
              <div class="d-flex align-items-center gap-2">
                <span class="badge bg-primary">
                  {{ filteredProducts.length }} producto{{ filteredProducts.length !== 1 ? 's' : '' }} encontrado{{ filteredProducts.length !== 1 ? 's' : '' }}
                </span>
                <span v-if="searchQuery" class="text-muted">
                  para "<strong>{{ searchQuery }}</strong>"
                </span>
                <span v-if="selectedCategory" class="text-muted">
                  en <strong>{{ getCategoryName(selectedCategory) }}</strong>
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="row g-4">
        <div v-for="p in pagedProducts" :key="p.id" class="col-12 col-sm-6 col-md-4 col-lg-3">
            <div class="card h-100 shadow-sm" :class="$catalogUi?.card">
            <div class="card-img-top bg-light d-flex align-items-center justify-content-center" style="height: 200px;">
              <img 
                v-if="getProductImage(p)" 
                :src="getProductImage(p)" 
                :alt="p.titulo"
                class="img-fluid"
                style="max-height: 200px; width: 100%; object-fit: cover; padding: 8px;"
                @error="imageError = true"
              >
              <i v-else class="bi bi-image text-muted" style="font-size: 3rem;"></i>
            </div>
            <div class="card-body d-flex flex-column">
              <div class="d-flex justify-content-between align-items-start mb-2">
                <h5 class="card-title fw-bold">{{ p.titulo }}</h5>
                  <span v-if="p.categoria_nombre" :class="$catalogUi?.badgeCategory">{{ p.categoria_nombre }}</span>
              </div>
              <p class="card-text text-muted flex-grow-1">{{ p.descripcion }}</p>
              <div class="mt-auto">
                <p class="h5 text-primary fw-bold mb-2">Q {{ Number(p.precio).toFixed(2) }}</p>
                <div class="d-flex justify-content-between align-items-center mb-3">
                  <small class="text-muted">
                    <i class="bi bi-box me-1"></i>Stock: {{ p.stock || 0 }}
                  </small>
                  <span v-if="p.stock === 0" class="badge bg-danger">Sin stock</span>
                  <span v-else-if="p.stock <= 5" class="badge bg-warning">Poco stock</span>
                  <span v-else class="badge bg-success">Disponible</span>
                </div>
                
                <!-- Selector de cantidad - visible para todos -->
                <div v-if="p.stock > 0" class="mb-3">
                  <label class="form-label small">Cantidad:</label>
                  <div class="input-group input-group-sm">
                    <button 
                      class="btn btn-outline-secondary" 
                      type="button" 
                      @click="decrementQuantity(p.id)"
                      :disabled="getProductQuantity(p.id) <= 1"
                    >
                      <i class="bi bi-dash"></i>
                    </button>
                    <input 
                      type="number" 
                      class="form-control text-center quantity-input" 
                      :value="getProductQuantity(p.id)"
                      @input="updateQuantity(p.id, $event)"
                      @keydown="handleQuantityKeydown($event, p.id)"
                      @blur="validateQuantity(p.id, $event)"
                      min="1" 
                      :max="p.stock"
                      style="max-width: 60px;"
                    >
                    <button 
                      class="btn btn-outline-secondary" 
                      type="button" 
                      @click="incrementQuantity(p.id)"
                      :disabled="getProductQuantity(p.id) >= p.stock"
                    >
                      <i class="bi bi-plus"></i>
                    </button>
                  </div>
                </div>
                
                <!-- Botón de agregar al carrito - visible para todos -->
                <BaseButton 
                  :class="($catalogUi?.btnAdd || '') + ' w-100'" 
                  :disabled="p.stock === 0 || addingToCart[p.id]"
                  @click="agregar(p, $event)"
                >
                  <i class="bi bi-cart-plus me-2"></i>
                  <span v-if="addingToCart[p.id]">Agregando...</span>
                  <span v-else-if="p.stock === 0">Sin stock</span>
                  <span v-else>Agregar {{ getProductQuantity(p.id) }} al carrito</span>
                </BaseButton>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="d-flex justify-content-center mt-4">
        <Paginator :total-items="filteredProducts.length" :page-size="12" v-model="page" />
      </div>
      
      <div v-if="filteredProducts.length === 0 && (searchQuery || selectedCategory)" class="text-center py-5">
        <i class="bi bi-search text-muted" style="font-size: 4rem;"></i>
        <h3 class="text-muted mt-3">No se encontraron productos</h3>
        <p class="text-muted">Intenta con otros términos de búsqueda o categoría.</p>
        <BaseButton variant="outline-primary" @click="clearFilters">
          <i class="bi bi-arrow-clockwise me-2"></i>Limpiar filtros
        </BaseButton>
      </div>

      <div v-if="productos.length === 0" class="text-center py-5">
        <i class="bi bi-box text-muted" style="font-size: 4rem;"></i>
        <h3 class="text-muted mt-3">No hay productos disponibles</h3>
        <p class="text-muted">Pronto tendremos productos increíbles para ti.</p>
      </div>
    </div>
    
    <!-- Botón flotante del carrito - visible para todos -->
    <div class="position-fixed bottom-0 end-0 p-3" style="z-index: 1000;">
      <NuxtLink to="/carrito" class="btn btn-primary btn-lg rounded-circle shadow-lg position-relative">
        <i class="bi bi-cart3"></i>
        <span v-if="cartCount > 0" class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
          {{ cartCount }}
        </span>
      </NuxtLink>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRuntimeConfig } from 'nuxt/app'
import { useCarritoStore } from '../../stores/carrito'
import { useAuthStore } from '../../stores/auth'

// El catálogo es público, no requiere autenticación
definePageMeta({
  // Sin middleware - acceso público
})

const config = useRuntimeConfig()
const carrito = useCarritoStore()
const auth = useAuthStore()

// Data
const productos = ref<any[]>([])
const categories = ref<any[]>([])
const searchQuery = ref('')
const selectedCategory = ref('')
const searchTimeout = ref<number | null>(null)
const imageError = ref(false)
const productQuantities = ref<Record<number, number>>({})
const addingToCart = ref<Record<number, boolean>>({})

// Computed properties
const filteredProducts = computed(() => {
  // Since filtering is done on the backend, we just return the products
  return productos.value
})

const cartCount = computed(() => {
  return carrito.count
})

// Pagination
const page = ref(1)
const pageSize = 12
const pagedProducts = computed(() => {
  const start = (page.value - 1) * pageSize
  return filteredProducts.value.slice(start, start + pageSize)
})

// Methods
const loadProducts = async (search = '', categoryId = '') => {
  try {
    let url = `${config.public.apiBase}/api/productos/`
    const params = new URLSearchParams()
    
    if (search) params.append('q', search)
    if (categoryId) params.append('categoria_id', categoryId)
    
    if (params.toString()) {
      url += `?${params.toString()}`
    }
    
    const res = await fetch(url)
    if (res.ok) {
      const productsData = await res.json()
      // Normalizar URLs de imágenes
      productos.value = productsData.map((product: any) => ({
        ...product,
        imagenes: product.imagenes ? product.imagenes.map((img: any) => 
          img.startsWith('http') ? img : `${config.public.apiBase}${img}`
        ) : [],
        // Asegurar que imagen_url esté disponible
        imagen_url: product.imagen_url || null
      }))
    }
  } catch (error) {
    console.error('Error cargando productos:', error)
  }
}

const loadCategories = async () => {
  try {
    const res = await fetch(`${config.public.apiBase}/api/categorias/`)
    if (res.ok) {
      categories.value = await res.json()
    }
  } catch (error) {
    console.error('Error cargando categorías:', error)
  }
}

const handleSearch = () => {
  // Debounce search to avoid too many requests
  if (searchTimeout.value) {
    clearTimeout(searchTimeout.value)
  }
  searchTimeout.value = setTimeout(() => {
    loadProducts(searchQuery.value, selectedCategory.value)
  }, 300) as any
}

const handleCategoryFilter = () => {
  loadProducts(searchQuery.value, selectedCategory.value)
}

const clearSearch = () => {
  searchQuery.value = ''
  loadProducts('', selectedCategory.value)
}

const clearFilters = () => {
  searchQuery.value = ''
  selectedCategory.value = ''
  loadProducts()
}

const getCategoryName = (categoryId: string) => {
  const category = categories.value.find(cat => cat.id === parseInt(categoryId))
  return category ? category.nombre : 'Categoría desconocida'
}

const getProductImage = (product: any) => {
  console.log('Getting image for product:', product.titulo, {
    imagen_url: product.imagen_url,
    imagenes: product.imagenes,
    apiBase: config.public.apiBase
  })
  
  // Priorizar imagen_url si está disponible
  if (product.imagen_url) {
    // Si es una URL completa, usarla tal como está
    if (product.imagen_url.startsWith('http://') || product.imagen_url.startsWith('https://')) {
      console.log('Using full URL:', product.imagen_url)
      return product.imagen_url
    }
    // Si es una ruta relativa, construir la URL completa
    const fullUrl = `${config.public.apiBase}${product.imagen_url}`
    console.log('Using constructed URL:', fullUrl)
    return fullUrl
  }
  
  // Fallback a imagenes array
  if (product.imagenes && product.imagenes.length > 0) {
    console.log('Using imagenes array:', product.imagenes[0])
    return product.imagenes[0]
  }
  
  console.log('No image found for product:', product.titulo)
  return null
}

// Funciones para manejar cantidades
const getProductQuantity = (productId: number) => {
  return productQuantities.value[productId] || 1
}

const incrementQuantity = (productId: number) => {
  const product = productos.value.find(p => p.id === productId)
  if (product && getProductQuantity(productId) < product.stock) {
    productQuantities.value[productId] = getProductQuantity(productId) + 1
  }
}

const decrementQuantity = (productId: number) => {
  if (getProductQuantity(productId) > 1) {
    productQuantities.value[productId] = getProductQuantity(productId) - 1
  }
}

const updateQuantity = (productId: number, event: Event) => {
  const target = event.target as HTMLInputElement
  const value = parseInt(target.value) || 1
  const product = productos.value.find(p => p.id === productId)
  
  if (product) {
    const maxStock = product.stock
    const quantity = Math.max(1, Math.min(value, maxStock))
    productQuantities.value[productId] = quantity
    
    // Actualizar el valor del input si es necesario
    if (target.value !== quantity.toString()) {
      target.value = quantity.toString()
    }
  }
}

const handleQuantityKeydown = (event: KeyboardEvent, productId: number) => {
  // Permitir teclas de navegación y edición
  const allowedKeys = ['Backspace', 'Delete', 'Tab', 'Escape', 'Enter', 'ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', 'Home', 'End']
  
  if (allowedKeys.includes(event.key)) {
    return
  }
  
  // Permitir Ctrl+A, Ctrl+C, Ctrl+V, Ctrl+X
  if (event.ctrlKey && ['a', 'c', 'v', 'x'].includes(event.key.toLowerCase())) {
    return
  }
  
  // Permitir solo números
  if (!/^\d$/.test(event.key)) {
    event.preventDefault()
  }
}

const validateQuantity = (productId: number, event: Event) => {
  const target = event.target as HTMLInputElement
  const value = parseInt(target.value) || 1
  const product = productos.value.find(p => p.id === productId)
  
  if (product) {
    const maxStock = product.stock
    const quantity = Math.max(1, Math.min(value, maxStock))
    productQuantities.value[productId] = quantity
  }
}

const agregar = async (p: any, event?: Event) => {
  if (event) {
    event.preventDefault()
    event.stopPropagation()
  }
  
  // Prevenir múltiples clics
  if (addingToCart.value[p.id]) {
    console.log('Ya se está agregando este producto, ignorando clic')
    return
  }
  
  // Si el usuario no está autenticado, mostrar mensaje pero no redirigir
  if (!auth.isAuthenticated) {
    alert('Debes iniciar sesión para agregar productos al carrito')
    return
  }
  
  // Validar stock disponible
  const quantity = getProductQuantity(p.id)
  if (p.stock < quantity) {
    alert(`No hay suficiente stock. Solo quedan ${p.stock} unidades disponibles.`)
    return
  }
  
  // Marcar como agregando
  addingToCart.value[p.id] = true
  
  try {
    carrito.agregarItem(p, quantity)
    
    // Mostrar feedback visual
    console.log(`Agregado ${quantity} de ${p.titulo} al carrito`)
    
    // Pequeño delay para evitar clics múltiples
    await new Promise(resolve => setTimeout(resolve, 500))
  } catch (error: any) {
    alert(error.message)
  } finally {
    // Liberar el flag
    addingToCart.value[p.id] = false
  }
}

// Lifecycle
onMounted(async () => {
  await Promise.all([
    loadProducts(),
    loadCategories()
  ])
  
  // Escuchar eventos de pedido creado para actualizar el catálogo
  if (typeof window !== 'undefined') {
    window.addEventListener('pedidoCreado', async () => {
      console.log('Pedido creado, actualizando catálogo...')
      await loadProducts(searchQuery.value, selectedCategory.value)
    })
  }
})

onUnmounted(() => {
  // Limpiar event listener
  if (typeof window !== 'undefined') {
    window.removeEventListener('pedidoCreado', () => {})
  }
})
</script>

<style scoped>
.search-filters-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 1.5rem;
  padding: 2rem;
  box-shadow: 
    0 20px 40px rgba(102, 126, 234, 0.15),
    0 8px 16px rgba(102, 126, 234, 0.1);
  margin-bottom: 1rem;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.search-filters-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, transparent 100%);
  pointer-events: none;
}

.search-filters-card:hover {
  transform: translateY(-2px);
  box-shadow: 
    0 25px 50px rgba(102, 126, 234, 0.2),
    0 12px 24px rgba(102, 126, 234, 0.15);
}

.search-filters-card .form-label {
  color: var(--bs-body-color);
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

/* Los estilos globales ya se aplican automáticamente */

/* Estilos específicos para el input de cantidad */
.quantity-input {
  border: 2px solid rgba(102, 126, 234, 0.15) !important;
  background: rgba(255, 255, 255, 0.9) !important;
  backdrop-filter: blur(5px) !important;
  color: #000000 !important;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.1) !important;
  font-weight: 600;
  font-size: 0.9rem;
}

.quantity-input:focus {
  border-color: #667eea !important;
  box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25), 0 4px 12px rgba(102, 126, 234, 0.15) !important;
  background: rgba(255, 255, 255, 1) !important;
  outline: none !important;
}

.quantity-input:hover {
  border-color: rgba(102, 126, 234, 0.25) !important;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15) !important;
}

/* Botones de cantidad */
.input-group .btn-outline-secondary {
  border-color: rgba(102, 126, 234, 0.15);
  color: #667eea;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(5px);
  transition: all 0.3s ease;
}

.input-group .btn-outline-secondary:hover {
  border-color: #667eea;
  background: #667eea;
  color: white;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
}

.input-group .btn-outline-secondary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}


.search-filters-card .input-group .btn {
  border-radius: 0 0.5rem 0.5rem 0;
}

.search-filters-card .btn-outline-secondary {
  border-radius: 0.5rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.search-filters-card .btn-outline-secondary:hover {
  transform: translateY(-1px);
}

.badge.bg-primary {
  font-size: 0.8rem;
  padding: 0.4rem 0.8rem;
}

.product-card .badge.bg-secondary {
  font-size: 0.7rem;
  padding: 0.25rem 0.5rem;
}

/* Dark theme adjustments */
.dark-theme .search-filters-card {
  background-color: var(--bs-gray-100);
  border-color: var(--bs-border-color);
}

.product-card {
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 1.5rem;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  box-shadow: 
    0 10px 30px rgba(102, 126, 234, 0.15),
    0 4px 12px rgba(102, 126, 234, 0.1);
  position: relative;
}

.product-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, transparent 100%);
  pointer-events: none;
  z-index: 1;
}

.product-card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 
    0 20px 60px rgba(102, 126, 234, 0.25),
    0 8px 24px rgba(102, 126, 234, 0.15);
  border-color: rgba(255, 255, 255, 0.3);
}

.product-card .card-img-top {
  background: linear-gradient(135deg, var(--bs-light) 0%, var(--bs-gray-100) 100%);
}

.product-card .btn {
  border-radius: 0.5rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.product-card .btn:hover {
  transform: translateY(-1px);
}

.card-title {
  color: var(--bs-dark);
  font-size: 1.1rem;
}

.card-text {
  font-size: 0.9rem;
  line-height: 1.4;
}

/* Dark theme adjustments */
.dark-theme .product-card {
  background-color: var(--bs-gray-100);
  border-color: var(--bs-border-color);
}

.dark-theme .product-card .card-img-top {
  background: linear-gradient(135deg, var(--bs-gray-200) 0%, var(--bs-gray-300) 100%);
}

.dark-theme .card-title {
  color: var(--bs-body-color);
}
</style>





