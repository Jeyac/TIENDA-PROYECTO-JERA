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
                :disabled="it.cantidad <= 1"
              >
                <i class="bi bi-dash"></i>
              </BaseButton>
              <span class="fw-bold">{{ it.cantidad }}</span>
              <BaseButton 
                variant="outline-secondary btn-sm" 
                @click="incrementarCantidad(it.producto_id)"
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
definePageMeta({
  middleware: ['user-only'],
  layout: 'default'
})

import { ref, reactive } from 'vue'
import { useRuntimeConfig, navigateTo } from 'nuxt/app'
import { useCarritoStore } from '../../stores/carrito'
import { useAuthStore } from '../../stores/auth'
// route derived from file path

const carrito = useCarritoStore()
const config = useRuntimeConfig()
const status = ref('')
const facturacion = reactive({ nombre: '', identificacion: '', direccion: '', telefono: '' })
const procesando = ref(false)

// Funciones para manejar cantidades
const incrementarCantidad = (producto_id: number) => {
  const item = carrito.items.find(i => i.producto_id === producto_id)
  if (item) {
    item.cantidad += 1
  }
}

const decrementarCantidad = (producto_id: number) => {
  const item = carrito.items.find(i => i.producto_id === producto_id)
  if (item && item.cantidad > 1) {
    item.cantidad -= 1
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
    carrito.vaciar()
    status.value = `Pedido creado #${data.id}`
    
    // Limpiar formulario
    Object.assign(facturacion, { nombre: '', identificacion: '', direccion: '', telefono: '' })
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


