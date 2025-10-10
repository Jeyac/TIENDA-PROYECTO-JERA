<template>
  <div class="text-center py-5">
    <InlineSpinner />
    <p class="text-muted mt-2">Redirigiendo al panel de administración...</p>
  </div>
</template>

<script setup lang="ts">
// Middleware
definePageMeta({
  middleware: ['auth', 'admin'],
  layout: 'admin'
})

// Redirigir automáticamente a analytics
onMounted(() => {
  navigateTo('/admin/analytics')
})
</script>
