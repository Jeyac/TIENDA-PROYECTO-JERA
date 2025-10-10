<template>
  <div class="text-center py-5">
    <i :class="icon" class="text-muted" :style="{ fontSize: iconSize }"></i>
    <h3 class="text-muted mt-3">{{ title }}</h3>
    <p v-if="subtitle" class="text-muted">{{ subtitle }}</p>
    <div v-if="$slots.actions" class="mt-3">
      <slot name="actions" />
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  icon?: string
  title: string
  subtitle?: string
  size?: 'lg' | 'xl'
}

const props = withDefaults(defineProps<Props>(), {
  icon: 'bi bi-inbox',
  size: 'xl'
})

const iconSize = computed(() => props.size === 'xl' ? '4rem' : '3rem')
</script>




