<template>
  <div class="app-layout">
    <!-- Header -->
    <header class="app-header">
      <nav class="navbar navbar-expand-lg">
        <div class="container-fluid">
          <NuxtLink class="navbar-brand fw-bold" to="/">
            <i class="bi bi-shop me-2"></i>
            Infinite Finds
          </NuxtLink>
          
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span class="navbar-toggler-icon"></span>
          </button>
          
          <div class="collapse navbar-collapse" id="navbarNav">
            <ClientOnly>
              <ul class="navbar-nav me-auto">
                <!-- Solo mostrar para usuarios normales, no para administradores -->
                <li v-if="!auth.isAdmin" class="nav-item">
                  <NuxtLink 
                    class="nav-link" 
                    to="/catalogo"
                    :class="{ 'active': $route.path === '/catalogo' }"
                  >
                    <i class="bi bi-grid me-1"></i>Catálogo
                  </NuxtLink>
                </li>
                <li v-if="!auth.isAdmin" class="nav-item">
                  <NuxtLink 
                    class="nav-link" 
                    to="/soporte"
                    :class="{ 'active': $route.path === '/soporte' }"
                  >
                    <i class="bi bi-chat-dots me-1"></i>Soporte
                  </NuxtLink>
                </li>
                <li v-if="auth.isAuthenticated && !auth.isAdmin" class="nav-item">
                  <NuxtLink 
                    class="nav-link" 
                    to="/tickets"
                    :class="{ 'active': $route.path === '/tickets' }"
                  >
                    <i class="bi bi-ticket-perforated me-1"></i>Tickets
                  </NuxtLink>
                </li>
                <li v-if="auth.isAuthenticated && !auth.isAdmin" class="nav-item">
                  <NuxtLink 
                    class="nav-link" 
                    to="/orders"
                    :class="{ 'active': $route.path === '/orders' }"
                  >
                    <i class="bi bi-bag me-1"></i>Mis Pedidos
                  </NuxtLink>
                </li>
                <li v-if="!auth.isAdmin" class="nav-item">
                  <NuxtLink 
                    class="nav-link" 
                    to="/carrito"
                    :class="{ 'active': $route.path === '/carrito' }"
                  >
                    <i class="bi bi-cart me-1"></i>Carrito
                    <span v-if="cartCount > 0" class="badge bg-primary ms-1">{{ cartCount }}</span>
                  </NuxtLink>
                </li>
              </ul>
              
              <ul class="navbar-nav">
                <!-- Selector de zona horaria -->
                <li class="nav-item">
                  <ClientOnly>
                    <div class="d-flex align-items-center gap-2">
                      <i class="bi bi-globe text-primary"></i>
                      <select 
                        v-model="selectedTimezone" 
                        @change="updateTimezone"
                        class="form-select form-select-sm"
                        style="max-width: 150px; font-size: 0.8rem;"
                      >
                        <option value="auto">🌍 Auto</option>
                        <option value="America/Guatemala">🇬🇹 Guatemala</option>
                        <option value="America/El_Salvador">🇸🇻 El Salvador</option>
                        <option value="America/Honduras">🇭🇳 Honduras</option>
                        <option value="America/Nicaragua">🇳🇮 Nicaragua</option>
                        <option value="America/Costa_Rica">🇨🇷 Costa Rica</option>
                        <option value="America/Mexico_City">🇲🇽 México</option>
                        <option value="America/New_York">🇺🇸 USA Este</option>
                        <option value="America/Los_Angeles">🇺🇸 USA Oeste</option>
                        <option value="Europe/Madrid">🇪🇸 España</option>
                      </select>
                    </div>
                  </ClientOnly>
                </li>
                
                <li v-if="!auth.isAuthenticated" class="nav-item">
                  <NuxtLink class="nav-link" to="/login">
                    <i class="bi bi-person me-1"></i>Login
                  </NuxtLink>
                </li>
                <li v-if="!auth.isAuthenticated" class="nav-item">
                  <NuxtLink class="nav-link" to="/register">
                    <i class="bi bi-person-plus me-1"></i>Registro
                  </NuxtLink>
                </li>
                <li v-if="auth.isAuthenticated" class="nav-item dropdown">
                  <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                    <i class="bi bi-person-circle me-1"></i>{{ auth.userName }}
                  </a>
                  <ul class="dropdown-menu">
                    <li><span class="dropdown-item-text text-muted">{{ auth.userEmail }}</span></li>
                    <li><hr class="dropdown-divider"></li>
                    <!-- Solo mostrar perfil y pedidos para usuarios normales -->
                    <li v-if="!auth.isAdmin"><NuxtLink 
                      class="dropdown-item" 
                      to="/profile"
                      :class="{ 'active': $route.path === '/profile' }"
                    >
                      <i class="bi bi-person me-2"></i>Mi perfil
                    </NuxtLink></li>
                    <li v-if="!auth.isAdmin"><NuxtLink 
                      class="dropdown-item" 
                      to="/orders"
                      :class="{ 'active': $route.path === '/orders' }"
                    >
                      <i class="bi bi-bag me-2"></i>Mis pedidos
                    </NuxtLink></li>
                    <li v-if="auth.isAdmin"><NuxtLink class="dropdown-item" to="/admin/analytics">
                      <i class="bi bi-gear me-2"></i>Administración
                    </NuxtLink></li>
                    <li><hr class="dropdown-divider"></li>
                    <li><button class="dropdown-item text-danger" @click="auth.logout()">
                      <i class="bi bi-box-arrow-right me-2"></i>Cerrar sesión
                    </button></li>
                  </ul>
                </li>
              </ul>
              <template #fallback>
                <ul class="navbar-nav me-auto">
                  <li class="nav-item">
                    <NuxtLink class="nav-link" to="/catalogo">
                      <i class="bi bi-grid me-1"></i>Catálogo
                    </NuxtLink>
                  </li>
                  <li class="nav-item">
                    <NuxtLink class="nav-link" to="/soporte">
                      <i class="bi bi-chat-dots me-1"></i>Soporte
                    </NuxtLink>
                  </li>
                  <li class="nav-item">
                    <NuxtLink class="nav-link" to="/carrito">
                      <i class="bi bi-cart me-1"></i>Carrito
                    </NuxtLink>
                  </li>
                </ul>
                <ul class="navbar-nav">
                  <li class="nav-item">
                    <span class="nav-link">
                      <i class="bi bi-person me-1"></i>Cargando...
                    </span>
                  </li>
                </ul>
              </template>
            </ClientOnly>
          </div>
        </div>
      </nav>
    </header>

    <!-- Main Content -->
    <main class="app-main">
      <div class="container-fluid py-4">
        <slot />
      </div>
    </main>

    <!-- Footer -->
    <footer class="app-footer mt-auto">
      <div class="container-fluid py-4">
        <div class="row">
          <div class="col-md-6">
            <h6 class="fw-bold mb-2">
              <i class="bi bi-shop me-1"></i>Infinite Finds
            </h6>
            <p class="text-muted small mb-0">
              Tu tienda online de confianza con los mejores productos y atención al cliente.
            </p>
          </div>
          <div class="col-md-6 text-md-end">
            <div class="social-links">
              <a href="#" class="text-decoration-none me-3">
                <i class="bi bi-facebook"></i>
              </a>
              <a href="#" class="text-decoration-none me-3">
                <i class="bi bi-twitter"></i>
              </a>
              <a href="#" class="text-decoration-none me-3">
                <i class="bi bi-instagram"></i>
              </a>
              <a href="#" class="text-decoration-none">
                <i class="bi bi-linkedin"></i>
              </a>
            </div>
            <p class="text-muted small mt-2 mb-0">
              © 2025 Infinite Finds. Todos los derechos reservados. By JA
            </p>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useCarritoStore } from '../stores/carrito'
