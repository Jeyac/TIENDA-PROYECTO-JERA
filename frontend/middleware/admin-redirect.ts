export default defineNuxtRouteMiddleware((to) => {
  const auth = useAuthStore()
  
  // Solo ejecutar en el cliente
  if (typeof window === 'undefined') return
  
  // Si el usuario es admin y está en la página principal, redirigir al dashboard de admin
  if (auth.isAuthenticated && auth.isAdmin && to.path === '/') {
    return navigateTo('/admin-redirect')
  }
})
