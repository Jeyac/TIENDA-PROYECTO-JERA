<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>

<script setup lang="ts">
</script>

<style>
/* Global styles */
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  line-height: 1.6;
}

/* Smooth scrolling */
html {
  scroll-behavior: smooth;
}

/* Focus styles */
*:focus {
  outline: 2px solid var(--bs-primary);
  outline-offset: 2px;
}
</style>


