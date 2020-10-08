<template>
  <v-card>
    <v-card-text>
      <users-table
        :headers="[
          { text: 'ID', value: 'id' },
          { text: 'Nombre', value: 'fullname' },
          {
            text: 'Telefono',
            value: 'phone',
          },
          { text: 'Clientes', value: 'clients_count' },
          {
            text: 'Ultima entrada',
            value: 'last_login',
          },
        ]"
        hide-chat
        list-url="users/canal_agents"
        detail-url="/agente/agentes"
        use-full-name
      />
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  components: {
    UsersTable: () => import('~/components/tables/UsersTable'),
  },
}
</script>
