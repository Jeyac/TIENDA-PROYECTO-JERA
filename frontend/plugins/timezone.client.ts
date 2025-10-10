import { defineNuxtPlugin } from '#app'

export default defineNuxtPlugin(() => {
  // Función para detectar zona horaria del usuario
  const detectUserTimezone = (): string => {
    try {
      // Obtener zona horaria del navegador
      const userTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone
      
      // Mapeo de zonas horarias comunes a países
      const timezoneMap: Record<string, string> = {
        'America/Guatemala': 'Guatemala',
        'America/El_Salvador': 'El Salvador', 
        'America/Honduras': 'Honduras',
        'America/Nicaragua': 'Nicaragua',
        'America/Costa_Rica': 'Costa Rica',
        'America/Belize': 'Belice',
        'America/Mexico_City': 'México',
        'America/New_York': 'Estados Unidos (Este)',
        'America/Los_Angeles': 'Estados Unidos (Oeste)',
        'America/Argentina/Buenos_Aires': 'Argentina',
        'America/Sao_Paulo': 'Brasil',
        'Europe/Madrid': 'España',
        'Europe/London': 'Reino Unido'
      }
      
      return timezoneMap[userTimezone] || userTimezone
    } catch (error) {
      console.warn('No se pudo detectar la zona horaria:', error)
      return 'America/Guatemala' // Fallback a Guatemala
    }
  }

  // Función para obtener zona horaria del usuario
  const getUserTimezone = (): string => {
    return Intl.DateTimeFormat().resolvedOptions().timeZone
  }

  // Función para formatear fechas en la zona horaria del usuario
  const formatDateInUserTimezone = (date: string | number | Date, options?: Intl.DateTimeFormatOptions): string => {
    const d = new Date(date)
    if (isNaN(d.getTime())) return 'N/A'
    
    const userTimezone = getUserTimezone()
    
    return d.toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      timeZone: userTimezone,
      ...options
    })
  }

  // Función para formatear tiempo en la zona horaria del usuario
  const formatTimeInUserTimezone = (date: string | number | Date, options?: Intl.DateTimeFormatOptions): string => {
    const d = new Date(date)
    if (isNaN(d.getTime())) return 'N/A'
    
    const userTimezone = getUserTimezone()
    
    return d.toLocaleTimeString('es-ES', {
      hour: '2-digit',
      minute: '2-digit',
      timeZone: userTimezone,
      ...options
    })
  }

  // Función para formatear fecha y hora completa en la zona horaria del usuario
  const formatDateTimeInUserTimezone = (date: string | number | Date, options?: Intl.DateTimeFormatOptions): string => {
    const d = new Date(date)
    if (isNaN(d.getTime())) return 'N/A'
    
    const userTimezone = getUserTimezone()
    
    return d.toLocaleString('es-ES', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      timeZone: userTimezone,
      ...options
    })
  }

  return {
    provide: {
      detectUserTimezone,
      getUserTimezone,
      formatDateInUserTimezone,
      formatTimeInUserTimezone,
      formatDateTimeInUserTimezone
    }
  }
})



