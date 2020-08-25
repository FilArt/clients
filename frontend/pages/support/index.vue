<template>
  <v-card>
    <v-card-text v-if="$auth.user.role === 'admin'">
      <admin-header />
    </v-card-text>

    <v-card-text>
      <users-table :default-headers="headers" is-support />
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  components: {
    UsersTable: () => import('~/components/tables/UsersTable'),
    AdminHeader: () => import('~/components/admin/AdminHeader'),
  },
  data() {
    return {
      headers: [
        { text: 'ID', value: 'id' },
        { text: 'Email', value: 'email' },
        { text: 'Nombre', value: 'first_name' },
        { text: 'Apellido', value: 'last_name' },
        { text: 'Solicitud', value: 'bids_count' },
        { text: 'Solicitud listo', value: 'bids_contracted_count' },
      ],
    }
  },
}
</script>
