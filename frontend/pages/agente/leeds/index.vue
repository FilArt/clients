<template>
  <v-card>
    <v-card-text>
      <users-table
        :client-roles="clientRoles"
        allow-delete
        :headers="headers"
        detail-url="/agente/leeds"
        use-full-name
      />
    </v-card-text>
  </v-card>
</template>

<script>
import constants from '@/lib/constants'

export default {
  components: {
    UsersTable: () => import('@/components/tables/UsersTable'),
  },
  data() {
    return {
      clientRoles: [constants.clientRoles.leeds.value],
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
          text: 'Ultima entrada',
          value: 'last_login',
        },
        {
          text: 'Solicitud',
          value: 'bids_count',
          sortable: false,
        },
      ],
    }
  },
}
</script>
