<template>
  <div v-if="showNotification" class="stock-notification">
    <div class="alert alert-info d-flex align-items-center" role="alert">
      <i class="bi bi-info-circle me-2"></i>
      <div>
        <strong>Stock actualizado:</strong> {{ message }}
      </div>
      <button type="button" class="btn-close ms-auto" @click="closeNotification"></button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const showNotification = ref(false)
const message = ref('')

const closeNotification = () => {
  showNotification.value = false
}

const showStockUpdate = (msg: string) => {
  message.value = msg
  showNotification.value = true
  
  // Auto-hide after 5 seconds
  setTimeout(() => {
    closeNotification()
  }, 5000)
}

onMounted(() => {
  // Escuchar eventos de actualización de stock
  if (typeof window !== 'undefined') {
    window.addEventListener('stockActualizado', (event: any) => {
      showStockUpdate(event.detail.message)
    })
  }
})

onUnmounted(() => {
  if (typeof window !== 'undefined') {
    window.removeEventListener('stockActualizado', () => {})
  }
})
</script>

<style scoped>
.stock-notification {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1050;
  max-width: 400px;
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}
</style>
