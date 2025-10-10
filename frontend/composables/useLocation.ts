import { ref, computed } from 'vue'

interface LocationData {
  country: string
  countryCode: string
  timezone: string
  city?: string
  region?: string
}

export const useLocation = () => {
  const location = ref<LocationData | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Mapeo de países a zonas horarias
  const countryTimezoneMap: Record<string, string> = {
    'GT': 'America/Guatemala',    // Guatemala
    'SV': 'America/El_Salvador',  // El Salvador
    'HN': 'America/Honduras',     // Honduras
    'NI': 'America/Nicaragua',    // Nicaragua
    'CR': 'America/Costa_Rica',   // Costa Rica
    'BZ': 'America/Belize',       // Belice
    'MX': 'America/Mexico_City',  // México
    'US': 'America/New_York',     // Estados Unidos
    'AR': 'America/Argentina/Buenos_Aires', // Argentina
    'BR': 'America/Sao_Paulo',    // Brasil
    'ES': 'Europe/Madrid',        // España
    'GB': 'Europe/London',        // Reino Unido
    'FR': 'Europe/Paris',         // Francia
    'DE': 'Europe/Berlin',        // Alemania
    'IT': 'Europe/Rome',          // Italia
    'CA': 'America/Toronto',      // Canadá
    'CO': 'America/Bogota',       // Colombia
    'PE': 'America/Lima',         // Perú
    'CL': 'America/Santiago',     // Chile
    'UY': 'America/Montevideo',   // Uruguay
    'PY': 'America/Asuncion',     // Paraguay
    'BO': 'America/La_Paz',       // Bolivia
    'EC': 'America/Guayaquil',    // Ecuador
    'VE': 'America/Caracas',      // Venezuela
    'PA': 'America/Panama',       // Panamá
    'CU': 'America/Havana',       // Cuba
    'DO': 'America/Santo_Domingo', // República Dominicana
    'PR': 'America/Puerto_Rico',  // Puerto Rico
    'JM': 'America/Jamaica',      // Jamaica
    'HT': 'America/Port-au-Prince', // Haití
  }

  // Detectar ubicación por IP
  const detectLocation = async (): Promise<void> => {
    loading.value = true
    error.value = null

    try {
      // Usar API gratuita para detectar ubicación por IP
      const response = await fetch('https://ipapi.co/json/')
      
      if (!response.ok) {
        throw new Error('No se pudo obtener la ubicación')
      }

      const data = await response.json()
      
      location.value = {
        country: data.country_name || 'Desconocido',
        countryCode: data.country_code || 'GT',
        timezone: data.timezone || 'America/Guatemala',
        city: data.city,
        region: data.region
      }

      // Si no hay timezone en la respuesta, usar nuestro mapeo
      if (!data.timezone && data.country_code) {
        location.value.timezone = countryTimezoneMap[data.country_code] || 'America/Guatemala'
      }

    } catch (err) {
      console.warn('Error detectando ubicación:', err)
      error.value = 'No se pudo detectar la ubicación'
      
      // Fallback a Guatemala
      location.value = {
        country: 'Guatemala',
        countryCode: 'GT',
        timezone: 'America/Guatemala'
      }
    } finally {
      loading.value = false
    }
  }

  // Zona horaria detectada
  const detectedTimezone = computed(() => {
    return location.value?.timezone || 'America/Guatemala'
  })

  // País detectado
  const detectedCountry = computed(() => {
    return location.value?.country || 'Guatemala'
  })

  // Función para formatear fechas en la zona horaria detectada
  const formatDateInDetectedTimezone = (date: string | number | Date, options?: Intl.DateTimeFormatOptions): string => {
    const d = new Date(date)
    if (isNaN(d.getTime())) return 'N/A'
    
    return d.toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      timeZone: detectedTimezone.value,
      ...options
    })
  }

  return {
    location: readonly(location),
    loading: readonly(loading),
    error: readonly(error),
    detectedTimezone,
    detectedCountry,
    detectLocation,
    formatDateInDetectedTimezone
  }
}



