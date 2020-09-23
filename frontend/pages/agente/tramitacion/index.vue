<template>
  <v-card>
    <v-card-text>
      <users-table
        :client-roles="clientRoles"
        :headers="headers"
        detail-url="/agente/tramitacion"
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
      clientRoles: [constants.clientRoles.tramitacion.value],
      headers: [
        { text: 'ID', value: 'id' },
        { text: 'Fecha de registro', value: 'date_joined' },
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
