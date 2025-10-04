<template>
  <div class="hero-section">
    <div class="container">
      <div class="row align-items-center min-vh-50">
        <div class="col-lg-6">
          <h1 class="display-4 fw-bold mb-4">
            Bienvenido a <span class="text-primary">Infinite Finds</span>
          </h1>
          <p class="lead mb-4">
            Descubre una experiencia de compra única con productos de calidad y atención personalizada.
            Explora nuestro catálogo o recibe ayuda instantánea con nuestro soporte especializado.
          </p>
          <div class="d-flex gap-3">
            <NuxtLink to="/catalogo" class="btn btn-primary btn-lg px-4">
              <i class="bi bi-grid me-2"></i>Ver Catálogo
            </NuxtLink>
            <NuxtLink to="/soporte" class="btn btn-outline-primary btn-lg px-4">
              <i class="bi bi-chat-dots me-2"></i>Soporte
            </NuxtLink>
          </div>
        </div>
        <div class="col-lg-6">
          <div class="hero-image">
            <i class="bi bi-shop display-1 text-primary"></i>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="container my-5">
    <div class="row">
      <div class="col-12">
        <h2 class="text-center mb-5">
          <i class="bi bi-question-circle me-2"></i>Preguntas Frecuentes
        </h2>
        <div class="row">
          <div class="col-lg-8 mx-auto">
            <div class="accordion" id="faqAccordion">
              <div v-for="(f, index) in faqs" :key="f.pregunta" class="accordion-item">
                <h2 class="accordion-header">
                  <button 
                    class="accordion-button" 
                    :class="{ collapsed: index !== 0 }"
                    type="button" 
                    :data-bs-toggle="'collapse'" 
                    :data-bs-target="`#faq${index}`"
                    :aria-expanded="index === 0 ? 'true' : 'false'"
                    :aria-controls="`faq${index}`"
                  >
                    {{ f.pregunta }}
                  </button>
                </h2>
                <div 
                  :id="`faq${index}`" 
                  class="accordion-collapse collapse" 
                  :class="{ show: index === 0 }"
                  :data-bs-parent="'#faqAccordion'"
                >
                  <div class="accordion-body">
                    {{ f.respuesta }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRuntimeConfig } from 'nuxt/app'

// Middleware para redirigir admin al dashboard
definePageMeta({
  middleware: 'admin-redirect'
})

const config = useRuntimeConfig()
const faqs = ref<{pregunta: string, respuesta: string}[]>([])

onMounted(async () => {
  try {
    const res = await fetch(`${config.public.apiBase}/api/faq/`)
    if (res.ok) {
      faqs.value = await res.json()
    }
  } catch {}
})
</script>

<style scoped>
.hero-section {
  background: linear-gradient(135deg, var(--bs-light) 0%, var(--bs-primary-bg-subtle) 100%);
  padding: 4rem 0;
  margin-bottom: 2rem;
}

.min-vh-50 {
  min-height: 50vh;
}

.hero-image {
  text-align: center;
  padding: 2rem;
}

.hero-image i {
  opacity: 0.8;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
}

.accordion-item {
  border: 1px solid var(--bs-border-color);
  margin-bottom: 0.5rem;
  border-radius: 0.5rem;
  overflow: hidden;
}

.accordion-button {
  background-color: var(--bs-body-bg);
  border: none;
  font-weight: 500;
}

.accordion-button:not(.collapsed) {
  background-color: var(--bs-primary-bg-subtle);
  color: var(--bs-primary);
}

.accordion-button:focus {
  box-shadow: 0 0 0 0.25rem rgba(var(--bs-primary-rgb), 0.25);
}

.accordion-body {
  background-color: var(--bs-body-bg);
  color: var(--bs-body-color);
}
</style>


