<template>
  <v-card flat>
    <v-toolbar dense>
      <v-toolbar-title>
        <v-btn icon color="error" @click="$router.back()">
          <v-icon>mdi-arrow-left</v-icon>
        </v-btn>
        {{ user.fullname }}
      </v-toolbar-title>
    </v-toolbar>

    <v-card-text>
      <user-detail-data :user-id="$route.params.id" @user-updated="refresh" />
    </v-card-text>

    <v-divider />

    <v-card-text>
      <solicitudes-process :user="user" @bid-added="refresh" @punto-updated="refresh" />
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
    async refresh() {
      const user = await this.$axios.$get(`users/users/${this.$route.params.id}/`)
      await this.$store.dispatch('bids/fetchBids', { params: `user=${user.id}` })
      this.user = user
      this.values = { ...user }
      this.user = await this.$axios.$get(`users/users/${this.user.id}/`)
    },
  },
}
</script>
