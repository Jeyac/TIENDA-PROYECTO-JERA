<template>
  <span class="order-status-badge" :class="statusClass">
    <i :class="statusIcon"></i>
    {{ statusText }}
  </span>
</template>

<script setup lang="ts">
interface Props {
  status: string
  text?: string
}

const props = withDefaults(defineProps<Props>(), {
  text: undefined
})

const statusClass = computed(() => {
  const status = props.status?.toLowerCase() || ''
  return {
    'order-pending': status === 'pendiente',
    'order-processing': status === 'en_proceso' || status === 'en proceso',
    'order-completed': status === 'completado',
    'order-cancelled': status === 'cancelado',
    'order-shipped': status === 'enviado',
    'order-delivered': status === 'entregado'
  }
})

const statusText = computed(() => 
  props.text || props.status || 'Desconocido'
)

const statusIcon = computed(() => {
  const status = props.status?.toLowerCase() || ''
  switch (status) {
    case 'pendiente':
      return 'bi bi-clock'
    case 'en_proceso':
    case 'en proceso':
      return 'bi bi-gear'
    case 'completado':
      return 'bi bi-check-circle-fill'
    case 'cancelado':
      return 'bi bi-x-circle-fill'
    case 'enviado':
      return 'bi bi-truck'
    case 'entregado':
      return 'bi bi-house-check'
    default:
      return 'bi bi-question-circle'
  }
})
</script>

<style scoped>
.order-status-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.order-pending {
  background-color: #fff3cd;
  color: #856404;
  border: 1px solid #ffeaa7;
}

.order-processing {
  background-color: #cce5ff;
  color: #004085;
  border: 1px solid #99d6ff;
}

.order-completed {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.order-cancelled {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.order-shipped {
  background-color: #e2e3e5;
  color: #383d41;
  border: 1px solid #d6d8db;
}

.order-delivered {
  background-color: #d1ecf1;
  color: #0c5460;
  border: 1px solid #bee5eb;
}

.order-status-badge i {
  font-size: 10px;
}
</style>




