<template>
  <div class="rag-page">
    <div class="container-fluid">
      <!-- Header -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <h1 class="display-6 fw-bold mb-2">
                <i class="bi bi-file-earmark-arrow-up me-2"></i>Gestión de archivos para RAG
              </h1>
              <p class="text-muted mb-0">Sube y gestiona archivos para el sistema de recuperación de información</p>
            </div>
            <button class="btn btn-primary" @click="showUploadModal = true">
              <i class="bi bi-cloud-upload me-2"></i>Subir archivo
            </button>
          </div>
        </div>
      </div>

      <!-- Upload Area -->
      <div class="row mb-4">
        <div class="col-12">
          <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
            <i class="bi bi-exclamation-triangle me-2"></i>{{ error }}
            <button type="button" class="btn-close" @click="error = ''"></button>
          </div>
          <div class="card border-0 shadow-sm">
            <div class="card-body">
              <div class="upload-area" @dragover.prevent @drop.prevent="handleDrop">
                <div v-if="uploading" class="upload-content">
                  <div class="spinner-border text-primary mb-3" role="status">
                    <span class="visually-hidden">Subiendo...</span>
                  </div>
                  <h5>Subiendo archivo...</h5>
                  <p class="text-muted">Por favor espera</p>
                </div>
                <div v-else class="upload-content">
                  <i class="bi bi-cloud-upload display-4 text-primary mb-3"></i>
                  <h5>Arrastra archivos aquí o haz clic para seleccionar</h5>
                  <p class="text-muted">Los archivos se subirán automáticamente</p>
                  <p class="text-muted small">Formatos soportados: PDF, TXT, DOC, DOCX (máx. 10MB)</p>
                  <button class="btn btn-outline-primary" @click="triggerFileInput" type="button" :disabled="uploading">
                    <i class="bi bi-folder2-open me-2"></i>Seleccionar archivos
                  </button>
                </div>
                <input
                  ref="fileInput"
                  type="file"
                  multiple
                  accept=".pdf,.txt,.doc,.docx"
                  @change="handleFileSelect"
                  style="display: none;"
                  :disabled="uploading"
                >
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Files List -->
      <div class="card border-0 shadow-sm">
        <div class="card-header bg-white border-bottom">
          <div class="row align-items-center">
            <div class="col-md-6">
              <h5 class="card-title mb-0">
                <i class="bi bi-files me-2"></i>Archivos subidos
                <span class="badge bg-primary ms-2">{{ files.length }}</span>
              </h5>
            </div>
            <div class="col-md-6">
              <div class="input-group">
                <input
                  v-model="searchQuery"
                  type="text"
                  class="form-control"
                  placeholder="Buscar archivos..."
                  @input="filterFiles"
                >
                <button class="btn btn-outline-secondary" type="button">
                  <i class="bi bi-search"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
        <div class="card-body p-0">
          <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Cargando...</span>
            </div>
            <p class="text-muted mt-3">Cargando archivos...</p>
          </div>
          
          <div v-else-if="filteredFiles.length === 0" class="text-center py-5">
            <i class="bi bi-file-earmark text-muted" style="font-size: 4rem;"></i>
            <h3 class="text-muted mt-3">No hay archivos</h3>
            <p class="text-muted">Sube tu primer archivo para comenzar.</p>
          </div>
          
          <div v-else class="table-responsive">
            <table class="table table-hover mb-0">
              <thead class="table-light">
                <tr>
                  <th>Nombre</th>
                  <th>Tipo</th>
                  <th>Tamaño</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="file in filteredFiles" :key="file.id">
                  <td>
                    <div class="d-flex align-items-center">
                      <i :class="getFileIcon(file.tipo)" class="me-2"></i>
                      <div>
                        <strong>{{ file.nombre }}</strong>
                        <br>
                        <small class="text-muted">{{ file.descripcion || 'Sin descripción' }}</small>
                      </div>
                    </div>
                  </td>
                  <td>
                    <span class="badge bg-secondary">{{ (file.tipo || '').toUpperCase() }}</span>
                  </td>
                  <td>{{ file.tamaño }}</td>
                  <td>
                    <div class="btn-group" role="group">
                      <button class="btn btn-outline-info btn-sm" @click="downloadFile(file)" title="Descargar archivo">
                        <i class="bi bi-download"></i>
                      </button>
                      <button class="btn btn-outline-success btn-sm" @click="processFile(file)" title="Reprocesar archivo">
                        <i class="bi bi-gear"></i>
                      </button>
                      <button class="btn btn-outline-danger btn-sm" @click="deleteFile(file)" title="Eliminar archivo">
                        <i class="bi bi-trash"></i>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Upload Modal -->
      <div class="modal fade" :class="{ show: showUploadModal }" :style="{ display: showUploadModal ? 'block' : 'none' }" tabindex="-1">
        <div class="modal-dialog modal-lg">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">
                <i class="bi bi-cloud-upload me-2"></i>Subir Archivo con opciones
              </h5>
              <button type="button" class="btn-close" @click="closeUploadModal"></button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="uploadFile">
                <div class="mb-3">
                  <label for="file" class="form-label">Seleccionar archivo</label>
                  <input
                    ref="modalFileInput"
                    type="file"
                    class="form-control"
                    id="file"
                    accept=".pdf,.txt,.doc,.docx"
                    @change="handleModalFileSelect"
                    required
                    :disabled="uploading"
                  >
                  <div class="form-text">
                    Formatos soportados: PDF, TXT, DOC, DOCX (máximo 10MB)
                  </div>
                </div>
                
                <div class="mb-3">
                  <label for="descripcion" class="form-label">Descripción</label>
                  <textarea
                    v-model="uploadForm.descripcion"
                    class="form-control"
                    id="descripcion"
                    rows="3"
                    placeholder="Describe el contenido del archivo..."
                    :disabled="uploading"
                  ></textarea>
                </div>
                
                <div class="mb-3">
                  <div class="form-check">
                    <input
                      v-model="uploadForm.procesar_automaticamente"
                      class="form-check-input"
                      type="checkbox"
                      id="procesar_auto"
                      :disabled="uploading"
                    >
                    <label class="form-check-label" for="procesar_auto">
                      Procesar automáticamente después de subir
                    </label>
                  </div>
                </div>
                
                <div v-if="error" class="alert alert-danger">
                  <i class="bi bi-exclamation-triangle me-2"></i>{{ error }}
                </div>
                
                <div class="modal-footer">
                  <button type="button" class="btn btn-secondary" @click="closeUploadModal" :disabled="uploading">
                    Cancelar
                  </button>
                  <button type="submit" class="btn btn-primary" :disabled="uploading || !selectedFile">
                    <span v-if="uploading" class="spinner-border spinner-border-sm me-2"></span>
                    {{ uploading ? 'Subiendo...' : 'Subir Archivo' }}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
      <div v-if="showUploadModal" class="modal-backdrop fade show"></div>

      <!-- File Details Modal -->
      <div class="modal fade" :class="{ show: showDetailsModal }" :style="{ display: showDetailsModal ? 'block' : 'none' }" tabindex="-1">
        <div class="modal-dialog modal-lg">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">
                <i class="bi bi-file-earmark me-2"></i>{{ selectedFileData?.nombre }}
              </h5>
              <button type="button" class="btn-close" @click="showDetailsModal = false"></button>
            </div>
            <div class="modal-body">
              <div v-if="selectedFileData" class="file-details">
                <div class="row mb-3">
                  <div class="col-md-6">
                    <h6>Información del Archivo</h6>
                    <p class="mb-1"><strong>Nombre:</strong> {{ selectedFileData.nombre }}</p>
                    <p class="mb-1"><strong>Tipo:</strong> {{ (selectedFileData.tipo || '').toUpperCase() }}</p>
                    <p class="mb-1"><strong>Tamaño:</strong> {{ selectedFileData.tamaño }}</p>
                  </div>
                  <div class="col-md-6">
                    <h6>Metadatos</h6>
                    <p class="mb-1"><strong>Fecha de subida:</strong> {{ formatDate(selectedFileData.fecha_subida) }}</p>
                  </div>
                </div>
                
                <div v-if="selectedFileData.descripcion">
                  <h6>Descripción</h6>
                  <p class="text-muted">{{ selectedFileData.descripcion }}</p>
                </div>
                
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="showDetailsModal = false">
                Cerrar
              </button>
            </div>
          </div>
        </div>
      </div>
      <div v-if="showDetailsModal" class="modal-backdrop fade show"></div>

      <!-- Delete Confirmation Modal -->
      <div class="modal fade" :class="{ show: showDeleteModal }" :style="{ display: showDeleteModal ? 'block' : 'none' }" tabindex="-1">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title text-danger">
                <i class="bi bi-exclamation-triangle me-2"></i>Confirmar eliminación
              </h5>
              <button type="button" class="btn-close" @click="showDeleteModal = false"></button>
            </div>
            <div class="modal-body">
              <p>¿Estás seguro de que deseas eliminar el archivo <strong>{{ fileToDelete?.nombre }}</strong>?</p>
              <p class="text-muted small">Esta acción no se puede deshacer.</p>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="showDeleteModal = false">
                Cancelar
              </button>
              <button type="button" class="btn btn-danger" @click="confirmDelete" :disabled="deleting">
                <span v-if="deleting" class="spinner-border spinner-border-sm me-2"></span>
                {{ deleting ? 'Eliminando...' : 'Eliminar' }}
              </button>
            </div>
          </div>
        </div>
      </div>
      <div v-if="showDeleteModal" class="modal-backdrop fade show"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useRuntimeConfig } from 'nuxt/app'
