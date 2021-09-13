<template>
  <v-card>
    <v-card-text>
      <users-table-expandable
        :statuses="statuses"
        :headers="headers"
        mode="tramitacion"
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
      statuses: Object.values(constants.statuses.tramitacion),
      mode: 'tramitacion',
      headers: ['id', 'fecha_registro', 'fullname', 'responsible_fn', 'bids_count'],
    }
  },
}
</script>
