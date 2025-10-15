<template>
  <div class="admin-layout">
    <!-- Admin Sidebar -->
    <nav class="admin-sidebar" :class="{ 'collapsed': sidebarCollapsed }">
      <div class="sidebar-header">
        <div class="d-flex align-items-center">
          <i class="bi bi-shield-check text-primary me-2"></i>
          <span v-if="!sidebarCollapsed" class="fw-bold">
            {{ auth.user?.rol === 'administrador' ? 'Panel de administración' : 'Panel de atención' }}
          </span>
        </div>
        <button class="btn btn-link btn-sm text-muted ms-2" @click="toggleSidebar">
          <i :class="sidebarCollapsed ? 'bi bi-chevron-right' : 'bi bi-chevron-left'"></i>
        </button>
      </div>
      
      <div class="sidebar-content">
        <ul class="nav nav-pills flex-column gap-1">
          <!-- Menú para Administradores -->
          <template v-if="auth.user?.rol === 'administrador'">
            <li class="nav-item">
              <NuxtLink to="/admin/analytics" class="nav-link d-flex align-items-center" :class="{ 'active': $route.path === '/admin/analytics' }">
                <i class="bi bi-graph-up me-3"></i>
                <span v-if="!sidebarCollapsed" class="fw-medium">Analitica</span>
              </NuxtLink>
            </li>
            <li class="nav-item">
              <NuxtLink to="/admin/users" class="nav-link d-flex align-items-center" :class="{ 'active': $route.path === '/admin/users' }">
                <i class="bi bi-people me-3"></i>
                <span v-if="!sidebarCollapsed" class="fw-medium">Gestión de usuarios</span>
              </NuxtLink>
            </li>
            <li class="nav-item">
              <NuxtLink to="/admin/products" class="nav-link d-flex align-items-center" :class="{ 'active': $route.path === '/admin/products' }">
                <i class="bi bi-box me-3"></i>
                <span v-if="!sidebarCollapsed" class="fw-medium">Gestión de productos</span>
              </NuxtLink>
            </li>
            <li class="nav-item">
              <NuxtLink to="/admin/orders" class="nav-link d-flex align-items-center" :class="{ 'active': $route.path === '/admin/orders' }">
                <i class="bi bi-bag me-3"></i>
                <span v-if="!sidebarCollapsed" class="fw-medium">Gestión de pedidos</span>
              </NuxtLink>
            </li>
            <li class="nav-item">
              <NuxtLink to="/admin/chats" class="nav-link d-flex align-items-center" :class="{ 'active': $route.path === '/admin/chats' }">
                <i class="bi bi-chat-dots me-3"></i>
                <span v-if="!sidebarCollapsed" class="fw-medium">Gestión de chats</span>
              </NuxtLink>
            </li>
            <li class="nav-item">
              <NuxtLink to="/admin/tickets" class="nav-link d-flex align-items-center" :class="{ 'active': $route.path === '/admin/tickets' }">
                <i class="bi bi-ticket me-3"></i>
                <span v-if="!sidebarCollapsed" class="fw-medium">Asignación de tickets</span>
              </NuxtLink>
            </li>
            <li class="nav-item">
              <NuxtLink to="/admin/rag" class="nav-link d-flex align-items-center" :class="{ 'active': $route.path === '/admin/rag' }">
                <i class="bi bi-file-earmark-arrow-up me-3"></i>
                <span v-if="!sidebarCollapsed" class="fw-medium">Archivos para RAG</span>
              </NuxtLink>
            </li>
          </template>
          
          <!-- Menú para Atención al Cliente -->
          <template v-else-if="auth.user?.rol === 'atencion_cliente'">
            <li class="nav-item">
              <NuxtLink to="/atencion/tickets" class="nav-link d-flex align-items-center" :class="{ 'active': $route.path === '/atencion/tickets' }">
                <i class="bi bi-ticket me-3"></i>
                <span v-if="!sidebarCollapsed" class="fw-medium">Gestión de tickets</span>
              </NuxtLink>
            </li>
            <li class="nav-item">
              <NuxtLink to="/atencion/chats" class="nav-link d-flex align-items-center" :class="{ 'active': $route.path === '/atencion/chats' }">
                <i class="bi bi-chat-dots me-3"></i>
                <span v-if="!sidebarCollapsed" class="fw-medium">Chats en vivo</span>
              </NuxtLink>
            </li>
          </template>
        </ul>
      </div>
      
      <div class="sidebar-footer">
        <div class="nav-item">
          <button class="nav-link text-danger d-flex align-items-center" @click="logout">
            <i class="bi bi-box-arrow-right me-3"></i>
            <span v-if="!sidebarCollapsed" class="fw-medium">Cerrar sesión</span>
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
            <button class="btn btn-outline-secondary btn-sm me-4" @click="toggleSidebar">
              <i class="bi bi-list"></i>
            </button>
            <div class="page-title-section">
              <h4 class="mb-0 fw-bold">{{ pageTitle }}</h4>
              <small class="text-muted">
                {{ auth.user?.rol === 'administrador' ? 'Panel de administración' : 'Panel de atención al cliente' }}
              </small>
            </div>
          </div>
          <div class="d-flex align-items-center gap-3">
            <div class="user-info bg-light rounded px-3 py-2">
              <div class="d-flex align-items-center">
                <div class="user-avatar bg-primary text-white rounded-circle d-flex align-items-center justify-content-center me-2" style="width: 32px; height: 32px; font-size: 14px;">
                  {{ auth.userName?.charAt(0).toUpperCase() }}
                </div>
                <div>
                  <div class="fw-semibold text-dark">{{ auth.userName }}</div>
                  <small class="text-muted">
                    {{ auth.user?.rol === 'administrador' ? 'Administrador' : 'Atención al cliente' }}
                  </small>
                </div>
              </div>
            </div>
          </div>
        </div>
      </header>

      <!-- Page Content -->
      <main class="admin-content">
        <slot />
      </main>
    </div>
    
    <!-- Stock Notification (solo para admin) -->
    <StockNotification />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const route = useRoute()

