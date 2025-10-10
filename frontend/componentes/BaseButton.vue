<template>
  <button
    :type="type"
    class="btn btn-modern"
    :class="variantClass"
    :disabled="disabled || loading"
    v-bind="$attrs"
    @click="$emit('click', $event)"
  >
    <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
    <slot />
  </button>
  
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  variant?: string
  type?: 'button' | 'submit' | 'reset'
  disabled?: boolean
  loading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  type: 'button',
  disabled: false,
  loading: false
})

const variantClass = computed(() => `btn-${props.variant}`)
</script>





