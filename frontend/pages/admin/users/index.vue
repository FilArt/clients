<template>
  <v-card>
    <v-card-title>
      Users
    </v-card-title>
    <v-card-text>
      <users-table :users="users" />
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  components: {
    UsersTable: () => import('~/components/tables/UsersTable'),
  },
  async asyncData({ $axios }) {
    const users = await $axios.$get('/users/users/')
    return {
      users,
    }
  },
}
</script>
