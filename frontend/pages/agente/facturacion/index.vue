<template>
  <v-card>
    <v-card-text>
      <users-table-expandable :statuses="statuses" :headers="headers" show-date-filters use-full-name />
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
      statuses: [constants.statuses.PENDIENTE_PAGO],
      headers: ['id', 'created_at', 'fecha_firma', 'fullname', 'bids_count', 'paid_count', 'status'],
    }
  },
}
</script>
