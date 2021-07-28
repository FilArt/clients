<template>
  <v-card>
    <v-card-title> Borradores </v-card-title>

    <v-card-text>
      <users-table mode="borradores" allow-delete :headers="headers" detail-url="/agente/tramitacion" use-full-name />
    </v-card-text>
  </v-card>
</template>

<script>
import UsersTable from './UsersTable.vue'
export default {
  name: 'Borradores',
  components: { UsersTable },
  data() {
    return {
      headers: ['id', 'fullname', 'actions'],
    }
  },
}
</script>
