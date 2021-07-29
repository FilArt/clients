<template>
  <v-card>
    <v-card-text>
      <users-table-expandable
        :headers="headers"
        :statuses="statuses"
        mode="tramitacion"
        is-support
        show-date-filters
        use-full-name
      />
    </v-card-text>
  </v-card>
</template>

<script>
import UsersTableExpandable from '~/components/tables/UsersTableExpandable'
import constants from '../../../lib/constants'

export default {
  components: {
    UsersTableExpandable,
  },
  data() {
    return {
      headers: ['id', 'fecha_registro', 'fullname', 'bids_count'],
      statuses: Object.values(constants.statuses.tramitacion),
    }
  },
}
</script>
