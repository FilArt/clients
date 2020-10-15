<template>
  <v-card>
    <v-card-text>
      <users-table :statuses="statuses" :headers="headers" detail-url="/agente/clientes" use-full-name />
    </v-card-text>
  </v-card>
</template>

<script>
import constants from '@/lib/constants'

export default {
  components: {
    UsersTable: () => import('@/components/tables/UsersTable'),
  },
  asyncData() {
    return {
      statuses: [
        constants.statuses.PAGADO,
        constants.statuses.PENDIENTE_PAGO,
        constants.statuses.PENDIENTE_PAGO_AGENTE,
        constants.statuses.PENDIENTE_PAGO_CANAL,
      ],
      headers: [
        { text: 'ID', value: 'id' },
        { text: 'Fecha de registro', value: 'date_joined' },
        { text: 'Fecha firma', value: 'fecha_firma' },
        { text: 'Nombre/Razon social', value: 'fullname' },
        { text: 'Origin', value: 'affiliate' },
        { text: 'Solicitud', value: 'bids_count' },
        { text: 'Comisiones', value: 'paid_count' },
        { text: 'Ultima entrada', value: 'last_login' },
      ],
    }
  },
}
</script>
