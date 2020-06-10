<template>
  <v-card>
    <v-container>
      <v-row justify="space-between">
        <v-col cols="auto">
          <v-img
            height="300"
            width="300"
            :src="offer.picture || '/no-image.svg'"
          />
        </v-col>
        <v-col>
          <v-divider />
          <v-card-title v-text="offer.name" />
          <v-divider />
          <v-card-text>
            <p v-for="key in Object.keys(offer)" :key="key">
              {{ key }}: {{ offer[key] }}
            </p>
            {{ offer.description }}
          </v-card-text>
        </v-col>
      </v-row>
      <v-card-actions>
        <v-row>
          <v-col>
            <v-btn
              :disabled="offer.added"
              rounded
              block
              outlined
              color="success"
              @click="addBid"
            >
              {{ offer.added ? 'Already added' : 'Add to portfel'
              }}<v-icon right>mdi-briefcase</v-icon>
            </v-btn>
          </v-col>
          <v-col>
            <return-button :to="back" />
          </v-col>
        </v-row>
      </v-card-actions>
    </v-container>
  </v-card>
</template>

<script>
const clientTypeShortcuts = {
  0: 'individual',
  individual: 0,
  1: 'business',
  business: 1,
}
export default {
  components: {
    ReturnButton: () => import('~/components/buttons/returnButton'),
    RefreshButton: () => import('~/components/buttons/refreshButton'),
    CancelButton: () => import('~/components/buttons/cancelButton'),
  },
  async asyncData({ $axios, params, query }) {
    const offer = await $axios.$get(`calculator/offers/${params.id}/`)
    const back = `/offers/detail?client_type=${
      clientTypeShortcuts[query.client_type || offer.client_type]
    }&tarif=${query.tarif || offer.tarif}`
    return { offer, id: params.id, back }
  },
  methods: {
    addBid() {
      if (this.offer.added) return
      this.$axios.$post('bids/', { offer: this.id }).then(() => {
        this.offer.added = true
        this.$swal({
          title: 'Se ha agregado una solicitud de contrato a la cartera.',
          icon: 'success',
        })
      })
    },
  },
}
</script>
