<template>
  <v-card>
    <v-card-text>
      <users-table
        :statuses="statuses"
        :headers="headers"
        detail-url="/agente/facturacion"
        show-date-filters
        use-full-name
      />
    </v-card-text>
  </v-card>
</template>

<script>
import constants from '@/lib/constants'

export default {
  components: {
    UsersTable: () => import('~/components/tables/UsersTable'),
  },
  data() {
    return {
      statuses: [constants.statuses.PENDIENTE_PAGO],
      headers: ['id', 'fecha_registro', 'fecha_firma', 'fullname', 'bids_count', 'paid_count', 'status'],
    }
  },
}
</script>
