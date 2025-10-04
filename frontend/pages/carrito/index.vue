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
          <td>{{ it.cantidad }}</td>
          <td>Q {{ (it.cantidad * it.precio_unitario).toFixed(2) }}</td>
          <td><button class="btn btn-sm btn-outline-danger" @click="carrito.quitarItem(it.producto_id)">Quitar</button></td>
        </tr>
      </tbody>
      <tfoot>
        <tr><td colspan="2">Total</td><td>Q {{ carrito.total.toFixed(2) }}</td><td></td></tr>
      </tfoot>
    </table>

    <div v-if="carrito.items.length">
      <h2>Datos de facturación</h2>
      <div class="row g-2">
        <div class="col-sm-6"><input class="form-control" v-model="facturacion.nombre" placeholder="Nombre completo" /></div>
        <div class="col-sm-6"><input class="form-control" v-model="facturacion.identificacion" placeholder="Identificación" /></div>
        <div class="col-sm-6"><input class="form-control" v-model="facturacion.direccion" placeholder="Dirección" /></div>
        <div class="col-sm-6"><input class="form-control" v-model="facturacion.email" placeholder="Correo" /></div>
      </div>
      <button class="btn btn-primary mt-2" @click="finalizar">Finalizar compra</button>
      <p class="status">{{ status }}</p>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRuntimeConfig, navigateTo } from 'nuxt/app'
import { useCarritoStore } from '../../stores/carrito'
// route derived from file path

const carrito = useCarritoStore()
const config = useRuntimeConfig()
const status = ref('')
const facturacion = reactive({ nombre: '', identificacion: '', direccion: '', email: '' })

async function finalizar() {
  status.value = 'Procesando...'
  try {
    const token = localStorage.getItem('token')
    if (!token) return navigateTo('/login?next=/carrito')
    const body = {
      usuario_id: 0,
      items: carrito.items.map(i => ({ producto_id: i.producto_id, cantidad: i.cantidad, precio_unitario: i.precio_unitario })),
      datos_facturacion: { ...facturacion }
    }
    const res = await fetch(`${config.public.apiBase}/api/pedidos/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
      body: JSON.stringify(body)
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.message || 'Error al crear pedido')
    carrito.vaciar()
    status.value = `Pedido creado #${data.id}`
  } catch (e: any) {
    status.value = `Error: ${e.message}`
  }
}
</script>

<style scoped>
.status { margin-top: 8px; color: #555; }
</style>


