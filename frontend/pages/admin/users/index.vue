<template>
  <v-card>
    <v-card-text>
      <admin-header />
    </v-card-text>

    <v-card-text>
      <users-table :users="users" @refresh="refresh" />
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  components: {
    UsersTable: () => import('~/components/tables/UsersTable'),
    AdminHeader: () => import('~/components/admin/AdminHeader'),
  },
  async asyncData({ $axios, query }) {
    const users = await $axios.$get(`/users/users/?leeds=${query.leeds || false}&clients=${query.clients || false}`)
    return {
      users,
    }
  },
  watch: {
    $route() {
      this.refresh()
    },
  },
  methods: {
    refresh() {
      const query = this.$route.query
      this.$axios
        .$get(`/users/users/?leeds=${query.leeds || false}&clients=${query.clients || false}`)
        .then((users) => (this.users = users))
    },
  },
}
</script>
