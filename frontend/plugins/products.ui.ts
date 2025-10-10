import { defineNuxtPlugin } from '#app'

export default defineNuxtPlugin(() => {
  const productsUi = {
    thumb: 'img-thumbnail',
    placeholder: 'placeholder-image',
    price: 'text-primary',
  }
  return { provide: { productsUi } }
})





