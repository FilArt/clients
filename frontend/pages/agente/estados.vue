<template>
  <v-card>
    <v-card-text>
      <users-table
        :client-roles="clientRoles"
        :default-headers="headers"
        detail-url="/agente"
        is-support
        read-only
        show-date-filters
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
      clientRoles: [constants.clientRoles.tramitacion.value],
      headers: [
        { text: 'ID', value: 'id' },
        { text: 'Fecha firma', value: 'fecha_firma' },
        { text: 'Email', value: 'email' },
        { text: 'Nombre/Razon social', value: 'fullname' },
        { text: 'Solicitud', value: 'bids_count' },
        { text: 'Estado', value: 'status' },
        { text: 'Doc', value: 'docs' },
        { text: 'Scoring', value: 'scorings' },
        { text: 'Llamadas', value: 'calls' },
      ],
    }
  },
}
</script>
