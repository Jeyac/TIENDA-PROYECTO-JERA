export default defineNuxtRouteMiddleware((to) => {
  const auth = useAuthStore()
  
  // Check if user is authenticated
  if (!auth.isAuthenticated) {
    return navigateTo('/login')
  }
  
  // Check if user is admin
  if (!auth.isAdmin) {
    throw createError({
      statusCode: 403,
      statusMessage: 'Acceso denegado. Se requieren permisos de administrador.'
    })
  }
})
