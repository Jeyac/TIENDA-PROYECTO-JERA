<template>
  <div class="input-group">
    <input
      :value="modelValue"
      @input="onInput"
      type="text"
      class="form-control"
      :placeholder="placeholder"
    >
    <BaseButton :variant="buttonVariant" type="button" @click="emit('search')">
      <i :class="icon"></i>
    </BaseButton>
  </div>
</template>

<script setup lang="ts">
interface Props {
  modelValue: string
  placeholder?: string
  icon?: string
  buttonVariant?: string
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: '',
  placeholder: 'Buscar...',
  icon: 'bi bi-search',
  buttonVariant: 'outline-secondary'
})

const emit = defineEmits(['update:modelValue', 'search'])

const onInput = (e: Event) => {
  const target = e.target as HTMLInputElement
  emit('update:modelValue', target.value)
}
</script>




