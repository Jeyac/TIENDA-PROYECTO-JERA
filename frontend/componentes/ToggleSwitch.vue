<template>
  <div class="toggle-switch" :class="{ 'active': modelValue }" @click="toggle">
    <div class="toggle-slider">
      <div class="toggle-knob"></div>
    </div>
    <span class="toggle-label">{{ modelValue ? 'Activo' : 'Inactivo' }}</span>
  </div>
</template>

<script setup lang="ts">
interface Props {
  modelValue: boolean
  disabled?: boolean
}

interface Emits {
  (e: 'update:modelValue', value: boolean): void
}

const props = withDefaults(defineProps<Props>(), {
  disabled: false
})

const emit = defineEmits<Emits>()

const toggle = () => {
  if (!props.disabled) {
    emit('update:modelValue', !props.modelValue)
  }
}
</script>

<style scoped>
.toggle-switch {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  user-select: none;
}

.toggle-switch.disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.toggle-slider {
  position: relative;
  width: 50px;
  height: 24px;
  background-color: #dc3545;
  border-radius: 12px;
  transition: background-color 0.3s ease;
}

.toggle-switch.active .toggle-slider {
  background-color: #28a745;
}

.toggle-knob {
  position: absolute;
  top: 2px;
  left: 2px;
  width: 20px;
  height: 20px;
  background-color: white;
  border-radius: 50%;
  transition: transform 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.toggle-switch.active .toggle-knob {
  transform: translateX(26px);
}

.toggle-label {
  font-size: 14px;
  font-weight: 500;
  color: #6c757d;
  transition: color 0.3s ease;
}

.toggle-switch.active .toggle-label {
  color: #28a745;
}

.toggle-switch:not(.active) .toggle-label {
  color: #dc3545;
}
</style>




