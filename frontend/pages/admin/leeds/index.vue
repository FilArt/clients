<template>
  <v-card>
    <v-card-title>
      Leeds
    </v-card-title>
    <v-card-text>
      <users-table :users="leeds" />
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  components: {
    UsersTable: () => import('~/components/tables/UsersTable'),
  },
  async asyncData({ $axios }) {
    const leeds = await $axios.$get('/users/leeds/')
    return {
      leeds,
    }
  },
}
</script>
