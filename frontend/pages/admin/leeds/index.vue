<template>
  <v-card>
    <v-card-text>
      <admin-header />
    </v-card-text>
    <v-card-text>
      <users-table :users="leeds" />
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
    const leeds = await $axios.$get('/users/leeds/')
    return {
      leeds,
    }
  },
}
</script>
