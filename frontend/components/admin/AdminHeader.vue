<template>
  <div class="d-flex flex-wrap justify-space-around align-center">
    <v-btn v-for="btn in buttons" :key="btn.to" color="#004680" dark :to="btn.to" nuxt v-text="btn.text" />
  </div>
</template>
<script>
export default {
  name: 'AdminHeader',
  data() {
    return {
      buttons: [
        { text: 'Dashboard', to: '/admin/dashboard' },
        { text: 'Leeds', to: '/admin/leeds' },
        { text: 'Clientes', to: '/admin/clientes' },
        { text: 'Usuarios', to: '/admin/usuarios' },
        { text: 'Tramitacion', to: '/support' },
      ],
    }
  },
}
</script>
