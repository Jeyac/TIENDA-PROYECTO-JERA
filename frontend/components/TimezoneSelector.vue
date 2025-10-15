<template>
  <div class="timezone-selector">
    <div class="d-flex align-items-center gap-2">
      <i class="bi bi-globe text-primary"></i>
      <span class="text-muted small">Zona horaria:</span>
      <select 
        v-model="selectedTimezone" 
        @change="updateTimezone"
        class="form-select form-select-sm"
        style="max-width: 200px;"
      >
        <option value="auto">🌍 Automática</option>
        <optgroup label="Centroamérica">
          <option value="America/Guatemala">🇬🇹 Guatemala</option>
          <option value="America/El_Salvador">🇸🇻 El Salvador</option>
          <option value="America/Honduras">🇭🇳 Honduras</option>
          <option value="America/Nicaragua">🇳🇮 Nicaragua</option>
          <option value="America/Costa_Rica">🇨🇷 Costa Rica</option>
          <option value="America/Belize">🇧🇿 Belice</option>
        </optgroup>
        <optgroup label="Norteamérica">
          <option value="America/Mexico_City">🇲🇽 México</option>
          <option value="America/New_York">🇺🇸 Estados Unidos (Este)</option>
          <option value="America/Los_Angeles">🇺🇸 Estados Unidos (Oeste)</option>
          <option value="America/Toronto">🇨🇦 Canadá</option>
        </optgroup>
        <optgroup label="Sudamérica">
          <option value="America/Argentina/Buenos_Aires">🇦🇷 Argentina</option>
          <option value="America/Sao_Paulo">🇧🇷 Brasil</option>
          <option value="America/Bogota">🇨🇴 Colombia</option>
          <option value="America/Lima">🇵🇪 Perú</option>
          <option value="America/Santiago">🇨🇱 Chile</option>
          <option value="America/Montevideo">🇺🇾 Uruguay</option>
        </optgroup>
        <optgroup label="Europa">
          <option value="Europe/Madrid">🇪🇸 España</option>
          <option value="Europe/London">🇬🇧 Reino Unido</option>
          <option value="Europe/Paris">🇫🇷 Francia</option>
          <option value="Europe/Berlin">🇩🇪 Alemania</option>
        </optgroup>
      </select>
    </div>
    
    <div v-if="currentTime" class="small text-muted mt-1">
      <i class="bi bi-clock me-1"></i>
      Hora actual: {{ currentTime }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'

const selectedTimezone = ref('auto')
const currentTime = ref('')

// Detectar zona horaria automáticamente
const detectTimezone = () => {
  try {
    const userTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone
    return userTimezone
  } catch (error) {
    console.warn('No se pudo detectar la zona horaria:', error)
    return 'America/Guatemala'
  }
}

// Actualizar zona horaria
const updateTimezone = () => {
  const timezone = selectedTimezone.value === 'auto' ? detectTimezone() : selectedTimezone.value
  
  // Guardar en localStorage
  localStorage.setItem('userTimezone', timezone)
  
  // Emitir evento para que otros componentes se actualicen
  window.dispatchEvent(new CustomEvent('timezoneChanged', { 
    detail: { timezone } 
  }))
  
  updateCurrentTime()
}

// Actualizar hora actual
const updateCurrentTime = () => {
  const timezone = selectedTimezone.value === 'auto' ? detectTimezone() : selectedTimezone.value
  
  const now = new Date()
  currentTime.value = now.toLocaleString('es-ES', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    timeZone: timezone
  })
}

// Cargar zona horaria guardada
onMounted(() => {
  const savedTimezone = localStorage.getItem('userTimezone')
  if (savedTimezone) {
    selectedTimezone.value = savedTimezone
  } else {
    // Detectar automáticamente
    const detected = detectTimezone()
    selectedTimezone.value = 'auto'
    localStorage.setItem('userTimezone', detected)
  }
  
  updateCurrentTime()
  
  // Actualizar cada segundo
  setInterval(updateCurrentTime, 1000)
})
</script>

<style scoped>
.timezone-selector {
  padding: 0.5rem;
  background: rgba(0, 0, 0, 0.02);
  border-radius: 0.375rem;
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.form-select-sm {
  font-size: 0.875rem;
}
</style>