import { useAuthStore } from '../../stores/auth'

// Middleware para proteger la ruta
definePageMeta({
  middleware: ['auth', 'admin'],
  layout: 'admin'
})

// Interfaces
interface DocumentoRAG {
  id: number
  nombre: string
  tipo: string
  tamaño: number
  descripcion?: string
  chunks_count?: number
  procesado: boolean
  fecha_subida: string
}

const config = useRuntimeConfig()
const auth = useAuthStore()

// Data
const files = ref<DocumentoRAG[]>([])
const searchQuery = ref('')
const loading = ref(false)
const uploading = ref(false)
const deleting = ref(false)
const error = ref('')
const lastUploadTime = ref(0)

// File handling
const selectedFile = ref<File | null>(null)
const fileInput = ref<HTMLInputElement>()
const modalFileInput = ref<HTMLInputElement>()

// Modal states
const showUploadModal = ref(false)
const showDetailsModal = ref(false)
const showDeleteModal = ref(false)
const selectedFileData = ref<DocumentoRAG | null>(null)
const fileToDelete = ref<DocumentoRAG | null>(null)

// Upload form
const uploadForm = reactive({
  descripcion: '',
  procesar_automaticamente: true
})

// Computed
const filteredFiles = computed(() => {
  if (!searchQuery.value) return files.value
  
  const query = searchQuery.value.toLowerCase()
  return files.value.filter(file => 
    file.nombre.toLowerCase().includes(query) ||
    (file.descripcion && file.descripcion.toLowerCase().includes(query))
  )
})

