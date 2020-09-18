<template>
  <v-card>
    <v-card-text>
      <users-table :client-role="clientRole" :default-headers="headers" is-support show-date-filters use-full-name />
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
      clientRole: constants.clientRoles.tramitacion.value,
      headers: [
        { text: 'ID', value: 'id' },
        { text: 'Fecha de registro', value: 'date_joined_date' },
        { text: 'Nombre/Razon social', value: 'fullname' },
        { text: 'Responsable', value: 'responsible_fn' },
        { text: 'Solicitud', value: 'bids_count' },
        { text: 'Estado', value: 'status' },
        { text: 'Doc', value: 'docs' },
        { text: 'Scoring', value: 'scorings' },
        { text: 'Llamadas', value: 'calls' },
        { text: '', value: 'new_messages_count' },
      ],
    }
  },
}
</script>
