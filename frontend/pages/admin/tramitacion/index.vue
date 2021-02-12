<template>
  <v-card>
    <v-card-text>
      <users-table
        :statuses="statuses"
        :headers="headers"
        :mode="mode"
        detail-url="/admin/tramitacion"
        is-support
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
      statuses: [
        constants.statuses.KO,
        constants.statuses.PENDIENTE_TRAMITACION,
        constants.statuses.TRAMITACION_EN_PROCESSO,
      ],
      mode: 'tramitacion',
      headers: [
        'id',
        'fecha_registro',
        'fecha_firma',
        'fullname',
        'responsible_fn',
        'bids_count',
        'status',
        'docs',
        'scorings',
        'calls',
        'offer_status',
        'new_messages_count',
      ],
    }
  },
}
</script>
