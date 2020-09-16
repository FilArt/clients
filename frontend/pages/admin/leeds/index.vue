<template>
  <v-card>
    <v-card-text>
      <admin-header />
    </v-card-text>

    <v-card-text>
      <users-table :client-role="userRole" allow-delete :default-headers="headers" use-full-name />
    </v-card-text>
  </v-card>
</template>

<script>
import constants from '@/lib/constants'

export default {
  components: {
    AdminHeader: () => import('@/components/admin/AdminHeader'),
    UsersTable: () => import('@/components/tables/UsersTable'),
  },
  data() {
    return {
      userRole: constants.clientRoles.leeds.value,
      headers: [
        {
          text: 'ID',
          value: 'id',
        },
        {
          text: 'Fecha de registro',
          value: 'date_joined_date',
        },
        {
          text: 'Nombre/Razon social',
          value: 'fullname',
        },
        {
          text: 'Origin',
          value: 'affiliate',
        },
        {
          text: 'Responsable',
          value: 'responsible',
        },
        {
          text: 'Ultima entrada',
          value: 'last_login',
        },
        {
          text: 'Cartera',
          value: 'bids_count',
          sortable: false,
        },
        {
          text: 'Nuevo mensajes',
          value: 'new_messages_count',
          sortable: false,
        },
        {
          value: 'actions',
          sortable: false,
        },
      ],
    }
  },
}
</script>
