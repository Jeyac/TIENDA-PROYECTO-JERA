<template>
  <div class="atencion-layout">
    <!-- Sidebar -->
    <aside class="sidebar" :class="{ 'sidebar-collapsed': sidebarCollapsed }">
      <div class="sidebar-header">
        <h5 class="m-0">
          <i class="bi bi-headset me-2"></i>
          <span v-if="!sidebarCollapsed">Atención al cliente</span>
        </h5>
        <button @click="sidebarCollapsed = !sidebarCollapsed" class="btn btn-sm btn-ghost">
          <i class="bi" :class="sidebarCollapsed ? 'bi-chevron-right' : 'bi-chevron-left'"></i>
        </button>
      </div>

      <nav class="sidebar-nav">
        <NuxtLink to="/atencion/tickets" class="nav-item">
          <i class="bi bi-ticket-perforated"></i>
          <span v-if="!sidebarCollapsed">Tickets asignados</span>
        </NuxtLink>

        <div class="nav-divider" v-if="!sidebarCollapsed"></div>

        <button @click="handleLogout" class="nav-item text-danger">
          <i class="bi bi-box-arrow-right"></i>
          <span v-if="!sidebarCollapsed">Cerrar sesión</span>
        </button>
      </nav>
    </aside>

    <!-- Main Content -->
    <div class="main-content">
      <!-- Top Bar -->
      <header class="topbar">
        <div class="d-flex justify-content-between align-items-center w-100">
          <div>
            <h4 class="mb-0">Tickets asignados</h4>
          </div>
          <div class="d-flex align-items-center gap-2">
            <div class="user-info">
              <i class="bi bi-person-circle me-2"></i>
              <span>{{ auth.user?.username || 'Usuario' }}</span>
            </div>
          </div>
        </div>
      </header>

      <!-- Page Content -->
      <main class="page-content">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '~/stores/auth'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

const sidebarCollapsed = ref(false)

// Theme management usando el plugin
const { $theme } = useNuxtApp()

const handleLogout = async () => {
  await auth.logout()
  router.push('/login')
}
</script>

<style scoped>
.atencion-layout {
  display: flex;
  min-height: 100vh;
  background-color: var(--bs-gray-100);
}

.sidebar {
  width: 250px;
  background: linear-gradient(180deg, #4f46e5 0%, #4338ca 100%);
  color: white;
  display: flex;
  flex-direction: column;
  transition: width 0.3s ease;
  position: fixed;
  height: 100vh;
  overflow-y: auto;
  z-index: 1000;
}

.sidebar-collapsed {
  width: 70px;
}

.sidebar-header {
  padding: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.sidebar-nav {
  flex: 1;
  padding: 1rem 0;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1.5rem;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  transition: all 0.2s;
  border: none;
  background: none;
  width: 100%;
  text-align: left;
  cursor: pointer;
}

.nav-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
  color: white;
}

.nav-item.router-link-active {
  background-color: rgba(255, 255, 255, 0.15);
  color: white;
  border-left: 3px solid white;
}

.nav-item i {
  font-size: 1.25rem;
  min-width: 1.25rem;
}

.nav-divider {
  height: 1px;
  background-color: rgba(255, 255, 255, 0.1);
  margin: 1rem 1.5rem;
}

.main-content {
  flex: 1;
  margin-left: 250px;
  transition: margin-left 0.3s ease;
}

.sidebar-collapsed + .main-content {
  margin-left: 70px;
}

.topbar {
  background-color: white;
  padding: 1rem 2rem;
  border-bottom: 1px solid var(--bs-border-color);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.user-info {
  padding: 0.5rem 1rem;
  background-color: var(--bs-gray-100);
  border-radius: 0.5rem;
  font-size: 0.875rem;
}

.page-content {
  padding: 2rem;
  min-height: calc(100vh - 73px);
}

.btn-ghost {
  background: none;
  border: none;
  color: white;
  padding: 0.25rem 0.5rem;
}

.btn-ghost:hover {
  background-color: rgba(255, 255, 255, 0.1);
}


/* Responsive */
@media (max-width: 768px) {
  .sidebar {
    transform: translateX(-100%);
    position: fixed;
    z-index: 1050;
    height: 100vh;
  }
  
  .sidebar.show {
    transform: translateX(0);
  }
  
  .main-content {
    margin-left: 0 !important;
  }
  
  .topbar {
    padding-left: 1rem;
  }
  
  .topbar h4 {
    font-size: 1.25rem;
  }
  
  .topbar .user-info {
    font-size: 0.875rem;
  }
}

@media (max-width: 576px) {
  .topbar .d-flex {
    flex-direction: column;
    align-items: flex-start !important;
    gap: 0.5rem;
  }
  
  .topbar h4 {
    font-size: 1.1rem;
  }
  
  .topbar .user-info {
    font-size: 0.8rem;
  }
}
</style>


