// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  pages: true,
  modules: ['@pinia/nuxt'],
  components: [
    { path: '~/componentes', pathPrefix: false }
  ],
  css: [
    'bootstrap/dist/css/bootstrap.min.css',
    'bootstrap-icons/font/bootstrap-icons.css'
  ],
  plugins: [
    { src: '~/plugins/bootstrap.client', mode: 'client' },
    { src: '~/plugins/bootstrap-theme.client', mode: 'client' },
    { src: '~/plugins/ui.helpers', mode: 'client' },
    { src: '~/plugins/fetch-logger.client', mode: 'client' },
    { src: '~/plugins/auth.client', mode: 'client' },
    { src: '~/plugins/carrito.client', mode: 'client' }
  ],
  runtimeConfig: {
    public: {
      apiBase: 'http://localhost:5000',
      jwtRefreshInterval: Number(process.env.JWT_REFRESH_INTERVAL), // segundos
      jwtRefreshThreshold: Number(process.env.JWT_REFRESH_THRESHOLD) // segundos antes de expirar
    }
  },
  nitro: {
    devProxy: {
      '/uploads': {
        target: 'http://localhost:5000/uploads',
        changeOrigin: true
      }
    }
  }
})
