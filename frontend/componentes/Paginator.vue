<template>
  <nav v-if="totalPages > 1" aria-label="Paginación">
    <ul class="pagination mb-0">
      <li class="page-item" :class="{ disabled: currentPage <= 1 }">
        <a class="page-link" href="#" @click.prevent="goTo(currentPage - 1)">Anterior</a>
      </li>
      <li v-for="p in pages" :key="p" class="page-item" :class="{ active: p === currentPage }">
        <a class="page-link" href="#" @click.prevent="goTo(p)">{{ p }}</a>
      </li>
      <li class="page-item" :class="{ disabled: currentPage >= totalPages }">
        <a class="page-link" href="#" @click.prevent="goTo(currentPage + 1)">Siguiente</a>
      </li>
    </ul>
  </nav>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  totalItems: number
  pageSize?: number
  modelValue: number
}

const props = withDefaults(defineProps<Props>(), {
  pageSize: 10,
  modelValue: 1
})

const emit = defineEmits(['update:modelValue'])

const totalPages = computed(() => Math.max(1, Math.ceil(props.totalItems / props.pageSize)))
const currentPage = computed(() => Math.min(props.modelValue, totalPages.value))
const pages = computed(() => {
  const arr: number[] = []
  for (let i = 1; i <= totalPages.value; i++) arr.push(i)
  return arr
})

const goTo = (p: number) => {
  if (p < 1 || p > totalPages.value || p === currentPage.value) return
  emit('update:modelValue', p)
}
</script>




