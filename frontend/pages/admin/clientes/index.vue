<template>
  <v-card>
    <v-card-text>
      <users-table :client-roles="clientRoles" :headers="headers" detail-url="/admin/clientes" use-full-name />
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
      clientRoles: [constants.clientRoles.clients.value, constants.clientRoles.facturacion.value],
      headers: [
        { text: 'ID', value: 'id' },
        { text: 'Fecha de registro', value: 'date_joined' },
        { text: 'Fecha firma', value: 'fecha_firma' },
        { text: 'Nombre/Razon social', value: 'fullname' },
        { text: 'Responsable', value: 'responsible_fn' },
        { text: 'Origin', value: 'affiliate' },
        { text: 'Solicitud', value: 'bids_count' },
        { text: 'Comisiones', value: 'paid_count' },
        { text: 'Ultima entrada', value: 'last_login' },
        { text: '', value: 'new_messages_count' },
      ],
    }
  },
}
</script>
