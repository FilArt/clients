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
      headers: ['id', 'created_at', 'fecha_firma', 'fullname', 'bids_count', 'paid_count', 'last_login'],
    }
  },
}
</script>
