<template>
  <v-card>
    <v-card-text>
      <users-table
        selectable
        bids-count-header="Puntos suministo"
        :statuses="statuses"
        :headers="headers"
        detail-url="/admin/clientes"
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
      statuses: [constants.statuses.PAGADO, constants.statuses.PENDIENTE_PAGO],
      headers: [
        'id',
        'created_at',
        'fecha_firma',
        'fullname',
        'responsible_fn',
        'bids_count',
        'paid_count',
        'last_login',
        'new_messages_count',
      ],
    }
  },
}
</script>