// Methods
const loadFiles = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const res = await fetch(`${config.public.apiBase}/api/admin/rag/files`, {
      headers: {
        'Authorization': `Bearer ${auth.token}`
      }
    })
    
    if (res.ok) {
      files.value = await res.json()
    } else if (res.status === 401) {
      await auth.logout()
    } else {
      throw new Error('Error al cargar archivos')
    }
  } catch (err: any) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

const filterFiles = () => {
  // Filtering is handled by computed property
}

const handleDrop = (event: DragEvent) => {
  const droppedFiles = event.dataTransfer?.files
  if (droppedFiles && droppedFiles.length > 0) {
    const now = Date.now()
    // Prevenir subidas muy rápidas (menos de 1 segundo)
    if (now - lastUploadTime.value < 1000) {
      console.log('Drop muy rápido, ignorando...')
      return
    }
    lastUploadTime.value = now
    
    // Subir directamente sin abrir modal
    uploadFilesDirectly(Array.from(droppedFiles))
  }
}

const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement
  
  if (target.files && target.files.length > 0) {
    const now = Date.now()
    // Prevenir subidas muy rápidas (menos de 1 segundo)
    if (now - lastUploadTime.value < 1000) {
      console.log('⚠️ Subida muy rápida, ignorando...')
      target.value = ''
      return
    }
    lastUploadTime.value = now
    
    // Subir directamente sin abrir modal
    uploadFilesDirectly(Array.from(target.files))
  }
  // Limpiar input para permitir resubir el mismo archivo
  target.value = ''
}

const handleModalFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    selectedFile.value = target.files[0] || null
  }
}

const uploadFilesDirectly = async (fileList: File[]) => {
  if (uploading.value) {
    console.log('⚠️ Ya hay una subida en progreso, ignorando...')
    return
  }
  
  uploading.value = true
  error.value = ''
  
  try {
    for (const file of fileList) {
      await uploadSingleFileInternal(file, '', true)
    }
    // Recargar lista solo una vez al final
    await loadFiles()
  } finally {
    uploading.value = false
  }
}

const triggerFileInput = () => {
  if (!uploading.value) {
    fileInput.value?.click()
  }
}

const uploadSingleFileInternal = async (file: File, descripcion: string = '', procesarAuto: boolean = true) => {
  try {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('descripcion', descripcion)
    formData.append('procesar_automaticamente', procesarAuto.toString())
    
    const res = await fetch(`${config.public.apiBase}/api/rag/upload`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${auth.token}`
      },
      body: formData
    })
    
    if (res.ok) {
      console.log(`Archivo "${file.name}" subido exitosamente`)
      return true
    } else if (res.status === 401) {
      await auth.logout()
      return false
    } else {
      const data = await res.json()
      throw new Error(data.error || data.message || 'Error al subir archivo')
    }
  } catch (err: any) {
    error.value = `Error subiendo "${file.name}": ${err.message}`
    console.error(`${error.value}`)
    return false
  }
}

const uploadSingleFile = async (file: File, descripcion: string = '', procesarAuto: boolean = true) => {
  uploading.value = true
  error.value = ''
  
  try {
    const success = await uploadSingleFileInternal(file, descripcion, procesarAuto)
    if (success) {
      await loadFiles()
    }
    return success
  } finally {
    uploading.value = false
  }
}

const uploadFile = async () => {
  if (!selectedFile.value) return
  
  const success = await uploadSingleFile(
    selectedFile.value,
    uploadForm.descripcion,
    uploadForm.procesar_automaticamente
  )
  
  if (success) {
    closeUploadModal()
  }
}

const viewFile = (file: DocumentoRAG) => {
  selectedFileData.value = file
  showDetailsModal.value = true
}

const processFile = async (file: DocumentoRAG) => {
  try {
    const res = await fetch(`${config.public.apiBase}/api/admin/rag/process/${file.id}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${auth.token}`
      }
    })
    
    if (res.ok) {
      const result = await res.json()
      console.log('Archivo reprocesado:', result.message)
      await loadFiles()
    } else if (res.status === 401) {
      await auth.logout()
    } else {
      const errorData = await res.json()
      throw new Error(errorData.error || 'Error al procesar archivo')
    }
  } catch (err: any) {
    error.value = err.message
  }
}

const downloadFile = async (file: any) => {
  try {
    const res = await fetch(`${config.public.apiBase}/api/admin/rag/files/${file.id}/download`, {
      headers: {
        'Authorization': `Bearer ${auth.token}`
      }
    })
    
    if (res.ok) {
      const blob = await res.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = file.nombre
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } else if (res.status === 401) {
      await auth.logout()
    } else {
      throw new Error('Error al descargar archivo')
    }
  } catch (err: any) {
    error.value = err.message
  }
}

const deleteFile = (file: DocumentoRAG) => {
  fileToDelete.value = file
  showDeleteModal.value = true
}

const confirmDelete = async () => {
  if (!fileToDelete.value) return
  
  deleting.value = true
  
  try {
    const res = await fetch(`${config.public.apiBase}/api/admin/rag/files/${fileToDelete.value.id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${auth.token}`
      }
    })
    
    if (res.ok) {
      await loadFiles()
      showDeleteModal.value = false
      fileToDelete.value = null
    } else if (res.status === 401) {
      await auth.logout()
    } else {
      throw new Error('Error al eliminar archivo')
    }
  } catch (err: any) {
    error.value = err.message
  } finally {
    deleting.value = false
  }
}

const closeUploadModal = () => {
  showUploadModal.value = false
  selectedFile.value = null
  uploadForm.descripcion = ''
  uploadForm.procesar_automaticamente = true
  error.value = ''
  if (modalFileInput.value) {
    modalFileInput.value.value = ''
  }
}

const getFileIcon = (tipo: string) => {
  const icons: { [key: string]: string } = {
    'pdf': 'bi bi-file-earmark-pdf text-danger',
    'txt': 'bi bi-file-earmark-text text-primary',
    'doc': 'bi bi-file-earmark-word text-primary',
    'docx': 'bi bi-file-earmark-word text-primary'
  }
  return icons[tipo] || 'bi bi-file-earmark text-secondary'
}


// Usar función global de formateo
const { $formatDate: formatDate } = useNuxtApp()

// Lifecycle
onMounted(() => {
  if (auth.isAuthenticated && auth.isAdmin) {
    loadFiles()
  }
})
</script>

<style scoped>
.rag-page {
  padding: 2rem 0;
}

.upload-area {
  border: 2px dashed var(--bs-border-color);
  border-radius: 1rem;
  padding: 3rem;
  text-align: center;
  transition: all 0.3s ease;
  cursor: pointer;
}

.upload-area:hover {
  border-color: var(--bs-primary);
  background-color: var(--bs-gray-100);
}

.upload-content {
  pointer-events: none;
}

.upload-content button {
  pointer-events: auto;
}

.upload-area {
  cursor: pointer;
}

.table th {
  border-top: none;
  font-weight: 600;
  color: var(--bs-gray-700);
}

.table td {
  vertical-align: middle;
}

.btn-group .btn {
  border-radius: 0.375rem;
}

.btn-group .btn:not(:last-child) {
  margin-right: 0.25rem;
}

.content-preview {
  background-color: var(--bs-gray-100);
  padding: 1rem;
  border-radius: 0.5rem;
  font-size: 0.9rem;
  max-height: 200px;
  overflow-y: auto;
}

.file-details {
  font-size: 0.9rem;
}

.modal-content {
  border-radius: 1rem;
  border: 1px solid var(--bs-border-color);
}

.modal-header {
  border-bottom: 1px solid var(--bs-border-color);
}

/* Dark theme adjustments */
.dark-theme .upload-area:hover {
  background-color: var(--bs-gray-200);
}

.dark-theme .table-light {
  background-color: var(--bs-gray-200) !important;
}

.dark-theme .modal-content {
  background-color: var(--bs-gray-100);
  border-color: var(--bs-border-color);
}

.dark-theme .modal-header {
  border-bottom-color: var(--bs-border-color);
}

.dark-theme .content-preview {
  background-color: var(--bs-gray-200);
}
</style>























