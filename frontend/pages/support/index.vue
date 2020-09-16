<template>
  <v-card>
    <v-card-text v-if="$auth.user.role === 'admin'">
      <admin-header />
    </v-card-text>

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
    AdminHeader: () => import('~/components/admin/AdminHeader'),
  },
  data() {
    return {
      clientRole: constants.clientRoles.tramitacion.value,
      headers: [
        { text: 'ID', value: 'id' },
        { text: 'Fecha firmado', value: 'date_joined_date' },
        { text: 'Nombre/Razon social', value: 'fullname' },
        { text: 'Responsable', value: 'responsible' },
        { text: 'Solicitud', value: 'bids_count' },
        { text: 'Solicitud listo', value: 'bids_contracted_count' },
        { text: 'Docs ok', value: 'docs_ok_count' },
        { text: 'Scoring ok', value: 'scoring_ok_count' },
        { text: 'Calls ok', value: 'calls_ok_count' },
        { text: 'Pagado', value: 'paid_count' },
      ],
    }
  },
}
</script>
