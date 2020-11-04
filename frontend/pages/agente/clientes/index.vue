<template>
  <v-card>
    <v-card-text>
      <users-table :statuses="statuses" :headers="headers" detail-url="/agente/clientes" use-full-name />
    </v-card-text>
  </v-card>
</template>

<script>
import constants from '@/lib/constants'

export default {
  components: {
    UsersTable: () => import('@/components/tables/UsersTable'),
  },
  asyncData() {
    return {
      statuses: [constants.statuses.PAGADO, constants.statuses.PENDIENTE_PAGO],
      headers: [
        { text: 'ID', value: 'id' },
        { text: 'Fecha de registro', value: 'date_joined' },
        { text: 'Fecha firma', value: 'fecha_firma' },
        { text: 'Nombre/Razon social', value: 'fullname', sortable: false },
        // { text: 'Origin', value: 'affiliate' },
        { text: 'Solicitud', value: 'bids_count', sortable: false },
        { text: 'Comisiones', value: 'paid_count' },
        { text: 'Ultima entrada', value: 'last_login' },
      ],
    }
  },
}
</script>
