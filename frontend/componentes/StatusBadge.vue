<template>
  <span class="status-badge" :class="statusClass">
    <i :class="statusIcon"></i>
    {{ statusText }}
  </span>
</template>

<script setup lang="ts">
interface Props {
  status: 'activo' | 'inactivo'
}

const props = defineProps<Props>()

const statusClass = computed(() => ({
  'status-active': props.status === 'activo',
  'status-inactive': props.status === 'inactivo'
}))

const statusText = computed(() => 
  props.status === 'activo' ? 'Activo' : 'Inactivo'
)

const statusIcon = computed(() => 
  props.status === 'activo' ? 'bi bi-check-circle-fill' : 'bi bi-x-circle-fill'
)
</script>

<style scoped>
.status-badge {
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

.status-active {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.status-inactive {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.status-badge i {
  font-size: 10px;
}
</style>