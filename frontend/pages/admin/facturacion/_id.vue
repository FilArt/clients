<template>
  <v-card flat>
    <v-toolbar dense>
      <v-toolbar-title>
        {{ user.fullname }}
      </v-toolbar-title>
    </v-toolbar>

    <v-card-text>
      <user-detail-data :user-id="$route.params.id" />
    </v-card-text>

    <v-divider />

    <v-row>
      <v-col class="flex-grow-0">
        <v-navigation-drawer permanent>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title class="title"> Solicitudes </v-list-item-title>
            </v-list-item-content>
          </v-list-item>

          <v-divider></v-divider>

          <v-list dense nav>
            <v-list-item
              v-for="bid in user.bids"
              :key="bid.id"
              :color="bidStatusColor(bid.status)"
              @click="chosenBid = bid.id"
            >
              <v-list-item-subtitle> ID: {{ bid.id }} </v-list-item-subtitle>

              <v-list-item-title>
                {{ bid.status }}
              </v-list-item-title>
            </v-list-item>
          </v-list>
        </v-navigation-drawer>
      </v-col>

      <div v-if="chosenBid" class="flex-grow-1">
        <tramitacion :bid-id="chosenBid" facturacion hide-puntos @tramitate="onTramitate" />
      </div>
    </v-row>
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
      values: {
        phones: [user.phone],
        ...user,
      },
    }
  },
  data() {
    return {
      chosenBid: null,
      cols: 3,
      errorMessages: { status: null, message: null },
    }
  },
  methods: {
    async onTramitate() {
      const user = await this.$axios.$get(`users/users/${this.$route.params.id}/`)
      this.user = user
      this.values = { phones: [user.phone], ...user }
      if (user.client_role === 'tramitacion') {
        await this.$router.push(`/admin/tramitacion/${this.user.id}`)
      } else if (user.client_role === 'client') {
        await this.$router.push(`/admin/clientes/${this.user.id}`)
      }
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