// Theme management usando el plugin
const { $theme } = useNuxtApp()


// Sidebar management
const sidebarCollapsed = ref(false)

const toggleSidebar = () => {
  sidebarCollapsed.value = !sidebarCollapsed.value
}

// Page title based on route
const pageTitle = computed(() => {
  const titles: { [key: string]: string } = {
    '/admin/analytics': 'Analitica',
    '/admin/users': 'Gestión de usuarios',
    '/admin/products': 'Gestión de productos',
    '/admin/orders': 'Historial de pedidos',
    '/admin/chats': 'Historial de chats',
    '/admin/tickets': 'Gestión de tickets',
    '/admin/rag': 'Archivos para RAG',
    '/atencion/tickets': 'Gestión de tickets',
    '/atencion/chats': 'Chats en vivo'
  }
  return titles[route.path] || (auth.user?.rol === 'administrador' ? 'Administración' : 'Atención al cliente')
})

const logout = async () => {
  await auth.logout()
  await navigateTo('/login')
}
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  position: relative;
}

.admin-layout::before {
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
  z-index: -1;
}

.admin-sidebar {
  width: 280px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-right: 1px solid rgba(255, 255, 255, 0.2);
  display: flex;
  flex-direction: column;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: fixed;
  height: 100vh;
  z-index: 1000;
  box-shadow: 
    0 8px 32px rgba(102, 126, 234, 0.15),
    inset -1px 0 0 rgba(255, 255, 255, 0.1);
}

.admin-sidebar::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, transparent 100%);
  pointer-events: none;
}

.admin-sidebar.collapsed {
  width: 70px;
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
  border-radius: 8px;
  transition: all 0.3s ease;
  margin-bottom: 0.25rem;
  position: relative;
}

.nav-link:hover {
  background-color: var(--bs-gray-100);
  color: var(--bs-primary);
  transform: translateX(4px);
}

.nav-link.active {
  background: linear-gradient(135deg, var(--bs-primary) 0%, #0d6efd 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(13, 110, 253, 0.3);
}

.nav-link.active::before {
  content: '';
  position: absolute;
  left: -1rem;
  top: 50%;
  transform: translateY(-50%);
  width: 4px;
  height: 20px;
  background: var(--bs-primary);
  border-radius: 2px;
}

.nav-link i {
  width: 20px;
  text-align: center;
  font-size: 1.1rem;
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
  box-shadow: 0 2px 4px rgba(102, 126, 234, 0.15);
  backdrop-filter: blur(10px);
}

.page-title-section {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.user-info {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border: 1px solid var(--bs-border-color);
  transition: all 0.3s ease;
}

.user-info:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(102, 126, 234, 0.15);
}

.user-avatar {
  font-weight: 600;
  letter-spacing: 0.5px;
}

.admin-content {
  flex: 1;
  padding: 1.5rem;
  overflow-y: auto;
}

.user-info {
  font-size: 0.9rem;
}


/* Responsive */
@media (max-width: 768px) {
  .admin-sidebar {
    transform: translateX(-100%);
    position: fixed;
    z-index: 1050;
    height: 100vh;
  }
  
  .admin-sidebar.show {
    transform: translateX(0);
  }
  
  .admin-main {
    margin-left: 0 !important;
  }
  
  .admin-topbar {
    padding-left: 1rem;
  }
  
  .admin-topbar .btn {
    margin-right: 0.5rem;
  }
  
  .admin-topbar .user-info {
    font-size: 0.875rem;
  }
}

@media (max-width: 576px) {
  .admin-topbar h4 {
    font-size: 1.25rem;
  }
  
  .admin-topbar .d-flex {
    flex-wrap: wrap;
    gap: 0.5rem;
  }
  
  .admin-topbar .user-info {
    order: 2;
    width: 100%;
    justify-content: center;
  }
}
</style>

