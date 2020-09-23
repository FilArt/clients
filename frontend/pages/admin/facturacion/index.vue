<template>
  <v-card>
    <v-card-text>
      <users-table
        :client-roles="clientRoles"
        :headers="headers"
        detail-url="/admin/facturacion"
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
      clientRoles: [constants.clientRoles.facturacion.value],
      headers: [
        { text: 'ID', value: 'id' },
        { text: 'Fecha de registro', value: 'date_joined' },
        { text: 'Fecha firma', value: 'fecha_firma' },
        { text: 'Nombre/Razon social', value: 'fullname' },
        { text: 'Responsable', value: 'responsible_fn' },
        { text: 'Solicitud', value: 'bids_count' },
        { text: 'Comisiones', value: 'paid_count' },
        { text: 'Estado', value: 'status' },
        { text: '', value: 'new_messages_count' },
      ],
    }
  },
}
</script>
