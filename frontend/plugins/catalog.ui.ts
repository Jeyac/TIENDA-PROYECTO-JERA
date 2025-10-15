import { defineNuxtPlugin } from '#app'

export default defineNuxtPlugin(() => {
  const catalogUi = {
    card: 'product-card',
    badgeCategory: 'badge bg-secondary',
    btnAdd: 'btn btn-primary'
  }
  return { provide: { catalogUi } }
})







