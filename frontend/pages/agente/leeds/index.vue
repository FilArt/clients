<template>
  <v-card>
    <v-card-text>
      <users-table :statuses="statuses" allow-delete :headers="headers" detail-url="/agente/leeds" use-full-name />
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
      statuses: [constants.statuses.LEED],
      headers: [
        {
          text: 'ID',
          value: 'id',
        },
        {
          text: 'Fecha de registro',
          value: 'date_joined',
        },
        {
          text: 'Nombre/Razon social',
          value: 'fullname',
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