import { useAuthStore } from '../stores/auth'

// Theme management usando el plugin
const { $theme } = useNuxtApp()

// Cart count (connected to cart store)
const cartCount = computed(() => {
  const carrito = useCarritoStore()
  return carrito.count
})

// Auth store
const auth = useAuthStore()

// Timezone selector
const selectedTimezone = ref('auto')

// Detectar zona horaria automáticamente
const detectTimezone = () => {
  try {
    const userTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone
    return userTimezone
  } catch (error) {
    console.warn('No se pudo detectar la zona horaria:', error)
    return 'America/Guatemala'
  }
}

// Actualizar zona horaria
const updateTimezone = () => {
  const timezone = selectedTimezone.value === 'auto' ? detectTimezone() : selectedTimezone.value
  
  // Guardar en localStorage
  localStorage.setItem('userTimezone', timezone)
  
  // Emitir evento para que otros componentes se actualicen
  window.dispatchEvent(new CustomEvent('timezoneChanged', { 
    detail: { timezone } 
  }))
}

// Initialize auth on mount
onMounted(() => {
  auth.initializeAuth()
  
  // Cargar zona horaria guardada
  const savedTimezone = localStorage.getItem('userTimezone')
  if (savedTimezone) {
    selectedTimezone.value = savedTimezone
  } else {
    // Detectar automáticamente
    const detected = detectTimezone()
    selectedTimezone.value = 'auto'
    localStorage.setItem('userTimezone', detected)
  }
  
  // Redirigir según el rol si está en páginas que no corresponden a su rol
  if (auth.isAuthenticated) {
    const currentPath = window.location.pathname
    
    // Si es administrador y no está en páginas de admin, redirigir
    if (auth.user?.rol === 'administrador' && !currentPath.startsWith('/admin')) {
      navigateTo('/admin/analytics')
    } 
    // Si es atención al cliente y no está en páginas de atención, redirigir
    else if (auth.user?.rol === 'atencion_cliente' && !currentPath.startsWith('/atencion')) {
      navigateTo('/atencion/tickets')
    }
    // Si es usuario normal y está en páginas de admin o atención, redirigir
    else if (auth.user?.rol === 'usuario' && (currentPath.startsWith('/admin') || currentPath.startsWith('/atencion'))) {
      navigateTo('/profile')
    }
  }
})
</script>

