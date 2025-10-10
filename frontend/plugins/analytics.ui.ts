import { defineNuxtPlugin } from '#app'

export default defineNuxtPlugin(() => {
  const analyticsClasses = {
    kpiIcon: 'rounded-circle mx-auto mb-3',
    kpiCard: 'border-0 shadow-sm',
    listIcon: 'text-muted',
  }

  return {
    provide: {
      analyticsUi: analyticsClasses
    }
  }
})





