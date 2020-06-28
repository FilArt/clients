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
      <v-row class="text-center">
        <v-col>
          <v-btn nuxt :to="`/bids/${bid.id}/purchase`" color="success">
            {{ bid.card ? 'Editar' : 'Contratar' }}
            <v-icon right>{{ bid.card ? 'mdi-pencil' : 'mdi-plus' }}</v-icon>
          </v-btn>
        </v-col>
        <v-col>
          <delete-button @click="deleteBid" />
        </v-col>
      </v-row>
    </v-card-actions>
    <v-card-text>
      <v-timeline>
        <v-timeline-item
          v-for="story in history"
          :key="story.id"
          class="text-left"
          :left="story.user === 'me'"
          :right="story.user !== 'me'"
        >
          <span slot="icon">
            <v-icon>{{ !story.old_status ? 'mdi-plus' : '' }}</v-icon>
          </span>
          <span slot="opposite">
            {{ story.dt }}
            <br />
            {{ story.user.email || story.user }}
          </span>
          <v-card class="elevation-2">
            <v-card-title class="headline">
              <span>{{ story.new_status }}</span>
            </v-card-title>
            <v-card-text>{{ story.message }}</v-card-text>
          </v-card>
        </v-timeline-item>
      </v-timeline>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  components: {
    DetailOffer: () => import('~/components/detailOffer'),
    DeleteButton: () => import('~/components/buttons/deleteButton'),
  },
  async asyncData({ $axios, params }) {
    const bid = await $axios.$get(`bids/${params.id}/`)
    const history = await $axios.$get(`bids/${params.id}/history/`)
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
          this.$axios.$delete(`bids/${bidId}/`).then(() => {
            this.$swal({ title: 'Solicitud eliminada!', icon: 'success' })
            this.$router.push('/bids')
          })
        }
      })
    },
  },
}
</script>
