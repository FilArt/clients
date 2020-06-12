<template>
  <v-card>
    <v-container>
      <div v-for="offer in offers" :key="offer.id">
        <v-row justify="space-between">
          <v-col cols="auto">
            <v-img
              height="300"
              width="300"
              :src="offer.picture || '/no-image.svg'"
            />
          </v-col>
          <v-col>
            <v-card-title v-text="offer.name" />
            <v-divider />
            <v-card-text>
              <p v-for="key in Object.keys(offer)" :key="key">
                {{ key }}: {{ offer[key] }}
              </p>
              {{ offer.description }}
            </v-card-text>
          </v-col>
          <v-card-actions>
            <v-row>
              <v-col>
                <v-btn
                  rounded
                  block
                  outlined
                  color="success"
                  @click="addBid(offer.id)"
                >
                  Add to portfel<v-icon right>mdi-briefcase</v-icon>
                </v-btn>
              </v-col>
            </v-row>
          </v-card-actions>
        </v-row>
        <v-divider />
      </div>
      <return-button :to="back" />
    </v-container>
  </v-card>
</template>

<script>
export default {
  components: {
    ReturnButton: () => import('~/components/buttons/returnButton'),
    RefreshButton: () => import('~/components/buttons/refreshButton'),
    CancelButton: () => import('~/components/buttons/cancelButton'),
  },
  async asyncData({ $axios, params, query }) {
    const offers = await $axios.$get(
      `calculator/offers/?by_name_id=${params.id}`
    )
    return { offers, back: query.back.replace(/@/, '&') }
  },
  methods: {
    addBid(bidId) {
      let data = { offer: bidId }
      if (this.$route.query.fromCalculator === 'true') {
        data = this.$store.state.calculatorForm
        data.offer = bidId
      }
      this.$axios.$post('bids/', data).then(() => {
        this.$swal({
          title: 'Se ha agregado una solicitud de contrato a la cartera.',
          icon: 'success',
        })
      })
    },
  },
}
</script>
