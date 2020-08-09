<template>
  <v-card>
    <v-card-text v-if="$auth.user.role === 'admin'">
      <admin-header />
    </v-card-text>

    <v-card-text>
      <users-table :users="users" :headers="headers" />
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  components: {
    UsersTable: () => import('~/components/tables/UsersTable'),
    AdminHeader: () => import('~/components/admin/AdminHeader'),
  },
  async asyncData({ $axios }) {
    const headers = [
      { text: 'ID', value: 'id' },
      { text: 'Usuario', value: 'fullname' },
      { text: 'Bids', value: 'bids_count' },
      { text: 'Bids listo', value: 'bids_contracted_count' },
    ]
    const users = await $axios.$get(
      `users/users/?fields=${headers.map((header) => header.value)}`
    )
    return {
      users,
      headers,
    }
  },
  data() {
    return {}
  },
}
</script>
