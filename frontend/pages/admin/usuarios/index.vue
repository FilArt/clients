<template>
  <v-card>
    <v-card-text>
      <users-table
        default-role="agent"
        show-filters
        allow-delete
        hide-chat
        :headers="headers"
        detail-url="/admin/usuarios"
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
  data() {
    return {
      headers: ['id', 'fullname', 'agent_type', 'phone', 'date_joined', 'last_login', 'actions'],
    }
  },
}
</script>
