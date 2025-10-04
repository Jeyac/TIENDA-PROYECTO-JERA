<template>
  <div class="catalog-page">
    <div class="container">
      <div class="row mb-4">
        <div class="col-12">
          <h1 class="display-5 fw-bold text-center mb-3">
            <i class="bi bi-grid me-2"></i>Catálogo de Productos
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
                  <i class="bi bi-search me-1"></i>Buscar Productos
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
                  <button class="btn btn-outline-secondary" type="button" @click="clearSearch">
                    <i class="bi bi-x-lg"></i>
                  </button>
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
                <button class="btn btn-outline-secondary w-100" @click="clearFilters">
                  <i class="bi bi-arrow-clockwise me-1"></i>Limpiar
                </button>
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
        <div v-for="p in filteredProducts" :key="p.id" class="col-12 col-sm-6 col-md-4 col-lg-3">
          <div class="card h-100 product-card shadow-sm">
            <div class="card-img-top bg-light d-flex align-items-center justify-content-center" style="height: 200px;">
              <i class="bi bi-image text-muted" style="font-size: 3rem;"></i>
            </div>
            <div class="card-body d-flex flex-column">
              <div class="d-flex justify-content-between align-items-start mb-2">
                <h5 class="card-title fw-bold">{{ p.titulo }}</h5>
                <span v-if="p.categoria_nombre" class="badge bg-secondary">{{ p.categoria_nombre }}</span>
              </div>
              <p class="card-text text-muted flex-grow-1">{{ p.descripcion }}</p>
              <div class="mt-auto">
                <p class="h5 text-primary fw-bold mb-3">Q {{ Number(p.precio).toFixed(2) }}</p>
                <button class="btn btn-primary w-100" @click="agregar(p)">
                  <i class="bi bi-cart-plus me-2"></i>Agregar al Carrito
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div v-if="filteredProducts.length === 0 && (searchQuery || selectedCategory)" class="text-center py-5">
        <i class="bi bi-search text-muted" style="font-size: 4rem;"></i>
        <h3 class="text-muted mt-3">No se encontraron productos</h3>
        <p class="text-muted">Intenta con otros términos de búsqueda o categoría.</p>
        <button class="btn btn-outline-primary" @click="clearFilters">
          <i class="bi bi-arrow-clockwise me-2"></i>Limpiar filtros
        </button>
      </div>

      <div v-if="productos.length === 0" class="text-center py-5">
        <i class="bi bi-box text-muted" style="font-size: 4rem;"></i>
        <h3 class="text-muted mt-3">No hay productos disponibles</h3>
        <p class="text-muted">Pronto tendremos productos increíbles para ti.</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRuntimeConfig } from 'nuxt/app'
import { useCarritoStore } from '../../stores/carrito'

const config = useRuntimeConfig()
const carrito = useCarritoStore()

// Data
const productos = ref<any[]>([])
const categories = ref<any[]>([])
const searchQuery = ref('')
const selectedCategory = ref('')
const searchTimeout = ref<number | null>(null)

// Computed properties
const filteredProducts = computed(() => {
  // Since filtering is done on the backend, we just return the products
  return productos.value
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
      productos.value = await res.json()
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
  }, 300)
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

const agregar = (p: any) => {
  carrito.agregarItem(p)
}

// Lifecycle
onMounted(async () => {
  await Promise.all([
    loadProducts(),
    loadCategories()
  ])
})
</script>

<style scoped>
.search-filters-card {
  background: var(--bs-body-bg);
  border: 1px solid var(--bs-border-color);
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 0.25rem 0.5rem rgba(0, 0, 0, 0.1);
  margin-bottom: 1rem;
}

.search-filters-card .form-label {
  color: var(--bs-body-color);
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.search-filters-card .form-control,
.search-filters-card .form-select {
  border-radius: 0.5rem;
  border: 1px solid var(--bs-border-color);
  transition: all 0.3s ease;
}

.search-filters-card .form-control:focus,
.search-filters-card .form-select:focus {
  border-color: var(--bs-primary);
  box-shadow: 0 0 0 0.2rem rgba(var(--bs-primary-rgb), 0.25);
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
  border: 1px solid var(--bs-border-color);
  border-radius: 1rem;
  overflow: hidden;
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15) !important;
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