<style scoped>
.app-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.app-header {
  position: sticky;
  top: 0;
  z-index: 1000;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(102, 126, 234, 0.15);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
}

.app-header:hover {
  box-shadow: 0 12px 40px rgba(102, 126, 234, 0.2);
}

.app-main {
  flex: 1;
  position: relative;
  background: transparent;
}

.app-main::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.1) 0%, transparent 50%);
  pointer-events: none;
}

.app-footer {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  position: relative;
  overflow: hidden;
}

/* Responsive Design */
@media (max-width: 768px) {
  .navbar-brand {
    font-size: 1.1rem;
  }
  
  .navbar-nav .nav-link {
    padding: 0.5rem 0.75rem;
  }
  
  .navbar-nav .dropdown-menu {
    position: static !important;
    float: none;
    width: 100%;
    margin-top: 0;
    background-color: var(--bs-body-bg);
    border: 1px solid rgba(102, 126, 234, 0.1);
    box-shadow: 0 0.5rem 1rem rgba(102, 126, 234, 0.1);
  }
  
  .app-main {
    padding: 1rem 0;
  }
  
  .app-footer {
    padding: 1.5rem 0;
  }
  
  .app-footer .row {
    text-align: center;
  }
  
  .app-footer .col-md-6 {
    margin-bottom: 1rem;
  }
}

@media (max-width: 576px) {
  .navbar-brand {
    font-size: 1rem;
  }
  
  .navbar-toggler {
    padding: 0.25rem 0.5rem;
  }
  
  .app-main {
    padding: 0.5rem 0;
  }
  
  .app-footer {
    padding: 1rem 0;
  }
  
  .app-footer h6 {
    font-size: 1rem;
  }
  
  .app-footer .social-links a {
    font-size: 1.2rem;
    margin: 0 0.5rem;
  }
}

.app-footer::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 30% 20%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 70% 80%, rgba(255, 255, 255, 0.05) 0%, transparent 50%);
  pointer-events: none;
}

.social-links a {
  color: var(--bs-gray-600);
  font-size: 1.2rem;
  transition: color 0.3s ease;
}

.social-links a:hover {
  color: var(--bs-primary);
}


/* Custom scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: var(--bs-gray-100);
}

::-webkit-scrollbar-thumb {
  background: var(--bs-gray-400);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: var(--bs-gray-500);
}

/* Smooth transitions */
.nav-link, .btn, .social-links a {
  transition: all 0.3s ease;
}

/* Badge animation */
.badge {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}
</style>
