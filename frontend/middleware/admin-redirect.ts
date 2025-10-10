export default defineNuxtRouteMiddleware((to) => {
  const auth = useAuthStore()
  
  // Solo ejecutar en el cliente
  if (process.client) {
    // Si el usuario está autenticado y es administrador
    if (auth.isAuthenticated && auth.user?.rol === 'administrador') {
      // Si no está en una página de admin, redirigir
      if (!to.path.startsWith('/admin')) {
        return navigateTo('/admin/analytics')
      }
    }
    
    // Si el usuario está autenticado y es atención al cliente
    if (auth.isAuthenticated && auth.user?.rol === 'atencion_cliente') {
      // Si no está en una página de atención, redirigir
      if (!to.path.startsWith('/atencion')) {
        return navigateTo('/atencion/tickets')
      }
    }
    
    // Si el usuario está autenticado y es usuario normal
    if (auth.isAuthenticated && auth.user?.rol === 'usuario') {
      // Si está en páginas de admin o atención, redirigir
      if (to.path.startsWith('/admin') || to.path.startsWith('/atencion')) {
        return navigateTo('/profile')
      }
    }
  }
})

