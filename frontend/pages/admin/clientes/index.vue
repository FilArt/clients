<template>
  <v-card>
    <v-card-text>
      <users-table
        selectable
        bids-count-header="Puntos suministros"
        mode="client"
        :statuses="statuses"
        :headers="headers"
        detail-url="/admin/clientes"
        use-full-name
        company-filters
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
        'puntos_count',
        'paid_count',
        'last_login',
        'call_visit_id',
      ],
    }
  },
}
</script>
