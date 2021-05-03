<template>
  <v-card>
    <v-card-text>
      <user-detail-data :user-id="$route.params.id" />
    </v-card-text>

    <v-divider />

    <v-card-text>
      <solicitudes-bar :user-id="$route.params.id" />
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  components: {
    SolicitudesBar: () => import('@/components/support/SolicitudesBar'),
    UserDetailData: () => import('@/components/forms/UserDetailData'),
  },
  async asyncData({ $axios, params }) {
    const user = await $axios.$get(`users/users/${params.id}/`)

    return {
      user,
      values: { ...user },
    }
  },
  data() {
    return {
      cols: 3,
      errorMessages: { status: null, message: null },
    }
  },
  methods: {
    bidStatusColor(status) {
      let color
      switch (status) {
        case 'OK':
          color = 'success'
          break
        case 'Pendiente tramitación':
          color = 'warning'
          break
        default:
          color = 'error'
          break
      }
      return color
    },
    async refresh() {
      this.user = await this.$axios.$get(`users/users/${this.user.id}/`)
    },
  },
}
</script>
