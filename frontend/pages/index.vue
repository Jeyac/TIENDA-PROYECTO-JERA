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
            <NuxtLink to="/catalogo">
              <BaseButton variant="primary" class="btn-lg px-4">
                <i class="bi bi-grid me-2"></i>Ver catálogo
              </BaseButton>
            </NuxtLink>
            <NuxtLink to="/soporte">
              <BaseButton variant="outline-primary" class="btn-lg px-4">
                <i class="bi bi-chat-dots me-2"></i>Soporte
              </BaseButton>
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
        <SectionTitle>
          <template #default>
            <i class="bi bi-question-circle me-2"></i>Preguntas frecuentes
          </template>
        </SectionTitle>
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

// Middleware para redirección automática según rol
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
  background: 
    linear-gradient(135deg, rgba(255, 255, 255, 0.85) 0%, rgba(13, 110, 253, 0.1) 100%),
    url('~/public/images/infinite-finds-background.jpeg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  background-attachment: fixed;
  padding: 4rem 0;
  margin-bottom: 2rem;
  position: relative;
  overflow: hidden;
}

/* Responsividad mejorada para móviles */
@media (max-width: 768px) {
  .hero-section {
    padding: 2rem 0;
    background-attachment: scroll; /* Mejor rendimiento en móviles */
  }
  
  .hero-section h1 {
    font-size: 2rem !important;
  }
  
  .hero-section .lead {
    font-size: 1rem;
  }
  
  .hero-section .d-flex {
    flex-direction: column;
    gap: 1rem;
  }
  
  .hero-section .btn-lg {
    width: 100%;
  }
}

@media (max-width: 576px) {
  .hero-section {
    padding: 1.5rem 0;
  }
  
  .hero-section h1 {
    font-size: 1.75rem !important;
  }
  
  .hero-image {
    padding: 1rem;
  }
  
  .hero-image i {
    font-size: 3rem !important;
  }
}

/* Efecto de overlay adicional para mejor legibilidad */
.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(13, 110, 253, 0.05) 100%);
  pointer-events: none;
  z-index: 1;
}

/* Asegurar que el contenido esté por encima del overlay */
.hero-section .container {
  position: relative;
  z-index: 2;
}

.min-vh-50 {
  min-height: 50vh;
}

.hero-image {
  text-align: center;
  padding: 2rem;
}

.hero-image i {
  opacity: 0.9;
  animation: float 3s ease-in-out infinite;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Mejorar legibilidad del texto sobre la imagen de fondo */
.hero-section h1 {
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.hero-section .lead {
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
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


