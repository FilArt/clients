<template>
  <v-card>
    <v-card-text>
      <users-table
        :statuses="statuses"
        :headers="headers"
        mode="ko_papellera"
        detail-url="/admin/ko"
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
      statuses: [constants.statuses.KO_PAPELLERA],
      headers: ['id', 'created_at', 'fullname', 'responsible_fn', 'bids_count'],
    }
  },
}
</script>
