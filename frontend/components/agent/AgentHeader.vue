<template>
  <div class="d-flex flex-wrap justify-space-around align-center">
    <v-btn v-for="btn in buttons" :key="btn.to" color="#004680" dark :to="btn.to" nuxt v-text="btn.text" />
  </div>
</template>

<script>
export default {
  name: 'AgentHeader',
  data() {
    return {
      buttons: [
        { text: 'Dashboard', to: '/agente/dashboard' },
        { text: 'Leeds', to: '/agente/leeds' },
        { text: 'Clients', to: '/agente/clientes' },
        { text: 'Estados tramitacion', to: '/agente/estados' },
      ],
    }
  },
}
</script>
