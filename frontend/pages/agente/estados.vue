<template>
  <v-card>
    <v-card-text>
      <agent-header />
    </v-card-text>

    <v-card-text>
      <users-table :client-role="clientRole" :default-headers="headers" is-support read-only show-date-filters />
    </v-card-text>
  </v-card>
</template>

<script>
import constants from '@/lib/constants'

export default {
  components: {
    UsersTable: () => import('~/components/tables/UsersTable'),
    AgentHeader: () => import('@/components/agent/AgentHeader'),
  },
  data() {
    return {
      clientRole: constants.clientRoles.tramitacion.value,
      headers: [
        { text: 'ID', value: 'id' },
        { text: 'Fecha firmado', value: 'date_joined_date' },
        { text: 'Email', value: 'email' },
        { text: 'Nombre', value: 'first_name' },
        { text: 'Apellido', value: 'last_name' },
        { text: 'Solicitud', value: 'bids_count' },
        { text: 'Solicitud listo', value: 'bids_contracted_count' },
        { text: 'Docs ok', value: 'docs_ok_count' },
        { text: 'Scoring ok', value: 'scoring_ok_count' },
        { text: 'Calls ok', value: 'calls_ok_count' },
      ],
    }
  },
}
</script>
