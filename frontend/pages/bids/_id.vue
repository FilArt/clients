<template>
  <v-card>
    <v-card-title>Bid <v-chip v-text="bid.status" /></v-card-title>
    <v-card-text>
      <detail-offer :offer="bid.offer" />
    </v-card-text>

    <v-card-actions>
      <v-row class="text-center">
        <v-col>
          <v-btn
            nuxt
            :to="`/bids/purchase?bid=${bid.id}&isIndividual=${
              bid.client_type === 0
            }&card=${bid.card}`"
            color="success"
          >
            {{ bid.card ? 'Change' : 'Buy' }}
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
        >
          <span slot="icon">
            <v-icon>{{ !story.old_status ? 'mdi-plus' : '' }}</v-icon>
          </span>
          <span slot="opposite">{{ story.dt }}</span>
          <v-card class="elevation-2">
            <v-card-title class="headline">
              <span v-if="!story.old_status">Created</span>
              <span v-else>{{ story.new_status }}</span>
            </v-card-title>
            <v-card-text>
              {{ story.message }}
            </v-card-text>
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
        title: `Delete bid ${bidId}?`,
        text: 'Once deleted, you will not be able to recover this bid!',
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
