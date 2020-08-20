<template>
  <v-btn-toggle>
    <v-btn nuxt to="/admin/users" exact>
      Usuarios
    </v-btn>
    <v-btn nuxt to="/support">
      Tramitacion
    </v-btn>
    <v-btn nuxt to="/admin/charts">
      Charts
    </v-btn>
  </v-btn-toggle>
</template>
<script>
export default {
  name: 'AdminHeader',
}
</script>
