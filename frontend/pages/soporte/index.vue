<template>
  <section>
    <h1>Soporte</h1>
    <div v-if="!token" class="notice">
      Para usar el chatbot debes iniciar sesión.
      <NuxtLink to="/login?next=/soporte">Ir a Login</NuxtLink>
    </div>
    <div v-else class="chat">
      <div class="messages" ref="msgsRef">
        <div v-for="(m, i) in messages" :key="i" :class="['msg', m.role]">{{ m.content }}</div>
      </div>
      <div class="input">
        <input v-model="text" @keyup.enter="send" placeholder="Escribe tu mensaje..." />
        <button @click="send">Enviar</button>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { useRuntimeConfig } from 'nuxt/app'
import { io } from 'socket.io-client'
// route derived from file path

const config = useRuntimeConfig()
const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null
const messages = ref<{role:'user'|'bot', content:string}[]>([
  { role: 'bot', content: 'Hola, ¿en qué puedo ayudarte?' }
])
const text = ref('')
const msgsRef = ref<HTMLDivElement|null>(null)

let socket: any
onMounted(() => {
  if (!token) return
  socket = io(config.public.apiBase as unknown as string)
  socket.on('server_message', (data: any) => {
    messages.value.push({ role: 'bot', content: data?.message || 'Conectado' })
  })
  socket.on('answer', (data: any) => {
    messages.value.push({ role: 'bot', content: data?.message || 'Sin respuesta' })
    nextTick(() => msgsRef.value && (msgsRef.value.scrollTop = msgsRef.value.scrollHeight))
  })
})

function send() {
  if (!text.value.trim()) return
  messages.value.push({ role: 'user', content: text.value })
  socket.emit('ask', { message: text.value })
  text.value = ''
  nextTick(() => msgsRef.value && (msgsRef.value.scrollTop = msgsRef.value.scrollHeight))
}
</script>

<style scoped>
.notice { background: #fff3cd; border: 1px solid #ffeeba; padding: 12px; border-radius: 6px; }
.chat { border: 1px solid #eee; border-radius: 8px; }
.messages { height: 360px; overflow: auto; padding: 12px; background: #f8f9fa; }
.msg { margin: 8px 0; padding: 10px 12px; border-radius: 16px; max-width: 70%; }
.msg.user { background: #0b5ed7; color: #fff; margin-left: auto; }
.msg.bot { background: #e9ecef; color: #222; }
.input { display: flex; gap: 8px; padding: 10px; }
input { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 6px; }
button { padding: 10px 16px; background: #0b5ed7; color: #fff; border: 0; border-radius: 6px; cursor: pointer; }
</style>


