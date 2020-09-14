<template>
  <v-card>
    <v-card-text>
      <admin-header />
    </v-card-text>

    <v-card-text>
      <users-table show-filters allow-delete hide-chat :default-headers="headers" />
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
        {
          text: 'ID',
          value: 'id',
        },
        {
          text: 'Email',
          value: 'email',
        },
        {
          text: 'Telefono',
          value: 'phone',
        },
        {
          text: 'Nombre/Razon social',
          value: 'fullname',
        },
        {
          text: 'Fecha de registro',
          value: 'date_joined',
        },
        {
          text: 'Ultima entrada',
          value: 'last_login',
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
