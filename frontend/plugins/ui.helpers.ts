import { defineNuxtPlugin } from '#app'

export default defineNuxtPlugin(() => {
  const formatCurrency = (value: number, currency: string = 'Q'): string => {
    if (Number.isNaN(Number(value))) return `${currency} 0.00`
    return `${currency} ${Number(value).toFixed(2)}`
  }

  const formatDate = (date: string | number | Date): string => {
    const d = new Date(date)
    if (isNaN(d.getTime())) return 'N/A'
    
    // Obtener zona horaria del usuario (guardada o detectada)
    const userTimezone = localStorage.getItem('userTimezone') || 
                        Intl.DateTimeFormat().resolvedOptions().timeZone || 
                        'America/Guatemala'
    
    return d.toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      timeZone: userTimezone
    })
  }

  const formatTime = (date: string | number | Date): string => {
    const d = new Date(date)
    if (isNaN(d.getTime())) return 'N/A'
    
    // Obtener zona horaria del usuario (guardada o detectada)
    const userTimezone = localStorage.getItem('userTimezone') || 
                        Intl.DateTimeFormat().resolvedOptions().timeZone || 
                        'America/Guatemala'
    
    return d.toLocaleTimeString('es-ES', {
      hour: '2-digit',
      minute: '2-digit',
      timeZone: userTimezone
    })
  }

  const formatDateTime = (date: string | number | Date): string => {
    const d = new Date(date)
    if (isNaN(d.getTime())) return 'N/A'
    
    // Obtener zona horaria del usuario (guardada o detectada)
    const userTimezone = localStorage.getItem('userTimezone') || 
                        Intl.DateTimeFormat().resolvedOptions().timeZone || 
                        'America/Guatemala'
    
    return d.toLocaleString('es-ES', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      timeZone: userTimezone
    })
  }

  return {
    provide: {
      formatCurrency,
      formatDate,
      formatTime,
      formatDateTime
    }
  }
})



