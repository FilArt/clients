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
        :statuses="[
          { text: 'KO', value: 'tramitacion_ko' },
          { text: 'Pendiente tramitacion', value: 'tramitacion_pendiente' },
          { text: 'Pagado', value: 'facturacion_ok' },
          { text: 'Pendiente pago', value: 'facturacion_pendiente' },
        ]"
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
export default {
  components: {
    UsersTable: () => import('~/components/tables/UsersTable'),
    UserDetailData: () => import('~/components/forms/UserDetailData'),
  },
  async asyncData({ params, $axios }) {
    const apiUrl = `users/manage_users/${params.id}/`
    const user = await $axios.$get(apiUrl)
    return {
      user,
      apiUrl,
    }
  },
}
</script>
