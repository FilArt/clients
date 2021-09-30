<template>
  <v-card>
    <v-card-text>
      <users-table
        :headers="['id', 'fullname', 'phone', 'clients_count', 'last_login']"
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
