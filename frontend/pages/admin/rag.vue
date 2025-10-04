<template>
  <div class="rag-page">
    <div class="container-fluid">
      <!-- Header -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <h1 class="display-6 fw-bold mb-2">
                <i class="bi bi-file-earmark-arrow-up me-2"></i>Gestión de Archivos RAG
              </h1>
              <p class="text-muted mb-0">Sube y gestiona archivos para el sistema de recuperación de información</p>
            </div>
            <button class="btn btn-primary" @click="showUploadModal = true">
              <i class="bi bi-cloud-upload me-2"></i>Subir Archivo
            </button>
          </div>
        </div>
      </div>

      <!-- Upload Area -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="card border-0 shadow-sm">
            <div class="card-body">
              <div class="upload-area" @dragover.prevent @drop.prevent="handleDrop">
                <div class="upload-content">
                  <i class="bi bi-cloud-upload display-4 text-primary mb-3"></i>
                  <h5>Arrastra archivos aquí o haz clic para seleccionar</h5>
                  <p class="text-muted">Formatos soportados: PDF, TXT, DOC, DOCX</p>
                  <button class="btn btn-outline-primary" @click="triggerFileInput">
                    <i class="bi bi-folder2-open me-2"></i>Seleccionar Archivos
                  </button>
                </div>
                <input
                  ref="fileInput"
                  type="file"
                  multiple
                  accept=".pdf,.txt,.doc,.docx"
                  @change="handleFileSelect"
                  style="display: none;"
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
                <i class="bi bi-files me-2"></i>Archivos Subidos
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
                  <th>Estado</th>
                  <th>Fecha Subida</th>
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
                    <span class="badge bg-secondary">{{ file.tipo.toUpperCase() }}</span>
                  </td>
                  <td>{{ formatFileSize(file.tamaño) }}</td>
                  <td>
                    <span class="badge" :class="getStatusBadgeClass(file.estado)">
                      {{ file.estado }}
                    </span>
                  </td>
                  <td>
                    <small>{{ formatDate(file.fecha_subida) }}</small>
                  </td>
                  <td>
                    <div class="btn-group" role="group">
                      <button class="btn btn-outline-primary btn-sm" @click="viewFile(file)">
                        <i class="bi bi-eye"></i>
                      </button>
                      <button class="btn btn-outline-success btn-sm" @click="processFile(file)" :disabled="file.estado === 'procesando'">
                        <i class="bi bi-gear"></i>
                      </button>
                      <button class="btn btn-outline-danger btn-sm" @click="deleteFile(file)">
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
                <i class="bi bi-cloud-upload me-2"></i>Subir Archivo
              </h5>
              <button type="button" class="btn-close" @click="closeUploadModal"></button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="uploadFile">
                <div class="mb-3">
                  <label for="file" class="form-label">Seleccionar Archivo</label>
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
                <i class="bi bi-file-earmark me-2"></i>{{ selectedFile?.nombre }}
              </h5>
              <button type="button" class="btn-close" @click="showDetailsModal = false"></button>
            </div>
            <div class="modal-body">
              <div v-if="selectedFile" class="file-details">
                <div class="row mb-3">
                  <div class="col-md-6">
                    <h6>Información del Archivo</h6>
                    <p class="mb-1"><strong>Nombre:</strong> {{ selectedFile.nombre }}</p>
                    <p class="mb-1"><strong>Tipo:</strong> {{ selectedFile.tipo.toUpperCase() }}</p>
                    <p class="mb-1"><strong>Tamaño:</strong> {{ formatFileSize(selectedFile.tamaño) }}</p>
                    <p class="mb-1"><strong>Estado:</strong> 
                      <span class="badge" :class="getStatusBadgeClass(selectedFile.estado)">
                        {{ selectedFile.estado }}
                      </span>
                    </p>
                  </div>
                  <div class="col-md-6">
                    <h6>Metadatos</h6>
                    <p class="mb-1"><strong>Fecha Subida:</strong> {{ formatDate(selectedFile.fecha_subida) }}</p>
                    <p class="mb-1"><strong>Última Modificación:</strong> {{ formatDate(selectedFile.fecha_modificacion) }}</p>
                    <p class="mb-1"><strong>Procesado:</strong> {{ selectedFile.procesado ? 'Sí' : 'No' }}</p>
                  </div>
                </div>
                
                <div v-if="selectedFile.descripcion">
                  <h6>Descripción</h6>
                  <p class="text-muted">{{ selectedFile.descripcion }}</p>
                </div>
                
                <div v-if="selectedFile.contenido_extracto">
                  <h6>Contenido Extraído</h6>
                  <div class="content-preview">
                    {{ selectedFile.contenido_extracto.substring(0, 500) }}...
                  </div>
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
                <i class="bi bi-exclamation-triangle me-2"></i>Confirmar Eliminación
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
  middleware: 'admin',
  layout: 'admin'
})

const config = useRuntimeConfig()
const auth = useAuthStore()

// Data
const files = ref<any[]>([])
const searchQuery = ref('')
const loading = ref(false)
const uploading = ref(false)
const deleting = ref(false)
const error = ref('')

// File handling
const selectedFile = ref<File | null>(null)
const fileInput = ref<HTMLInputElement>()
const modalFileInput = ref<HTMLInputElement>()

// Modal states
const showUploadModal = ref(false)
const showDetailsModal = ref(false)
const showDeleteModal = ref(false)
const selectedFileData = ref<any>(null)
const fileToDelete = ref<any>(null)

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
    handleFiles(Array.from(droppedFiles))
  }
}

const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    handleFiles(Array.from(target.files))
  }
}

const handleModalFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    selectedFile.value = target.files[0]
  }
}

const handleFiles = (fileList: File[]) => {
  if (fileList.length > 0) {
    selectedFile.value = fileList[0]
    showUploadModal.value = true
  }
}

const triggerFileInput = () => {
  fileInput.value?.click()
}

const uploadFile = async () => {
  if (!selectedFile.value) return
  
  uploading.value = true
  error.value = ''
  
  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value)
    formData.append('descripcion', uploadForm.descripcion)
    formData.append('procesar_automaticamente', uploadForm.procesar_automaticamente.toString())
    
    const res = await fetch(`${config.public.apiBase}/api/admin/rag/upload`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${auth.token}`
      },
      body: formData
    })
    
    if (res.ok) {
      await loadFiles()
      closeUploadModal()
    } else if (res.status === 401) {
      await auth.logout()
    } else {
      const data = await res.json()
      throw new Error(data.error || data.message || 'Error al subir archivo')
    }
  } catch (err: any) {
    error.value = err.message
  } finally {
    uploading.value = false
  }
}

const viewFile = (file: any) => {
  selectedFileData.value = file
  showDetailsModal.value = true
}

const processFile = async (file: any) => {
  try {
    const res = await fetch(`${config.public.apiBase}/api/admin/rag/process/${file.id}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${auth.token}`
      }
    })
    
    if (res.ok) {
      await loadFiles()
    } else if (res.status === 401) {
      await auth.logout()
    } else {
      throw new Error('Error al procesar archivo')
    }
  } catch (err: any) {
    error.value = err.message
  }
}

const deleteFile = (file: any) => {
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

const getStatusBadgeClass = (estado: string) => {
  const statusClasses: { [key: string]: string } = {
    'subido': 'bg-info',
    'procesando': 'bg-warning',
    'procesado': 'bg-success',
    'error': 'bg-danger'
  }
  return statusClasses[estado] || 'bg-secondary'
}

const formatFileSize = (bytes: number) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString()
}

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
