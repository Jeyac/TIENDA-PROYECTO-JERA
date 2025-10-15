import { defineNuxtPlugin } from '#app'

export default defineNuxtPlugin(() => {
  // Agregar estilos modernos globalmente
  if (process.client) {
    // Crear link element para el CSS
    const link = document.createElement('link')
    link.rel = 'stylesheet'
    link.href = '/css/modern-design.css'
    document.head.appendChild(link)
    
    // Agregar clases modernas a elementos existentes
    const addModernClasses = () => {
      // Mejorar botones
      document.querySelectorAll('.btn').forEach(btn => {
        if (!btn.classList.contains('btn-modern')) {
          btn.classList.add('btn-modern')
        }
      })
      
      // Mejorar formularios
      document.querySelectorAll('.form-control').forEach(input => {
        if (!input.classList.contains('form-control-modern')) {
          input.classList.add('form-control-modern')
        }
      })
      
      // Mejorar tablas
      document.querySelectorAll('.table').forEach(table => {
        if (!table.classList.contains('table-modern')) {
          table.classList.add('table-modern')
        }
      })
      
      // Mejorar badges
      document.querySelectorAll('.badge').forEach(badge => {
        if (!badge.classList.contains('badge-modern')) {
          badge.classList.add('badge-modern')
        }
      })
    }
    
    // Aplicar estilos cuando el DOM esté listo
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', addModernClasses)
    } else {
      addModernClasses()
    }
    
    // Observar cambios en el DOM para aplicar estilos a elementos nuevos
    const observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        mutation.addedNodes.forEach((node) => {
          if (node.nodeType === Node.ELEMENT_NODE) {
            const element = node as Element
            
            // Aplicar estilos a elementos nuevos
            element.querySelectorAll('.btn').forEach(btn => {
              if (!btn.classList.contains('btn-modern')) {
                btn.classList.add('btn-modern')
              }
            })
            
            element.querySelectorAll('.form-control').forEach(input => {
              if (!input.classList.contains('form-control-modern')) {
                input.classList.add('form-control-modern')
              }
            })
            
            element.querySelectorAll('.table').forEach(table => {
              if (!table.classList.contains('table-modern')) {
                table.classList.add('table-modern')
              }
            })
            
            element.querySelectorAll('.badge').forEach(badge => {
              if (!badge.classList.contains('badge-modern')) {
                badge.classList.add('badge-modern')
              }
            })
          }
        })
      })
    })
    
    observer.observe(document.body, {
      childList: true,
      subtree: true
    })
  }
})






