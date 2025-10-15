<template>
  <div :class="['avatar-circle', bgClass, 'text-white', sizeClass]">
    {{ initial }}
  </div>
</template>

<script setup lang="ts">
interface Props {
  text?: string
  size?: 'sm' | 'md' | 'lg'
  color?: 'primary' | 'secondary' | 'success' | 'danger' | 'info' | 'warning'
}

const props = withDefaults(defineProps<Props>(), {
  text: 'U',
  size: 'md',
  color: 'primary'
})

const initial = computed(() => (props.text || 'U').charAt(0).toUpperCase())
const sizeClass = computed(() => ({
  'avatar-sm': props.size === 'sm',
  'avatar-md': props.size === 'md',
  'avatar-lg': props.size === 'lg'
}))
const bgClass = computed(() => `bg-${props.color}`)
</script>

<style scoped>
.avatar-circle {
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  font-weight: bold;
}
.avatar-sm { width: 32px; height: 32px; font-size: 0.875rem; }
.avatar-md { width: 40px; height: 40px; font-size: 1rem; }
.avatar-lg { width: 48px; height: 48px; font-size: 1.125rem; }
</style>










