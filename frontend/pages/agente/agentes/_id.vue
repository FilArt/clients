<template>
  <v-card class="pa-3">
    <v-toolbar>
      <v-toolbar-title>
        {{ user.fullname }}
      </v-toolbar-title>
    </v-toolbar>

    <v-card-text>
      <user-detail-data readonly :user-id="$route.params.id" />
    </v-card-text>

    <v-card-text>
      <users-table
        list-url="users/agent_clients"
        :statuses="statuses"
        :responsible="$route.params.id"
        :detail-url="null"
        :headers="[
          {
            text: 'ID',
            value: 'id',
          },
          {
            text: 'Nombre',
            value: 'fullname',
            sortable: false,
          },
          {
            text: 'Estado',
            value: 'status',
          },
          {
            text: 'Solicitudes',
            value: 'bids_count',
          },
          {
            text: 'Agente comisiones',
            value: 'paid_count',
          },
          {
            text: 'Canal comisiones',
            value: 'canal_paid_count',
          },
        ]"
      />
    </v-card-text>
  </v-card>
</template>

<script>
import constants from '@/lib/constants'

export default {
  components: {
    UsersTable: () => import('~/components/tables/UsersTable'),
    UserDetailData: () => import('~/components/forms/UserDetailData'),
  },
  async asyncData({ params, $axios }) {
    const apiUrl = `users/manage_users/${params.id}/`
    const user = await $axios.$get(apiUrl)
    const statuses = [
      constants.statuses.KO,
      constants.statuses.TRAMITACION_EN_PROCESSO,
      constants.statuses.PENDIENTE_TRAMITACION,
      constants.statuses.PAGADO,
      constants.statuses.PENDIENTE_PAGO,
    ]
    return {
      user,
      apiUrl,
      statuses,
    }
  },
}
</script>
