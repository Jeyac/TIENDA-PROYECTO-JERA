<template>
  <div class="container py-4">
    <h1 class="h4 mb-3"><i class="bi bi-person me-2"></i>Mi perfil</h1>
    <div class="card border-0 shadow-sm">
      <div class="card-body">
        <p class="mb-1"><strong>Nombre:</strong> {{ auth.userName }}</p>
        <p class="mb-3"><strong>Email:</strong> {{ auth.userEmail }}</p>
        <BaseButton variant="primary" @click="logout">
          <i class="bi bi-box-arrow-right me-2"></i>Cerrar sesión
        </BaseButton>
      </div>
    </div>
  </div>
  
</template>

<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'

definePageMeta({ 
  middleware: ['user-only'],
  layout: 'default' 
})

const auth = useAuthStore()

const logout = async () => {
  await auth.logout()
}
</script>



