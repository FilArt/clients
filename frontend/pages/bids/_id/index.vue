<template>
  <v-card>
    <v-card-title>
      Solicitud
      <v-chip v-text="bid.status" />
    </v-card-title>
    <v-card-text>
      <detail-offer :offer="bid.offer" />
    </v-card-text>

    <v-card-actions>
      <v-row justify="center">
        <v-col class="flex-grow-0">
          <v-btn nuxt :to="`/bids/${bid.id}/purchase`" color="success">
            Editar puntos
            <v-icon right>mdi-pencil</v-icon>
          </v-btn>
        </v-col>
        <v-col class="flex-grow-0">
          <v-btn
            nuxt
            :disabled="bid.status !== 'Pendiente tramitación'"
            :to="`/ofertas/search/?bid_for_change=${bid.id}`"
            color="warning"
          >
            Editar oferta
            <v-icon right>mdi-pencil</v-icon>
          </v-btn>
        </v-col>

        <v-col class="flex-grow-0">
          <delete-button @click="deleteBid" />
        </v-col>
      </v-row>
    </v-card-actions>
    <v-card-text v-if="history.length">
      <history-list :history="history" />
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  components: {
    DetailOffer: () => import('~/components/detailOffer'),
    DeleteButton: () => import('~/components/buttons/deleteButton'),
    HistoryList: () => import('~/components/history/HistoryList'),
  },
  async asyncData({ $axios, params }) {
    const bid = await $axios.$get(`bids/bids/${params.id}/`)
    const history = await $axios.$get(`bids/bids/${params.id}/history/`)
    return { bid, history }
  },
  methods: {
    deleteBid() {
      const bidId = this.bid.id
      this.$swal({
        title: `Eliminar solicitud ${bidId}?`,
        text: 'Una vez borrado, no podrás recuperar esta oferta!',
        icon: 'warning',
        buttons: true,
        dangerMode: true,
      }).then((willDelete) => {
        if (willDelete) {
          this.$axios.$delete(`bids/bids/${bidId}/`).then(() => {
            this.$swal({
              title: 'Solicitud eliminada!',
              icon: 'success',
            })
            this.$router.push('/bids')
          })
        }
      })
    },
  },
}
</script>
