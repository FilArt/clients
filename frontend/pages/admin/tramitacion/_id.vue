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
      <user-detail-data :user-id="$route.params.id" />
    </v-card-text>

    <v-divider />

    <v-row>
      <v-col class="flex-grow-0">
        <solicitudes-bar
          :bids="user.bids"
          @chosen="
            chosenBid = $event
            x += 1
          "
        />
      </v-col>

      <div v-if="chosenBid" :key="x" class="flex-grow-1">
        <tramitacion
          :bid-id="chosenBid"
          push-to-title="Papelera"
          @tramitate="onTramitate"
          @push-to="pushToKo(chosenBid)"
        />
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
    const user = await $axios.$get(`users/users/${params.id}/?client_role=tramitacion`)

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
      x: 0,
      chosenBid: null,
      cols: 3,
      errorMessages: { status: null, message: null },
    }
  },
  methods: {
    pushToKo(bidId) {
      this.$swal({
        title: 'Mover a la Papelera?',
        icon: 'warning',
        buttons: true,
        dangerMode: true,
      }).then((willDelete) => {
        if (willDelete) {
          this.$axios.$post(`bids/bids/${bidId}/push_to_ko/`).then(() => this.$router.back())
        }
      })
    },
    async onTramitate() {
      const user = await this.$axios.$get(`users/users/${this.$route.params.id}/`)
      this.user = user
      this.values = { phones: [user.phone], ...user }
      if (user.client_role !== 'tramitacion') {
        await this.$router.push(`/admin/facturacion/${this.user.id}`)
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
