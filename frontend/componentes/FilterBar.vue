<template>
  <div class="row g-3 align-items-end">
    <div class="col-md-8">
      <SearchBar v-model="search" :placeholder="placeholder" @search="emit('search', search)" />
    </div>
    <div class="col-md-4">
      <div class="d-flex gap-2">
        <slot />
        <BaseButton variant="outline-secondary" class="flex-fill" @click="emit('clear')">
          <i class="bi bi-x-circle me-2"></i>Limpiar filtros
        </BaseButton>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = withDefaults(defineProps<{ modelValue: string; placeholder?: string }>(), {
  modelValue: '',
  placeholder: 'Buscar...'
})

const emit = defineEmits(['update:modelValue', 'search', 'clear'])

const search = computed({
  get: () => props.modelValue,
  set: (v: string) => emit('update:modelValue', v)
})
</script>



