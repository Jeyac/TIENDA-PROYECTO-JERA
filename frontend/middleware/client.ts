export default defineNuxtRouteMiddleware((to, from) => {
  const auth = useAuthStore()
  
  // Verificar que esté autenticado
  if (!auth.isAuthenticated) {
    return navigateTo('/login')
  }
  
  // Verificar que sea cliente (no administrador)
  if (auth.isAdmin) {
    throw createError({
      statusCode: 403,
      statusMessage: 'Los administradores no pueden acceder a esta página desde el panel de administración.'
    })
  }
})



