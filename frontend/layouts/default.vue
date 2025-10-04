<template>
  <div class="app-layout" :class="{ 'dark-theme': isDark }">
    <!-- Header -->
    <header class="app-header">
      <nav class="navbar navbar-expand-lg" :class="isDark ? 'navbar-dark bg-dark' : 'navbar-light bg-white'">
        <div class="container-fluid">
          <NuxtLink class="navbar-brand fw-bold" to="/">
            <i class="bi bi-shop me-2"></i>
            Infinite Finds
          </NuxtLink>
          
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span class="navbar-toggler-icon"></span>
          </button>
          
          <div class="collapse navbar-collapse" id="navbarNav">
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
                  <span v-if="cartCount > 0" class="badge bg-primary ms-1">{{ cartCount }}</span>
                </NuxtLink>
              </li>
            </ul>
            
            <ul class="navbar-nav">
              <li class="nav-item">
                <button class="btn btn-outline-secondary btn-sm me-2" @click="toggleTheme">
                  <i :class="isDark ? 'bi bi-sun' : 'bi bi-moon'"></i>
                </button>
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
                  <li><NuxtLink class="dropdown-item" to="/profile">
                    <i class="bi bi-person me-2"></i>Mi Perfil
                  </NuxtLink></li>
                  <li><NuxtLink class="dropdown-item" to="/orders">
                    <i class="bi bi-bag me-2"></i>Mis Pedidos
                  </NuxtLink></li>
                  <li v-if="auth.isAdmin"><NuxtLink class="dropdown-item" to="/admin">
                    <i class="bi bi-gear me-2"></i>Administración
                  </NuxtLink></li>
                  <li><hr class="dropdown-divider"></li>
                  <li><button class="dropdown-item text-danger" @click="auth.logout()">
                    <i class="bi bi-box-arrow-right me-2"></i>Cerrar Sesión
                  </button></li>
                </ul>
              </li>
            </ul>
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
              © 2024 Infinite Finds. Todos los derechos reservados.
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

// Theme management
const isDark = ref(false)

// Load theme preference from localStorage
if (typeof window !== 'undefined') {
  const savedTheme = localStorage.getItem('theme')
  isDark.value = savedTheme === 'dark'
}

const toggleTheme = () => {
  isDark.value = !isDark.value
  if (typeof window !== 'undefined') {
    localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
  }
}

// Cart count (connected to cart store)
const cartCount = computed(() => {
  const carrito = useCarritoStore()
  return carrito.count
})

// Auth store
const auth = useAuthStore()

// Initialize auth on mount
onMounted(() => {
  auth.initializeAuth()
  
  // Redirigir admin a su dashboard si está en la página principal
  if (auth.isAuthenticated && auth.isAdmin && window.location.pathname === '/') {
    navigateTo('/admin-redirect')
  }
})
</script>

<style scoped>
.app-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
}

.app-header {
  position: sticky;
  top: 0;
  z-index: 1000;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.app-main {
  flex: 1;
  background-color: var(--bs-body-bg);
}

.app-footer {
  background-color: var(--bs-gray-100);
  border-top: 1px solid var(--bs-border-color);
}

.social-links a {
  color: var(--bs-gray-600);
  font-size: 1.2rem;
  transition: color 0.3s ease;
}

.social-links a:hover {
  color: var(--bs-primary);
}

/* Dark theme styles */
.dark-theme {
  --bs-body-bg: #1a1a1a;
  --bs-body-color: #e9ecef;
  --bs-gray-100: #2d2d2d;
  --bs-gray-600: #adb5bd;
  --bs-border-color: #495057;
}

.dark-theme .app-footer {
  background-color: var(--bs-gray-100);
  border-top-color: var(--bs-border-color);
}

.dark-theme .navbar {
  box-shadow: 0 2px 4px rgba(255,255,255,0.1);
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
