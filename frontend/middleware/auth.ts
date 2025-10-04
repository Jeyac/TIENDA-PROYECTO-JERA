export default defineNuxtRouteMiddleware((to) => {
  const auth = useAuthStore()
  
  if (!auth.isAuthenticated) {
    return navigateTo(`/login?next=${to.fullPath}`)
  }
})
