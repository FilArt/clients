<template>
  <div>
    <v-btn nuxt to="/admin/users" exact>
      Clientes
    </v-btn>
    <v-btn nuxt to="/admin/users?leeds=true" exact>
      Leeds
    </v-btn>
    <v-btn nuxt to="/support">
      Tramitacion
    </v-btn>
  </div>
</template>
<script>
export default {
  name: 'AdminHeader',
}
</script>
