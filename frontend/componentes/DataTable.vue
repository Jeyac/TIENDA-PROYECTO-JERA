<template>
  <div class="table-responsive">
    <table class="table table-hover mb-0">
      <thead class="table-light">
        <tr>
          <th v-for="col in columns" :key="col.key">{{ col.label }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in pagedItems" :key="rowKey(row)">
          <slot name="row" :row="row" />
        </tr>
      </tbody>
    </table>
    <div v-if="items.length === 0" class="p-4">
      <EmptyState :icon="emptyIcon" :title="emptyTitle" :subtitle="emptySubtitle" />
    </div>
    <div class="d-flex justify-content-center py-3">
      <Paginator :total-items="items.length" :page-size="pageSize" v-model="page" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'

interface Column { key: string; label: string }
interface Props {
  items: any[]
  columns: Column[]
  pageSize?: number
  rowKey?: (row: any) => string | number
  emptyIcon?: string
  emptyTitle?: string
  emptySubtitle?: string
}

const props = withDefaults(defineProps<Props>(), {
  pageSize: 10,
  rowKey: (row: any) => row.id,
  emptyIcon: 'bi bi-inbox',
  emptyTitle: 'Sin resultados',
  emptySubtitle: 'No hay datos para mostrar'
})

const page = ref(1)
const pagedItems = computed(() => {
  const start = (page.value - 1) * props.pageSize
  return props.items.slice(start, start + props.pageSize)
})

const rowKey = (row: any) => props.rowKey!(row)
</script>




