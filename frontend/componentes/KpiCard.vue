<template>
  <div class="col-md-3">
    <div class="card kpi-card" :class="$analyticsUi?.kpiCard || 'border-0 shadow-sm'">
      <div class="card-body text-center">
        <div class="kpi-icon" :class="[$analyticsUi?.kpiIcon || 'rounded-circle mx-auto mb-3', bgClass]">
          <i :class="icon"></i>
        </div>
        <h3 class="fw-bold" :class="textClass">{{ value }}</h3>
        <p class="text-muted mb-0">{{ label }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  icon: string
  label: string
  value: string | number
  color?: 'primary' | 'success' | 'info' | 'warning' | 'secondary'
}

const props = withDefaults(defineProps<Props>(), {
  color: 'primary'
})

const bgClass = computed(() => `bg-${props.color} text-white`)
const textClass = computed(() => `text-${props.color}`)
</script>

<style scoped>
.kpi-card .kpi-icon {
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}
</style>


