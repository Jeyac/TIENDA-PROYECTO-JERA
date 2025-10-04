<template>
  <div class="admin-layout">
    <!-- Admin Sidebar -->
    <nav class="admin-sidebar" :class="{ 'collapsed': sidebarCollapsed }">
      <div class="sidebar-header">
        <div class="d-flex align-items-center">
          <i class="bi bi-shield-check text-primary me-2"></i>
          <span v-if="!sidebarCollapsed" class="fw-bold">Admin Panel</span>
        </div>
        <button class="btn btn-link btn-sm text-muted" @click="toggleSidebar">
          <i :class="sidebarCollapsed ? 'bi bi-chevron-right' : 'bi bi-chevron-left'"></i>
        </button>
      </div>
      
      <div class="sidebar-content">
        <ul class="nav nav-pills flex-column">
          <li class="nav-item">
            <NuxtLink to="/admin" class="nav-link" :class="{ 'active': $route.path === '/admin' || $route.path === '/admin/' }">
              <i class="bi bi-house me-2"></i>
              <span v-if="!sidebarCollapsed">Dashboard</span>
            </NuxtLink>
          </li>
          <li class="nav-item">
            <NuxtLink to="/admin/analytics" class="nav-link" :class="{ 'active': $route.path === '/admin/analytics' }">
              <i class="bi bi-graph-up me-2"></i>
              <span v-if="!sidebarCollapsed">Analytics</span>
            </NuxtLink>
          </li>
          <li class="nav-item">
            <NuxtLink to="/admin/users" class="nav-link" :class="{ 'active': $route.path === '/admin/users' }">
              <i class="bi bi-people me-2"></i>
              <span v-if="!sidebarCollapsed">Usuarios</span>
            </NuxtLink>
          </li>
          <li class="nav-item">
            <NuxtLink to="/admin/products" class="nav-link" :class="{ 'active': $route.path === '/admin/products' }">
              <i class="bi bi-box me-2"></i>
              <span v-if="!sidebarCollapsed">Productos</span>
            </NuxtLink>
          </li>
          <li class="nav-item">
            <NuxtLink to="/admin/orders" class="nav-link" :class="{ 'active': $route.path === '/admin/orders' }">
              <i class="bi bi-bag me-2"></i>
              <span v-if="!sidebarCollapsed">Pedidos</span>
            </NuxtLink>
          </li>
          <li class="nav-item">
            <NuxtLink to="/admin/chats" class="nav-link" :class="{ 'active': $route.path === '/admin/chats' }">
              <i class="bi bi-chat-dots me-2"></i>
              <span v-if="!sidebarCollapsed">Chats</span>
            </NuxtLink>
          </li>
          <li class="nav-item">
            <NuxtLink to="/admin/rag" class="nav-link" :class="{ 'active': $route.path === '/admin/rag' }">
              <i class="bi bi-file-earmark-arrow-up me-2"></i>
              <span v-if="!sidebarCollapsed">Archivos RAG</span>
            </NuxtLink>
          </li>
        </ul>
      </div>
      
      <div class="sidebar-footer">
        <div class="nav-item">
          <button class="nav-link text-danger" @click="logout">
            <i class="bi bi-box-arrow-right me-2"></i>
            <span v-if="!sidebarCollapsed">Cerrar Sesión</span>
          </button>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="admin-main" :class="{ 'sidebar-collapsed': sidebarCollapsed }">
      <!-- Top Bar -->
      <header class="admin-topbar">
        <div class="d-flex justify-content-between align-items-center">
          <div class="d-flex align-items-center">
            <button class="btn btn-outline-secondary btn-sm me-3" @click="toggleSidebar">
              <i class="bi bi-list"></i>
            </button>
            <h4 class="mb-0">{{ pageTitle }}</h4>
          </div>
          <div class="d-flex align-items-center gap-3">
            <div class="user-info">
              <span class="text-muted">Bienvenido,</span>
              <strong>{{ auth.userName }}</strong>
            </div>
            <button class="btn btn-outline-secondary btn-sm" @click="toggleTheme">
              <i :class="isDark ? 'bi bi-sun' : 'bi bi-moon'"></i>
            </button>
            <NuxtLink to="/" class="btn btn-outline-primary btn-sm">
              <i class="bi bi-house me-1"></i>Ir al Sitio
            </NuxtLink>
          </div>
        </div>
      </header>

      <!-- Page Content -->
      <main class="admin-content">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const route = useRoute()

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

// Sidebar management
const sidebarCollapsed = ref(false)

const toggleSidebar = () => {
  sidebarCollapsed.value = !sidebarCollapsed.value
}

// Page title based on route
const pageTitle = computed(() => {
  const titles: { [key: string]: string } = {
    '/admin/analytics': 'Analytics',
    '/admin/users': 'Gestión de Usuarios',
    '/admin/products': 'Gestión de Productos',
    '/admin/orders': 'Historial de Pedidos',
    '/admin/chats': 'Historial de Chats',
    '/admin/rag': 'Archivos RAG'
  }
  return titles[route.path] || 'Administración'
})

const logout = async () => {
  await auth.logout()
}
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
  background-color: var(--bs-gray-100);
}

.admin-sidebar {
  width: 250px;
  background: var(--bs-white);
  border-right: 1px solid var(--bs-border-color);
  display: flex;
  flex-direction: column;
  transition: width 0.3s ease;
  position: fixed;
  height: 100vh;
  z-index: 1000;
}

.admin-sidebar.collapsed {
  width: 60px;
}

.sidebar-header {
  padding: 1rem;
  border-bottom: 1px solid var(--bs-border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.sidebar-content {
  flex: 1;
  padding: 1rem 0;
  overflow-y: auto;
}

.sidebar-footer {
  padding: 1rem;
  border-top: 1px solid var(--bs-border-color);
}

.nav-link {
  color: var(--bs-gray-700);
  padding: 0.75rem 1rem;
  border-radius: 0;
  transition: all 0.3s ease;
}

.nav-link:hover {
  background-color: var(--bs-gray-100);
  color: var(--bs-primary);
}

.nav-link.active {
  background-color: var(--bs-primary);
  color: white;
}

.nav-link i {
  width: 20px;
  text-align: center;
}

.admin-main {
  flex: 1;
  margin-left: 250px;
  transition: margin-left 0.3s ease;
  display: flex;
  flex-direction: column;
}

.admin-main.sidebar-collapsed {
  margin-left: 60px;
}

.admin-topbar {
  background: var(--bs-white);
  border-bottom: 1px solid var(--bs-border-color);
  padding: 1rem 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.admin-content {
  flex: 1;
  padding: 1.5rem;
  overflow-y: auto;
}

.user-info {
  font-size: 0.9rem;
}

/* Dark theme adjustments */
.dark-theme .admin-sidebar {
  background-color: var(--bs-gray-100);
  border-right-color: var(--bs-border-color);
}

.dark-theme .admin-topbar {
  background-color: var(--bs-gray-100);
  border-bottom-color: var(--bs-border-color);
}

.dark-theme .admin-layout {
  background-color: var(--bs-gray-200);
}

.dark-theme .nav-link:hover {
  background-color: var(--bs-gray-200);
}

/* Responsive */
@media (max-width: 768px) {
  .admin-sidebar {
    transform: translateX(-100%);
  }
  
  .admin-sidebar.show {
    transform: translateX(0);
  }
  
  .admin-main {
    margin-left: 0;
  }
  
  .admin-main.sidebar-collapsed {
    margin-left: 0;
  }
}
</style>
