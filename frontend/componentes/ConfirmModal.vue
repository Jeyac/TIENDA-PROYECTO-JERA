<template>
  <div>
    <div class="modal fade" :class="{ show: modelValue }" :style="{ display: modelValue ? 'block' : 'none' }" tabindex="-1">
      <div class="modal-dialog" :class="sizeClass">
        <div class="modal-content">
          <div class="modal-header" v-if="title || $slots.title">
            <h5 class="modal-title">
              <slot name="title">{{ title }}</slot>
            </h5>
            <button type="button" class="btn-close" @click="emit('update:modelValue', false)"></button>
          </div>
          <div class="modal-body">
            <slot>
              <p class="mb-0">{{ message }}</p>
            </slot>
          </div>
          <div class="modal-footer">
            <BaseButton :variant="cancelVariant" @click="emit('update:modelValue', false)" :disabled="loading">
              {{ cancelText }}
            </BaseButton>
            <BaseButton :variant="confirmVariant" @click="emit('confirm')" :loading="loading" :disabled="loading">
              {{ confirmText }}
            </BaseButton>
          </div>
        </div>
      </div>
    </div>
    <div v-if="modelValue" class="modal-backdrop fade show"></div>
  </div>
  
</template>

<script setup lang="ts">
interface Props {
  modelValue: boolean
  title?: string
  message?: string
  confirmText?: string
  cancelText?: string
  confirmVariant?: string
  cancelVariant?: string
  size?: 'sm' | 'md' | 'lg'
  loading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: false,
  title: '',
  message: '',
  confirmText: 'Confirmar',
  cancelText: 'Cancelar',
  confirmVariant: 'primary',
  cancelVariant: 'secondary',
  size: 'md',
  loading: false
})

const emit = defineEmits(['update:modelValue', 'confirm'])

const sizeClass = computed(() => ({
  'modal-sm': props.size === 'sm',
  'modal-lg': props.size === 'lg'
}))
</script>




