<template>
  <v-card>
    <v-card-text>
      <users-table
        default-role="agent"
        show-filters
        allow-delete
        :headers="headers"
        use-full-name
        detail-url="/admin/usuarios"
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
      headers: ['id', 'fullname', 'agent_type', 'phone', 'created_at', 'last_modified', 'last_login', 'actions'],
    }
  },
}
</script>
