<template>
  <v-card>
    <v-card-text>
      <admin-header />
    </v-card-text>

    <v-card-text>
      <users-table :users="users" />
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
    const users = await $axios.$get(`/users/users/?leeds=${query.leeds}`)
    return {
      users,
    }
  },
  watch: {
    async $route() {
      this.users = await this.$axios.$get(
        `/users/users/?leeds=${this.$route.query.leeds}`
      )
    },
  },
}
</script>
