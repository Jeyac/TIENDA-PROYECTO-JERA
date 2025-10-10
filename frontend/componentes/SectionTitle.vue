<template>
  <div class="d-flex align-items-center justify-content-between mb-3">
    <h5 class="card-title mb-0">
      <slot />
    </h5>
    <div v-if="$slots.actions">
      <slot name="actions" />
    </div>
  </div>
</template>

<script setup lang="ts">
</script>




