<template>
  <v-card>
    <v-card-text>
      <users-table :statuses="statuses" allow-delete :headers="headers" detail-url="/admin/leeds" use-full-name />
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
      statuses: [constants.statuses.LEED],
      headers: [
        'id',
        'created_at',
        'fullname',
        'responsible_fn',
        'last_login',
        'bids_count',
        'new_messages_count',
        'actions',
      ],
    }
  },
}
</script>
