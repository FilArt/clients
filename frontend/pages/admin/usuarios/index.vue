<template>
  <v-card>
    <v-card-text>
      <users-table
        show-filters
        allow-delete
        hide-chat
        :default-headers="headers"
        detail-url="/admin/usuarios"
        use-full-name
      />
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  components: {
    UsersTable: () => import('~/components/tables/UsersTable'),
  },
  data() {
    return {
      headers: [
        {
          text: 'ID',
          value: 'id',
        },
        {
          text: 'Nombre',
          value: 'fullname',
        },
        {
          text: 'Tipo de agente',
          value: 'agent_type',
        },
        {
          text: 'Telefono',
          value: 'phone',
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
