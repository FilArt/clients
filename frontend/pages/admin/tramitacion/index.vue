<template>
  <v-card>
    <v-card-text>
      <users-table
        :statuses="statuses"
        :headers="headers"
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
      statuses: [constants.statuses.PENDIENTE_TRAMITACION, constants.statuses.TRAMITACION_EN_PROCESSO],
      headers: [
        { text: 'ID', value: 'id' },
        { text: 'Fecha de registro', value: 'date_joined' },
        { text: 'Nombre/Razon social', value: 'fullname', sortable: false },
        { text: 'Responsable', value: 'responsible_fn' },
        { text: 'Solicitud', value: 'bids_count', sortable: false },
        { text: 'Estado', value: 'status' },
        { text: 'Doc', value: 'docs', sortable: false },
        { text: 'Scoring', value: 'scorings', sortable: false },
        { text: 'Llamadas', value: 'calls', sortable: false },
        { text: '', value: 'new_messages_count', sortable: false },
      ],
    }
  },
}
</script>
