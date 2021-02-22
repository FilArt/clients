<template>
  <v-card>
    <v-card-text>
      <users-table-expandable
        :statuses="statuses"
        :headers="headers"
        :mode="mode"
        detail-url="/admin/tramitacion"
        is-support
        show-date-filters
      />
    </v-card-text>
  </v-card>
</template>

<script>
import constants from '@/lib/constants'
import UsersTableExpandable from '@/components/tables/UsersTableExpandable'

export default {
  components: {
    UsersTableExpandable,
  },
  data() {
    return {
      statuses: [
        constants.statuses.KO,
        constants.statuses.PENDIENTE_TRAMITACION,
        constants.statuses.TRAMITACION_EN_PROCESO,
      ],
      mode: 'tramitacion',
      headers: ['id', 'fecha_registro', 'fecha_firma', 'fullname', 'responsible_fn', 'bids_count'],
    }
  },
}
</script>
