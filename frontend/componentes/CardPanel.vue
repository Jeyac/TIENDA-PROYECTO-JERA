<template>
  <div class="card border-0 shadow-sm h-100">
    <div v-if="$slots.header" class="card-header bg-white border-bottom d-flex align-items-center justify-content-between">
      <slot name="header" />
    </div>
    <div class="card-body">
      <slot />
    </div>
    <div v-if="$slots.footer" class="card-footer bg-white border-top">
      <slot name="footer" />
    </div>
  </div>
</template>

<script setup lang="ts">
</script>




