<template>
  <v-card>
    <v-card-text>
      <v-toolbar>
        <v-toolbar-title>
          {{ user.fullname }}
        </v-toolbar-title>
      </v-toolbar>
      <user-detail-data :user-id="$route.params.id" />
    </v-card-text>

    <v-divider />

    <v-card-title>Solicitudes</v-card-title>
    <v-card-text>
      <v-list>
        <v-list-group v-for="bid in user.bids" :key="bid.id" v-model="bid.active" no-action>
          <template v-slot:activator>
            <v-list-item-content>
              ID: {{ bid.id }}

              <v-chip :color="bidStatusColor(bid.status)">
                {{ bid.status }}
              </v-chip>
            </v-list-item-content>
          </template>

          <v-list-item>
            <v-list-item-content>
              <tramitacion :bid-id="bid.id" facturacion @tramitate="onTramitate" />
            </v-list-item-content>
          </v-list-item>
        </v-list-group>
      </v-list>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  components: {
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
