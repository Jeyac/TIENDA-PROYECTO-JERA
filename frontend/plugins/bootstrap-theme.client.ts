import { defineNuxtPlugin } from '#app'

export default defineNuxtPlugin(() => {
  // Variables CSS para tema azul y celeste (solo modo claro)
  const blueTheme = {
    '--bs-primary': '#0d6efd',
    '--bs-primary-rgb': '13, 110, 253',
    '--bs-secondary': '#6c757d',
    '--bs-success': '#198754',
    '--bs-info': '#0dcaf0',
    '--bs-warning': '#ffc107',
    '--bs-danger': '#dc3545',
    '--bs-light': '#f8f9fa',
    '--bs-dark': '#212529',
    '--bs-body-bg': '#ffffff',
    '--bs-body-color': '#212529',
    '--bs-border-color': '#dee2e6',
    '--bs-link-color': '#0d6efd',
    '--bs-link-hover-color': '#0b5ed7',
    '--bs-card-bg': '#ffffff',
    '--bs-modal-bg': '#ffffff',
    '--bs-dropdown-bg': '#ffffff',
    '--bs-navbar-bg': '#ffffff',
    '--bs-table-bg': '#ffffff',
    '--bs-table-striped-bg': '#f8f9fa',
    '--bs-input-bg': '#ffffff',
    '--bs-input-border-color': '#ced4da',
    '--bs-btn-primary-bg': '#0d6efd',
    '--bs-btn-primary-border-color': '#0d6efd',
    '--bs-btn-primary-hover-bg': '#0b5ed7',
    '--bs-btn-primary-hover-border-color': '#0b5ed7',
    '--bs-btn-outline-primary-color': '#0d6efd',
    '--bs-btn-outline-primary-border-color': '#0d6efd',
    '--bs-btn-outline-primary-hover-bg': '#0d6efd',
    '--bs-btn-outline-primary-hover-border-color': '#0d6efd',
    '--bs-alert-primary-bg': '#d1ecf1',
    '--bs-alert-primary-border-color': '#bee5eb',
    '--bs-alert-primary-color': '#0c5460',
    '--bs-badge-primary-bg': '#0d6efd',
    '--bs-list-group-bg': '#ffffff',
    '--bs-list-group-border-color': '#dee2e6',
    '--bs-list-group-hover-bg': '#f8f9fa',
    '--bs-list-group-active-bg': '#0d6efd',
    '--bs-list-group-active-border-color': '#0d6efd'
  }

  // Función para aplicar tema
  const applyTheme = () => {
    const root = document.documentElement
    
    Object.entries(blueTheme).forEach(([property, value]) => {
      root.style.setProperty(property, value)
    })
  }

  // Aplicar tema inicial
  if (process.client) {
    applyTheme()
  }

  // CSS adicional para el tema azul y celeste
  const style = document.createElement('style')
  style.textContent = `
    /* Tema Azul y Celeste - Estilos adicionales */
    :root {
      --blue-gradient: linear-gradient(135deg, #0d6efd 0%, #0dcaf0 100%);
      --blue-shadow: 0 4px 15px rgba(13, 110, 253, 0.2);
      --blue-shadow-hover: 0 8px 25px rgba(13, 110, 253, 0.3);
    }

    /* Botones con gradiente azul */
    .btn-primary {
      background: var(--blue-gradient);
      border: none;
      box-shadow: var(--blue-shadow);
      transition: all 0.3s ease;
    }

    .btn-primary:hover {
      transform: translateY(-2px);
      box-shadow: var(--blue-shadow-hover);
    }

    /* Cards con sombra azul */
    .card {
      border: none;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
      transition: all 0.3s ease;
    }

    .card:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 25px rgba(13, 110, 253, 0.15);
    }

    /* Navbar con gradiente */
    .navbar {
      background: var(--blue-gradient) !important;
      box-shadow: var(--blue-shadow);
    }

    .navbar-brand, .navbar-nav .nav-link {
      color: white !important;
      font-weight: 500;
    }

    .navbar-nav .nav-link:hover {
      color: rgba(255, 255, 255, 0.8) !important;
    }

    /* Badges y alertas */
    .badge {
      font-weight: 500;
    }

    .alert {
      border: none;
      border-radius: 10px;
    }

    /* Animaciones suaves */
    * {
      transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
    }

    /* Scrollbar personalizado */
    ::-webkit-scrollbar {
      width: 8px;
    }

    ::-webkit-scrollbar-track {
      background: var(--bs-light);
    }

    ::-webkit-scrollbar-thumb {
      background: var(--bs-primary);
      border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
      background: var(--bs-btn-primary-hover-bg);
    }
  `
  
  if (process.client) {
    document.head.appendChild(style)
  }

  return {
    provide: {
      theme: {
        apply: applyTheme
      }
    }
  }
})
