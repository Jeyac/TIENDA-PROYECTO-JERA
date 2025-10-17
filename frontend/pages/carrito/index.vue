<template>
  <section>
    <h1>Carrito ({{ carrito.count }})</h1>
    <div v-if="carrito.items.length === 0">Tu carrito está vacío.</div>
    <table v-else class="table">
      <thead>
        <tr><th>Producto</th><th>Cantidad</th><th>Precio</th><th></th></tr>
      </thead>
      <tbody>
        <tr v-for="it in carrito.items" :key="it.producto_id">
          <td>{{ it.titulo }}</td>
          <td>
            <div class="d-flex align-items-center gap-2">
              <BaseButton 
                variant="outline-secondary btn-sm" 
                @click="decrementarCantidad(it.producto_id)"
                :disabled="it.cantidad <= 1 || procesandoCantidad[it.producto_id]"
              >
                <i class="bi bi-dash"></i>
              </BaseButton>
              <span class="fw-bold">{{ it.cantidad }}</span>
              <BaseButton 
                variant="outline-secondary btn-sm" 
                @click="incrementarCantidad(it.producto_id)"
                :disabled="it.cantidad >= it.stock || procesandoCantidad[it.producto_id]"
              >
                <i class="bi bi-plus"></i>
              </BaseButton>
            </div>
          </td>
          <td>Q {{ (it.cantidad * it.precio_unitario).toFixed(2) }}</td>
          <td><BaseButton variant="outline-danger btn-sm" @click="carrito.quitarItem(it.producto_id)">Quitar</BaseButton></td>
        </tr>
      </tbody>
      <tfoot>
        <tr><td colspan="2">Total</td><td>Q {{ carrito.total.toFixed(2) }}</td><td></td></tr>
      </tfoot>
    </table>

    <div v-if="carrito.items.length">
      <h2>Datos de facturación</h2>
      <div class="row g-2">
        <div class="col-sm-6">
          <label class="form-label">Nombre completo <span class="text-danger">*</span></label>
          <input class="form-control" v-model="facturacion.nombre" placeholder="Nombre completo" required />
        </div>
        <div class="col-sm-6">
          <label class="form-label">NIT</label>
          <input class="form-control" v-model="facturacion.identificacion" placeholder="Identificación" />
        </div>
        <div class="col-sm-6">
          <label class="form-label">Dirección <span class="text-danger">*</span></label>
          <input class="form-control" v-model="facturacion.direccion" placeholder="Dirección" required />
        </div>
        <div class="col-sm-6">
          <label class="form-label">Número de teléfono <span class="text-danger">*</span></label>
          <input class="form-control" v-model="facturacion.telefono" type="tel" placeholder="Número de teléfono" required />
        </div>
      </div>
      <BaseButton variant="primary" class="mt-3" @click="finalizar" :disabled="!facturacion.nombre || !facturacion.telefono || !facturacion.direccion || procesando">
        <i class="bi bi-check-circle me-2"></i>{{ procesando ? 'Procesando...' : 'Finalizar compra' }}
      </BaseButton>
      <p class="status">{{ status }}</p>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRuntimeConfig, navigateTo } from 'nuxt/app'
import { useCarritoStore } from '../../stores/carrito'
import { useAuthStore } from '../../stores/auth'

definePageMeta({
  middleware: ['user-only'],
  layout: 'default'
})
// route derived from file path

const carrito = useCarritoStore()
const config = useRuntimeConfig()
const status = ref('')
const facturacion = reactive({ nombre: '', identificacion: '', direccion: '', telefono: '' })
const procesando = ref(false)

// Flag para prevenir doble clic en incrementar/decrementar
const procesandoCantidad = ref<Record<number, boolean>>({})

// Funciones para manejar cantidades
const incrementarCantidad = async (producto_id: number) => {
  // Prevenir doble clic
  if (procesandoCantidad.value[producto_id]) {
    console.log(`Ya se está procesando incremento para producto ${producto_id}, ignorando clic`)
    return
  }
  
  procesandoCantidad.value[producto_id] = true
  
  try {
    const item = carrito.items.find(i => i.producto_id === producto_id)
    if (item) {
      console.log(`Incrementando cantidad para producto ${producto_id}: ${item.cantidad} -> ${item.cantidad + 1} (stock: ${item.stock})`)
      // Verificar que no exceda el stock disponible
      if (item.cantidad < item.stock) {
        item.cantidad += 1
        console.log(`Cantidad actualizada a: ${item.cantidad}`)
      } else {
        console.log(`No se puede incrementar: cantidad (${item.cantidad}) >= stock (${item.stock})`)
      }
    } else {
      console.log(`Producto ${producto_id} no encontrado en el carrito`)
    }
  } finally {
    // Pequeño delay para evitar clics múltiples
    await new Promise(resolve => setTimeout(resolve, 100))
    procesandoCantidad.value[producto_id] = false
  }
}

const decrementarCantidad = async (producto_id: number) => {
  // Prevenir doble clic
  if (procesandoCantidad.value[producto_id]) {
    console.log(`Ya se está procesando decremento para producto ${producto_id}, ignorando clic`)
    return
  }
  
  procesandoCantidad.value[producto_id] = true
  
  try {
    const item = carrito.items.find(i => i.producto_id === producto_id)
    if (item && item.cantidad > 1) {
      console.log(`Decrementando cantidad para producto ${producto_id}: ${item.cantidad} -> ${item.cantidad - 1}`)
      item.cantidad -= 1
      console.log(`Cantidad actualizada a: ${item.cantidad}`)
    }
  } finally {
    // Pequeño delay para evitar clics múltiples
    await new Promise(resolve => setTimeout(resolve, 100))
    procesandoCantidad.value[producto_id] = false
  }
}

async function finalizar() {
  // Prevenir doble clic
  if (procesando.value) return
  
  procesando.value = true
  status.value = 'Procesando...'
  
  try {
    const { apiRequest } = useApi()
    const auth = useAuthStore()
    
    // Validar que el usuario esté autenticado
    if (!auth.user?.id) {
      throw new Error('Usuario no autenticado')
    }
    
    // Validar datos de facturación
    if (!facturacion.nombre || !facturacion.telefono || !facturacion.direccion) {
      throw new Error('Por favor completa todos los campos obligatorios (nombre, teléfono y dirección)')
    }
    
    // Validar que hay items en el carrito
    if (carrito.items.length === 0) {
      throw new Error('No hay productos en el carrito')
    }
    
    const body = {
      usuario_id: auth.user.id,
      items: carrito.items.map(i => ({ producto_id: i.producto_id, cantidad: i.cantidad, precio_unitario: i.precio_unitario })),
      datos_facturacion: { ...facturacion }
    }
    
    const res = await apiRequest('/api/pedidos/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.message || 'Error al crear pedido')
    
    // Limpiar carrito y formulario
    carrito.vaciar()
    Object.assign(facturacion, { nombre: '', identificacion: '', direccion: '', telefono: '' })
    
    status.value = `Pedido creado #${data.id}`
    
    // Emitir evento para actualizar el catálogo
    if (typeof window !== 'undefined') {
      window.dispatchEvent(new CustomEvent('pedidoCreado', { 
        detail: { pedidoId: data.id } 
      }))
    }
    
  } catch (e: any) {
    status.value = `Error: ${e.message}`
  } finally {
    procesando.value = false
  }
}
</script>

<style scoped>
.status { margin-top: 8px; color: #555; }
</style>


