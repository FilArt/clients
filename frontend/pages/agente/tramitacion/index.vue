<template>
  <v-card>
    <v-card-text>
      <users-table-expandable
        :statuses="statuses"
        :headers="headers"
        mode="tramitacion"
        is-support
        show-date-filters
        use-full-name
      />
    </v-card-text>
  </v-card>
</template>

<script>
import constants from '@/lib/constants'
import UsersTableExpandable from '~/components/tables/UsersTableExpandable'

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
      headers: [
        'id',
        'fecha_registro',
        'fullname',
        'bids_count',
        'status',
        'docs',
        'scorings',
        'calls',
        'offer_status',
      ],
    }
  },
}
</script>
