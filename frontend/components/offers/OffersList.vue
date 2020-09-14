<template>
  <v-row class="d-flex align-center justify-space-around flex-wrap">
    <v-col v-for="offer in offers" :key="offer.id" class="flex-grow-0">
      <v-card :to="detailOfferUrl(offer)" nuxt class="mx-auto">
        <v-img max-height="150" max-width="300" :src="offer.company_logo || '/no-image.svg'" />
        <v-card-subtitle v-text="'Comercializadora: ' + offer.company" />
        <v-card-text>{{ offer.name }}</v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>
<script>
export default {
  name: 'OffersList',
  props: {
    offers: {
      type: Array,
      default: () => [],
    },
    filters: {
      type: Object,
      default: () => {
        return {
          client_type: 0,
        }
      },
    },
  },
  methods: {
    detailOfferUrl(offer) {
      const params = {
        ...this.filters,
        name: offer.name,
        is_price_permanent: offer.is_price_permanent,
      }

      const query = Object.keys(params)
        .filter((k) => params[k] || params[k] === 0)
        .map((k) => `${encodeURIComponent(k)}=${encodeURIComponent(params[k])}`)
        .join('&')

      return `/ofertas/${this.filters.client_type === 0 ? 'hogar' : 'pyme'}/${offer.id}/?${query}`
    },
  },
}
</script>
