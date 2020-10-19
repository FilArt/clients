<template>
  <v-card>
    <v-card-text>
      <users-table
        :statuses="statuses"
        :headers="headers"
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
      statuses: [constants.statuses.KO],
      headers: [
        { text: 'ID', value: 'id' },
        { text: 'Fecha de registro', value: 'date_joined' },
        { text: 'Nombre/Razon social', value: 'fullname', sortable: false },
        { text: 'Responsable', value: 'responsible_fn' },
        { text: 'Solicitud', value: 'bids_count', sortable: false },
        { text: '', value: 'new_messages_count' },
      ],
    }
  },
}
</script>
