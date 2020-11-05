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

    <v-row>
      <v-col class="flex-grow-0">
        <solicitudes-bar
          :user-id="user.id"
          :bids="user.bids"
          @bid-added="refresh"
          @chosen="
            chosenBid = $event
            x += 1
          "
        />
      </v-col>

      <div v-if="chosenBid" :key="x" class="flex-grow-1">
        <tramitacion :bid-id="chosenBid" />
      </div>
    </v-row>
  </v-card>
</template>

<script>
export default {
  components: {
    SolicitudesBar: () => import('@/components/support/SolicitudesBar'),
    UserDetailData: () => import('@/components/forms/UserDetailData'),
    Tramitacion: () => import('~/components/support/Tramitacion'),
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
        case 'Pendiente tramitacion':
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
