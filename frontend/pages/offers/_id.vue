<template>
  <v-card>
    <v-fab-transition>
      <v-btn
        v-if="!isBottomIntersecting && !isTopIntersecting"
        min-width="30%"
        color="primary"
        fixed
        style="z-index: 1000;"
        bottom
        rounded
        right
        nuxt
        :to="back"
      >
        Back
        <v-icon right>mdi-keyboard-return</v-icon>
      </v-btn>
    </v-fab-transition>

    <v-container>
      <v-card v-intersect="onIntersectTop">
        <return-button :to="back" />
      </v-card>

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
      <v-card v-intersect="onIntersectBottom">
        <return-button :to="back" />
      </v-card>
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
  data() {
    return {
      isBottomIntersecting: false,
      isTopIntersecting: true,
    }
  },
  async asyncData({ $axios, params, query }) {
    const offers = await $axios.$get(
      `calculator/offers/?by_name_id=${params.id}`
    )
    return { offers, back: query.back.replace(/@/, '&') }
  },
  methods: {
    onIntersectBottom(entries) {
      this.isBottomIntersecting = entries[0].isIntersecting
    },
    onIntersectTop(entries) {
      this.isTopIntersecting = entries[0].isIntersecting
    },
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
