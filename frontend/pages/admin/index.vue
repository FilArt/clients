<template>
  <v-card>
    <v-card-text>
      <admin-header />
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  components: {
    AdminHeader: () => import('~/components/admin/AdminHeader'),
  },
}
</script>
