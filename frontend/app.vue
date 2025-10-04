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
  color: var(--bs-body-color);
  background-color: var(--bs-body-bg);
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

/* Custom CSS variables for theming */
:root {
  --bs-primary-rgb: 13, 110, 253;
  --bs-secondary-rgb: 108, 117, 125;
  --bs-success-rgb: 25, 135, 84;
  --bs-danger-rgb: 220, 53, 69;
  --bs-warning-rgb: 255, 193, 7;
  --bs-info-rgb: 13, 202, 240;
  --bs-light-rgb: 248, 249, 250;
  --bs-dark-rgb: 33, 37, 41;
}

/* Dark theme variables */
.dark-theme {
  --bs-body-bg: #1a1a1a;
  --bs-body-color: #e9ecef;
  --bs-gray-100: #2d2d2d;
  --bs-gray-200: #3d3d3d;
  --bs-gray-300: #4d4d4d;
  --bs-gray-400: #6c757d;
  --bs-gray-500: #adb5bd;
  --bs-gray-600: #ced4da;
  --bs-gray-700: #dee2e6;
  --bs-gray-800: #e9ecef;
  --bs-gray-900: #f8f9fa;
  --bs-border-color: #495057;
  --bs-border-color-translucent: rgba(255, 255, 255, 0.15);
}
</style>


