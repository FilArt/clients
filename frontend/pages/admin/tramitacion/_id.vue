<template>
  <v-card flat>
    <v-toolbar dense>
      <v-toolbar-title>
        <v-btn icon color="error" @click="$router.back()">
          <v-icon>mdi-arrow-left</v-icon>
        </v-btn>
        {{ user.fullname }}
      </v-toolbar-title>

      <v-spacer />

      <v-toolbar-items>
        <v-btn color="error" @click="moveToKo">Mover a papellera</v-btn>
      </v-toolbar-items>
    </v-toolbar>

    <v-card-text>
      <user-detail-data :user-id="$route.params.id" @user-updated="refresh" />
    </v-card-text>

    <v-divider />

    <v-card-text>
      <solicitudes-process :user="user" @bid-added="refresh" @tramitate="onTramitate" />
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  components: {
    SolicitudesProcess: () => import('@/components/SolicitudesProcess'),
    UserDetailData: () => import('@/components/forms/UserDetailData'),
  },
  async asyncData({ $axios, params }) {
    const user = await $axios.$get(`users/users/${params.id}/`)

    return {
      user,
      values: { ...user },
    }
  },
  methods: {
    async onTramitate() {
      const user = await this.$axios.$get(`users/users/${this.$route.params.id}/`)
      this.user = user
      this.values = { ...user }
    },
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
    async moveToKo() {
      await this.$axios.$patch(`users/users/${this.user.id}/`, { ko: true })
      await this.$router.push(`/admin/ko/${this.user.id}`)
    },
    async refresh() {
      this.user = await this.$axios.$get(`users/users/${this.user.id}/`)
    },
  },
}
</script>
